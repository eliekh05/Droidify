"""
app/api/watchlist.py — Device watchlist for logged-in users.
GET    /api/watchlist                   — list saved devices with info
POST   /api/watchlist/{codename}        — add device
DELETE /api/watchlist/{codename}        — remove device
GET    /api/watchlist/{codename}/status — check if saved
"""
import asyncio
import re
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.db import add_to_watchlist, remove_from_watchlist, get_watchlist, is_in_watchlist
from app.session import get_session
from app.scrapers.devices import get_devices

router = APIRouter()

_CODENAME_RE = re.compile(r'^[a-z0-9_-]{1,40}$')


def _require_auth(request: Request):
    session = get_session(request)
    if not session:
        return None, JSONResponse({"detail": "Not authenticated"}, status_code=401)
    return session["user_id"], None


async def _fetch_device_info(codename: str) -> dict:
    try:
        result = await get_devices(q=codename, limit=5, offset=0)
        devs   = result.get("devices", [])
        match  = next((d for d in devs if d.get("codename") == codename), None)
        if match:
            return {
                "codename":      match.get("codename"),
                "model":         match.get("model") or match.get("name"),
                "manufacturer":  match.get("manufacturer") or match.get("oem"),
                "has_lineageos": match.get("has_lineageos", False),
                "has_twrp":      match.get("has_twrp", False),
                "has_orangefox": match.get("has_orangefox", False),
                "rom_count":     match.get("rom_count", 0),
            }
    except Exception:
        pass
    return {"codename": codename, "model": None}


@router.get("")
async def list_watchlist(request: Request):
    user_id, err = _require_auth(request)
    if err:
        return err
    codenames = await get_watchlist(user_id)
    if not codenames:
        return JSONResponse({"watchlist": [], "total": 0})
    devices = await asyncio.gather(*[_fetch_device_info(c) for c in codenames])
    return JSONResponse({"watchlist": list(devices), "total": len(devices)})


@router.post("/{codename}")
async def add_device(codename: str, request: Request):
    user_id, err = _require_auth(request)
    if err:
        return err
    if not _CODENAME_RE.match(codename):
        return JSONResponse({"detail": "Invalid codename"}, status_code=400)
    existing = await get_watchlist(user_id)
    from app.db import WATCHLIST_CAP
    if len(existing) >= WATCHLIST_CAP:
        return JSONResponse({"detail": f"Watchlist limit is {WATCHLIST_CAP} devices."}, status_code=400)
    added = await add_to_watchlist(user_id, codename)
    return JSONResponse({"ok": True, "added": added, "codename": codename})


@router.delete("/{codename}")
async def remove_device(codename: str, request: Request):
    user_id, err = _require_auth(request)
    if err:
        return err
    if not _CODENAME_RE.match(codename):
        return JSONResponse({"detail": "Invalid codename"}, status_code=400)
    removed = await remove_from_watchlist(user_id, codename)
    return JSONResponse({"ok": True, "removed": removed, "codename": codename})


@router.get("/{codename}/status")
async def watchlist_status(codename: str, request: Request):
    user_id, err = _require_auth(request)
    if err:
        return JSONResponse({"saved": False})
    if not _CODENAME_RE.match(codename):
        return JSONResponse({"saved": False})
    saved = await is_in_watchlist(user_id, codename)
    return JSONResponse({"saved": saved, "codename": codename})
