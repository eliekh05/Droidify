"""
app/api/terms.py — server-side terms agreement for logged-in users.
"""
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.db import record_terms_agreement, has_agreed_terms
from app.session import get_session

router = APIRouter()


@router.post("/agree", tags=["auth"])
async def agree_terms(request: Request):
    """Record that the current logged-in user has agreed to the terms."""
    session = get_session(request)
    if not session:
        return JSONResponse({"ok": False, "reason": "not logged in"}, status_code=401)

    user_id = session["user_id"]
    fwd     = request.headers.get("X-Forwarded-For", "")
    ip      = fwd.split(",")[0].strip() if fwd else (
              request.client.host if request.client else "unknown")
    ua      = request.headers.get("User-Agent", "")[:200]

    await record_terms_agreement(user_id, ip, ua)
    return JSONResponse({"ok": True})


@router.get("/status", tags=["auth"])
async def terms_status(request: Request):
    """Check if the current user has agreed to the terms."""
    session = get_session(request)
    if not session:
        return JSONResponse({"agreed": False, "logged_in": False})

    agreed = await has_agreed_terms(session["user_id"])
    return JSONResponse({"agreed": agreed, "logged_in": True})
