"""
app/api/pages.py — Server-side rendered HTML pages using Jinja2.
Data fetched and escaped server-side. No JS HTML building.
"""
import os
import time
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.session import get_session
from app.db import get_watchlist, get_user_by_id

router = APIRouter()

_tpl_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(_tpl_dir))
_V = os.environ.get("BUILD_TS", str(int(time.time())))

def _format_number(value):
    try: return "{:,}".format(int(value))
    except: return str(value)

templates.env.filters["format_number"] = _format_number


def _r(request, name, active, **kw):
    ctx = {"request": request, "active": active, "v": _V}
    ctx.update(kw)
    ctx_clean = {k: v for k, v in ctx.items() if k != "request"}
    return templates.TemplateResponse(request=ctx["request"], name=name, context=ctx_clean)


@router.get("/devices", response_class=HTMLResponse)
async def devices_page(request: Request, q: str = "", limit: int = 24, offset: int = 0):
    from app.scrapers.devices import get_devices
    try:
        data = await get_devices(q=q or None, limit=limit, offset=offset)
    except Exception:
        data = {"devices": [], "total": 0}
    return _r(request, "devices.html", "devices",
        title=("Devices — " + q + " — Droidify") if q else "Devices — Droidify",
        devices=data.get("devices", []),
        total=data.get("total", 0),
        q=q, limit=limit, offset=offset)


@router.get("/roms", response_class=HTMLResponse)
async def roms_page(request: Request, q: str = "", limit: int = 20, offset: int = 0):
    from app.scrapers.roms import get_all_roms as get_roms
    try:
        data = await get_roms(q=q or None, limit=limit, offset=offset)
    except Exception:
        data = {"roms": [], "total": 0}
    return _r(request, "roms.html", "roms",
        title=("ROMs — " + q + " — Droidify") if q else "ROMs — Droidify",
        roms=data.get("roms", []),
        total=data.get("total", 0),
        q=q, limit=limit, offset=offset)


@router.get("/recoveries", response_class=HTMLResponse)
async def recoveries_page(request: Request, q: str = "", limit: int = 20, offset: int = 0):
    from app.scrapers.recoveries import get_recoveries
    try:
        data = await get_recoveries(q=q or None, limit=limit, offset=offset)
    except Exception:
        data = {"recoveries": [], "total": 0}
    return _r(request, "recoveries.html", "recoveries",
        title="Recoveries — Droidify",
        recoveries=data.get("recoveries", []),
        total=data.get("total", 0),
        q=q, limit=limit, offset=offset)


@router.get("/tools", response_class=HTMLResponse)
async def tools_page(request: Request, q: str = ""):
    from app.scrapers.tools import get_tools
    try:
        data    = await get_tools()
        all_tools = data.get("tools", data) if isinstance(data, dict) else data
    except Exception:
        all_tools = []
    if q:
        ql = q.lower()
        all_tools = [t for t in all_tools if
            ql in (t.get("name") or "").lower() or
            ql in (t.get("description") or "").lower() or
            ql in (t.get("category") or "").lower()]
    return _r(request, "tools.html", "tools",
        title="Tools — Droidify", tools=all_tools, q=q)


@router.get("/guides", response_class=HTMLResponse)
async def guides_page(request: Request, q: str = ""):
    from app.scrapers.guides import get_all_guides as _get_all_guides, get_guides_for_device as _get_device_guides
    try:
        if q:
            guides = await _get_device_guides(q)
        else:
            data   = await _get_all_guides(limit=50)
            guides = data.get("guides", [])
    except Exception:
        guides = []
    return _r(request, "guides.html", "guides",
        title=("Guides — " + q + " — Droidify") if q else "Guides — Droidify",
        guides=guides, q=q)


@router.get("/android", response_class=HTMLResponse)
async def android_page(request: Request):
    from app.scrapers.android_versions import get_android_versions
    try:
        data     = await get_android_versions()
        versions = list(reversed(data.get("versions", [])))
    except Exception:
        versions = []
    return _r(request, "android.html", "android",
        title="Android Versions — Droidify", versions=versions)


@router.get("/watchlist", response_class=HTMLResponse)
async def watchlist_page(request: Request):
    import asyncio
    session   = get_session(request)
    user      = None
    watchlist = []
    if session:
        user = await get_user_by_id(session["user_id"])
        if user:
            from app.db import get_watchlist as _gwl
            codenames = await _gwl(session["user_id"])
            if codenames:
                from app.api.watchlist import _fetch_device_info
                watchlist = list(await asyncio.gather(
                    *[_fetch_device_info(c) for c in codenames]
                ))
    return _r(request, "watchlist.html", "watchlist",
        title="Watchlist — Droidify", user=user, watchlist=watchlist)


@router.post("/watchlist/{codename}/remove")
async def watchlist_remove(codename: str, request: Request):
    session = get_session(request)
    if session:
        from app.db import remove_from_watchlist
        await remove_from_watchlist(session["user_id"], codename)
    return RedirectResponse("/watchlist", status_code=303)

@router.get("/device/{codename}", response_class=HTMLResponse)
async def device_page(codename: str, request: Request):
    import re as _re
    if not _re.match(r'^[a-zA-Z0-9_-]{1,64}$', codename):
        return _r(request, "device.html", "devices",
            title="Device not found — Droidify",
            device=None, error="Invalid device codename.")
    try:
        import asyncio as _aio
        from app.scrapers.devices import get_device_detail
        from app.scrapers.roms import get_roms_for_device
        from app.scrapers.recoveries import get_recovery_for_device
        from app.scrapers.samfw import get_samfw_for_device
        from app.api.devices import LOS_BRANCH_TO_ANDROID

        device, roms, recoveries, samfw = await _aio.gather(
            get_device_detail(codename),
            get_roms_for_device(codename),
            get_recovery_for_device(codename),
            get_samfw_for_device(codename),
            return_exceptions=True,
        )

        # Handle exceptions from gather
        device     = device     if isinstance(device, dict)     else None
        roms       = roms       if isinstance(roms, list)       else []
        recoveries = recoveries if isinstance(recoveries, list) else []
        samfw      = samfw      if isinstance(samfw, list)      else []

        if not device:
            return _r(request, "device.html", "devices",
                title="Device not found — Droidify",
                device=None, error=f'Device "{codename}" not found.')

        # Build LineageOS ROM entries
        if device.get("has_lineageos"):
            los_roms = []
            for branch in device.get("lineageos_branches", []):
                android = LOS_BRANCH_TO_ANDROID.get(branch, "?")
                los_roms.append({
                    "name": "LineageOS",
                    "source": "lineageos",
                    "codename": codename,
                    "android_base": android,
                    "version_label": f"Branch: {branch}",
                    "download_url": f"https://download.lineageos.org/devices/{codename}/builds",
                })
            roms = los_roms + [r for r in roms if r.get("source") != "lineageos"]

        device["roms"]           = roms
        device["recoveries"]     = recoveries
        device["stock_firmware"] = samfw

        name = device.get("model_name") or device.get("codename", codename)
        return _r(request, "device.html", "devices",
            title=f'{name} — Droidify',
            device=device)

    except Exception as e:
        return _r(request, "device.html", "devices",
            title="Device not found — Droidify",
            device=None, error=f'Could not load device "{codename}". Please try again.')
