"""
app/api/auth.py — GitHub OAuth2 login, callback, logout, and session endpoints.
"""
import os
import httpx
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.db import upsert_user, get_user_by_id, has_agreed_terms
from app.session import set_session, get_session, clear_session

router = APIRouter()

GITHUB_CLIENT_ID     = os.environ.get("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
CALLBACK_URL         = os.environ.get(
    "CALLBACK_URL",
    "https://eliekh05-droidify-hf.hf.space/api/auth/callback"
)


@router.get("/login", include_in_schema=False)
async def login(request: Request):
    """Redirect to GitHub OAuth."""
    if not GITHUB_CLIENT_ID:
        return JSONResponse({"detail": "OAuth not configured"}, status_code=503)
    url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={CALLBACK_URL}"
        "&scope=read:user"
    )
    return RedirectResponse(url)


@router.get("/callback", include_in_schema=False)
async def callback(request: Request, code: str = "", error: str = ""):
    """GitHub redirects here with a code. Exchange it for a token."""
    if error or not code:
        return RedirectResponse("/?auth=error")

    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            json={
                "client_id":     GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code":          code,
                "redirect_uri":  CALLBACK_URL,
            },
            headers={"Accept": "application/json"},
            timeout=10,
        )
        token_data = token_resp.json()
        access_token = token_data.get("access_token", "")
        if not access_token:
            return RedirectResponse("/?auth=error")

        # Fetch GitHub user profile
        user_resp = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
            timeout=10,
        )
        gh = user_resp.json()

    github_id  = gh.get("id")
    login_name = gh.get("login", "")
    name       = gh.get("name")
    avatar     = gh.get("avatar_url")

    if not github_id or not login_name:
        return RedirectResponse("/?auth=error")

    # Upsert user into database
    user_id = await upsert_user(github_id, login_name, name, avatar)

    # Create session
    response = RedirectResponse("/")
    set_session(response, {"user_id": user_id, "login": login_name})
    return response


@router.get("/logout", include_in_schema=False)
async def logout(request: Request):
    response = RedirectResponse("/")
    clear_session(response)
    return response


@router.get("/me", tags=["auth"])
async def me(request: Request):
    """Return current user info. Returns null if not logged in."""
    session = get_session(request)
    if not session:
        return JSONResponse({"user": None})

    user = await get_user_by_id(session["user_id"])
    if not user:
        return JSONResponse({"user": None})

    agreed = await has_agreed_terms(user["id"])
    return JSONResponse({
        "user": {
            "id":         user["id"],
            "login":      user["login"],
            "name":       user["name"],
            "avatar_url": user["avatar_url"],
            "agreed_terms": agreed,
        }
    })
