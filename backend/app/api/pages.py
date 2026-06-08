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

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return _r(request, "index.html", "home", title="Droidify — Android ROM & Device Index")


_tpl_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(_tpl_dir))
_V = os.environ.get("BUILD_TS", str(int(time.time())))

async def _gate(request: Request) -> bool:
    """
    Returns True if the user is allowed through (agreed to terms).
    Logic:
      - localStorage is checked client-side (terms.js).
      - Here we do the server-side check:
        * Anonymous user   → block (terms.js handles redirect)
        * Signed-in user who agreed → allow
        * Signed-in user who hasn't agreed → block
    We return True to allow, False to redirect to /terms.html.
    Anonymous users are NOT blocked server-side — terms.js handles them
    so the page loads fast on cache hit. Signed-in users get server check
    so agreeing on one device unlocks all devices immediately.
    """
    session = get_session(request)
    if not session:
        # Anonymous — let terms.js handle it client-side
        return True
    from app.db import has_agreed_terms
    return await has_agreed_terms(session["user_id"])


def _terms_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse("/terms.html", status_code=302)


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
    if not await _gate(request): return _terms_redirect()
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
    if not await _gate(request): return _terms_redirect()
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
    if not await _gate(request): return _terms_redirect()
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
    if not await _gate(request): return _terms_redirect()
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
    from app.scrapers.devices import get_devices, get_device_by_codename
    device_found   = False
    similar        = []
    try:
        if q:
            guides = await _get_device_guides(q)
            # Check if this is a real device codename
            exact = await get_devices(q=q, limit=10)
            devices = exact.get("devices", [])
            # Exact codename match
            device_found = any(d.get("codename", "").lower() == q.lower() for d in devices)
            if not device_found:
                # Suggest real devices whose codename contains the search term
                similar = [d for d in devices if q.lower() in d.get("codename", "").lower()][:5]
        else:
            data   = await _get_all_guides(limit=50)
            guides = data.get("guides", [])
    except Exception:
        guides = []
    return _r(request, "guides.html", "guides",
        title=("Guides — " + q + " — Droidify") if q else "Guides — Droidify",
        guides=guides, q=q, device_found=device_found, similar=similar)


@router.get("/android", response_class=HTMLResponse)
async def android_page(request: Request):
    if not await _gate(request): return _terms_redirect()
    from app.scrapers.android_versions import get_android_versions, get_android_versions_dict
    try:
        raw      = await get_android_versions()
        versions = list(reversed(raw))
    except Exception:
        versions = []
    return _r(request, "android.html", "android",
        title="Android Versions — Droidify", versions=versions)


@router.get("/watchlist", response_class=HTMLResponse)
async def watchlist_page(request: Request):
    if not await _gate(request): return _terms_redirect()
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
    alerts = []
    if user:
        from app.db import get_unread_alerts
        alerts = await get_unread_alerts(session["user_id"])

    return _r(request, "watchlist.html", "watchlist",
        title="Watchlist — Droidify", user=user, watchlist=watchlist, alerts=alerts)


@router.post("/watchlist/{codename}/remove")
async def watchlist_remove(codename: str, request: Request):
    session = get_session(request)
    if session:
        from app.db import remove_from_watchlist
        await remove_from_watchlist(session["user_id"], codename)
    return RedirectResponse("/watchlist", status_code=303)

@router.get("/device", response_class=HTMLResponse)
@router.get("/device/", response_class=HTMLResponse)
async def device_bare(request: Request):
    from fastapi.responses import HTMLResponse as _H
    return _H("""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Device lookup — Droidify</title>
<style>
body{background:#0b0f14;color:#e8eef5;font-family:system-ui,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;text-align:center}
.wrap{max-width:480px;padding:2rem}
.logo{font-size:1.6rem;font-weight:800;letter-spacing:-.04em;margin-bottom:2rem}
.logo span{color:#3dd68c}
code{background:#141c26;border:1px solid #1e2d42;border-radius:6px;padding:.2rem .5rem;font-size:.9rem;color:#3dd68c}
a{color:#3dd68c}
p{color:#4a6080;font-size:.9rem;line-height:1.6;margin:.75rem 0}
</style></head>
<body><div class="wrap">
<div class="logo"><span>Droid</span>ify</div>
<p>Nothing to see here without a device codename.</p>
<p>Try: <code>/device/beryllium</code></p>
<p>Or search on the <a href="/devices">devices page</a>.</p>
<p style="font-size:.8rem;color:#2a3a50">API: <code>GET /api/devices/{codename}</code></p>
</div></body></html>""", status_code=200)


@router.get("/device/{codename}", response_class=HTMLResponse)
async def device_page(codename: str, request: Request):
    if not await _gate(request): return _terms_redirect()
    import re as _re
    if not _re.match(r"^[a-zA-Z0-9_.-]{1,50}$", codename):
        from fastapi.responses import Response as _Resp
        return _Resp(status_code=400)
    _CODENAME_RE = _re.compile(r"^[a-zA-Z0-9_.-]{1,50}$")
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

        # Auth — watchlist status
        name    = device.get("model_name") or device.get("codename", codename)
        session = get_session(request)
        user    = None
        saved   = False
        if session:
            user = await get_user_by_id(session["user_id"])
            if user:
                from app.db import is_in_watchlist
                saved = await is_in_watchlist(session["user_id"], codename)

        return _r(request, "device.html", "devices",
            title=f'{name} — Droidify',
            device=device, user=user, saved=saved)

    except Exception as e:
        return _r(request, "device.html", "devices",
            title="Device not found — Droidify",
            device=None, error=f'Could not load device "{codename}". Please try again.')

@router.post("/device/{codename}/save")
async def device_save(codename: str, request: Request):
    from fastapi.responses import RedirectResponse
    session = get_session(request)
    if session:
        from app.db import add_to_watchlist
        await add_to_watchlist(session["user_id"], codename)
        # cap enforced inside add_to_watchlist — returns False if over cap, ignored here
    return RedirectResponse(f"/device/{codename}", status_code=303)

@router.post("/device/{codename}/unsave")
async def device_unsave(codename: str, request: Request):
    from fastapi.responses import RedirectResponse
    session = get_session(request)
    if session:
        from app.db import remove_from_watchlist
        await remove_from_watchlist(session["user_id"], codename)
    return RedirectResponse(f"/device/{codename}", status_code=303)


@router.get("/perks", response_class=HTMLResponse)
async def perks_page(request: Request):
    session = get_session(request)
    user = await get_user_by_id(session["user_id"]) if session else None
    return _r(request, "perks.html", "perks",
        title="Perks — Droidify", user=user)

@router.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    return _r(request, "faq.html", "", title="FAQ — Droidify")


@router.get("/privacy", response_class=HTMLResponse)
async def privacy_page(request: Request):
    return _r(request, "privacy.html", "", title="Privacy — Droidify")


@router.get("/terms", response_class=HTMLResponse)
async def terms_page(request: Request):
    return _r(request, "terms.html", "", title="Terms — Droidify")


@router.post("/watchlist/alerts/read")
async def watchlist_mark_alerts_read(request: Request):
    from fastapi.responses import RedirectResponse
    session = get_session(request)
    if session:
        from app.db import mark_alerts_read
        await mark_alerts_read(session["user_id"])
    return RedirectResponse("/watchlist", status_code=303)
