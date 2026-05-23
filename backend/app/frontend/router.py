"""
frontend/router.py
==================
Serves HTML pages from templates/ and static assets from static/.
FastAPI StaticFiles handles CSS, JS, icons — real files, real paths,
real line numbers in DevTools.
"""
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles

FRONTEND = Path(__file__).parent
STATIC   = FRONTEND / "static"
TMPL     = FRONTEND / "templates"

router = APIRouter()


# ── HTML pages ────────────────────────────────────────────────────────────────

def _html(name: str, status: int = 200) -> HTMLResponse:
    return HTMLResponse(
        content=(TMPL / name).read_text(),
        status_code=status,
    )


@router.get("/",                include_in_schema=False)
@router.get("/index.html",      include_in_schema=False)
async def serve_index():        return _html("index.html")

@router.get("/devices.html",    include_in_schema=False)
async def serve_devices():      return _html("devices.html")

@router.get("/device.html",     include_in_schema=False)
async def serve_device():       return _html("device.html")

@router.get("/roms.html",       include_in_schema=False)
async def serve_roms():         return _html("roms.html")

@router.get("/recoveries.html", include_in_schema=False)
async def serve_recoveries():   return _html("recoveries.html")

@router.get("/tools.html",      include_in_schema=False)
async def serve_tools():        return _html("tools.html")

@router.get("/android.html",    include_in_schema=False)
async def serve_android():      return _html("android.html")

@router.get("/guides.html",     include_in_schema=False)
async def serve_guides():       return _html("guides.html")

@router.get("/privacy.html",    include_in_schema=False)
async def serve_privacy():      return _html("privacy.html")

@router.get("/404.html",        include_in_schema=False)
async def serve_404():          return _html("404.html", status=404)


# ── Root-level static files (favicon, manifest, sw, robots) ──────────────────
# These must be explicit routes because StaticFiles is mounted at /static

@router.get("/favicon.svg",     include_in_schema=False)
async def favicon_svg():        return FileResponse(STATIC / "favicon.svg")

@router.get("/favicon.ico",     include_in_schema=False)
async def favicon_ico():        return FileResponse(STATIC / "favicon.ico")

@router.get("/manifest.json",   include_in_schema=False)
async def manifest():           return FileResponse(STATIC / "manifest.json")

@router.get("/sw.js",           include_in_schema=False)
async def sw():
    return FileResponse(
        STATIC / "sw.js",
        headers={"Cache-Control": "no-store"},
    )

@router.get("/robots.txt",      include_in_schema=False)
async def robots():             return FileResponse(STATIC / "robots.txt")

@router.get("/apple-touch-icon.png",                     include_in_schema=False)
@router.get("/apple-touch-icon-precomposed.png",         include_in_schema=False)
@router.get("/apple-touch-icon-120x120.png",             include_in_schema=False)
@router.get("/apple-touch-icon-120x120-precomposed.png", include_in_schema=False)
async def apple_touch():        return FileResponse(STATIC / "apple-touch-icon.png")
