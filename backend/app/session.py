"""
app/session.py — signed cookie session using itsdangerous.
HttpOnly, Secure, SameSite=Lax. No JWT, no database lookup per request.
Session data is signed but not encrypted — do not store sensitive values.
"""
import json
import os
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi import Request

SECRET = os.environ.get("SESSION_SECRET", "")
COOKIE = "droidify_session"
MAX_AGE = 60 * 60 * 24 * 30  # 30 days


def _signer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(SECRET, salt="session")


def set_session(response, data: dict) -> None:
    token = _signer().dumps(data)
    response.set_cookie(
        key=COOKIE,
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=MAX_AGE,
        path="/",
    )


def get_session(request: Request) -> dict | None:
    token = request.cookies.get(COOKIE)
    if not token or not SECRET:
        return None
    try:
        return _signer().loads(token, max_age=MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None


def clear_session(response) -> None:
    response.delete_cookie(key=COOKIE, path="/")
