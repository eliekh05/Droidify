"""
app/api/alerts.py — ROM alert endpoints.
GET  /api/alerts         — unread alerts for current user
POST /api/alerts/read    — mark all alerts as read
GET  /api/alerts/count   — unread count (for navbar badge)
"""
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.session import get_session
from app.db import get_unread_alerts, mark_alerts_read

router = APIRouter()


@router.get("")
async def list_alerts(request: Request):
    session = get_session(request)
    if not session:
        return JSONResponse({"alerts": [], "total": 0})
    alerts = await get_unread_alerts(session["user_id"])
    return JSONResponse({"alerts": alerts, "total": len(alerts)})


@router.get("/count")
async def alert_count(request: Request):
    session = get_session(request)
    if not session:
        return JSONResponse({"count": 0})
    alerts = await get_unread_alerts(session["user_id"])
    return JSONResponse({"count": len(alerts)})


@router.post("/read")
async def read_alerts(request: Request):
    session = get_session(request)
    if not session:
        return JSONResponse({"ok": False}, status_code=401)
    await mark_alerts_read(session["user_id"])
    return JSONResponse({"ok": True})
