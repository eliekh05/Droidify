"""
app/api/auth.py — GitHub OAuth2 login, callback, logout, and session endpoints.
"""
import os
import time
import httpx
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

from app.db import upsert_user, get_user_by_id, has_agreed_terms
from app.session import set_session, get_session, clear_session

router = APIRouter()

GITHUB_CLIENT_ID     = os.environ.get("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
CALLBACK_URL         = os.environ.get(
    "CALLBACK_URL",
    "https://eliekh05-droidify-hf.hf.space/api/auth/callback"
)

_rl: dict[str, tuple[int, int]] = {}

def _check_rate_limit(ip: str) -> bool:
    w = int(time.time()) // 60
    prev_w, count = _rl.get(ip, (w, 0))
    if prev_w != w:
        count = 0
    if count >= 10:
        return False
    _rl[ip] = (w, count + 1)
    return True


@router.get("/login", include_in_schema=False)
async def login(request: Request):
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
    if error or not code:
        return RedirectResponse("/?auth=error")

    fwd = request.headers.get("X-Forwarded-For", "")
    ip  = fwd.split(",")[0].strip() if fwd else (
          request.client.host if request.client else "unknown")
    if not _check_rate_limit(ip):
        return JSONResponse({"detail": "Too many requests"}, status_code=429)

    async with httpx.AsyncClient() as client:
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

    user_id = await upsert_user(github_id, login_name, name, avatar)

    # HTML meta-refresh — ensures cookie is stored BEFORE browser navigates.
    # A 307/302 redirect causes browsers (especially Safari/mobile) to follow
    # the redirect before the Set-Cookie header is persisted.
    html = (
        "<!DOCTYPE html><html><head>"
        '<meta http-equiv="refresh" content="0;url=/">'
        "</head><body>Redirecting...</body></html>"
    )
    response = HTMLResponse(content=html, status_code=200)
    set_session(response, {"user_id": user_id, "login": login_name})
    return response


@router.get("/logout", include_in_schema=False)
async def logout(request: Request):
    response = RedirectResponse("/")
    clear_session(response)
    return response


@router.get("/me", tags=["auth"])
async def me(request: Request):
    session = get_session(request)
    if not session:
        return JSONResponse({"user": None})

    user = await get_user_by_id(session["user_id"])
    if not user:
        return JSONResponse({"user": None})

    agreed = await has_agreed_terms(user["id"])
    return JSONResponse({
        "user": {
            "id":           user["id"],
            "login":        user["login"],
            "name":         user["name"],
            "avatar_url":   user["avatar_url"],
            "agreed_terms": agreed,
        }
    })
