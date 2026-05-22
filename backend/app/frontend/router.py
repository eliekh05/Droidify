"""
frontend/router.py
==================
Serves all frontend assets and HTML pages.
- Static assets: ETag + Cache-Control headers, computed at import time
- HEAD routes: explicit, correct Content-Length — no middleware hack
- HTML pages: no-cache so browsers always revalidate
"""
from __future__ import annotations

import base64
import hashlib

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

from .assets import (
    style_css, api_js, home_js, devices_js, device_detail_js,
    roms_js, recoveries_js, tools_js, android_js, guides_js,
    manifest_json, sw_js, robots_txt, favicon_svg,
    icon_192_b64, icon_512_b64, apple_touch_b64,
    favicon_ico_b64,
)
from . import pages

router = APIRouter()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _etag(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return '"' + hashlib.sha1(data).hexdigest()[:16] + '"'


def _text(content: str, media_type: str, *, cache: str = "public, max-age=300, must-revalidate") -> Response:
    return Response(
        content=content,
        media_type=f"{media_type}; charset=utf-8",
        headers={"ETag": _etag(content), "Cache-Control": cache},
    )


def _binary(b64: str, media_type: str) -> Response:
    data = base64.b64decode(b64)
    return Response(
        content=data,
        media_type=media_type,
        headers={"ETag": _etag(data), "Cache-Control": "public, max-age=86400"},
    )


def _html(page: str) -> HTMLResponse:
    return HTMLResponse(
        content=page,
        headers={"ETag": _etag(page), "Cache-Control": "no-cache"},
    )


# Pre-compute HEAD metadata at import time (sizes + ETags from actual content)
def _head(content: str | bytes, media_type: str, *, long_cache: bool = False) -> Response:
    if isinstance(content, str):
        raw = content.encode()
    else:
        raw = content
    return Response(
        content=b"",
        status_code=200,
        headers={
            "Content-Type": media_type,
            "Content-Length": str(len(raw)),
            "ETag": _etag(raw),
            "Cache-Control": "public, max-age=86400" if long_cache else "public, max-age=300",
        },
    )


# ── JS & CSS ──────────────────────────────────────────────────────────────────

@router.get("/css/style.css",       include_in_schema=False)
async def serve_css():              return _text(style_css, "text/css")

@router.get("/js/api.js",           include_in_schema=False)
async def serve_api_js():           return _text(api_js, "application/javascript")

@router.get("/js/home.js",          include_in_schema=False)
async def serve_home_js():          return _text(home_js, "application/javascript")

@router.get("/js/devices.js",       include_in_schema=False)
async def serve_devices_js():       return _text(devices_js, "application/javascript")

@router.get("/js/device-detail.js", include_in_schema=False)
async def serve_device_detail_js(): return _text(device_detail_js, "application/javascript")

@router.get("/js/roms.js",          include_in_schema=False)
async def serve_roms_js():          return _text(roms_js, "application/javascript")

@router.get("/js/recoveries.js",    include_in_schema=False)
async def serve_recoveries_js():    return _text(recoveries_js, "application/javascript")

@router.get("/js/tools.js",         include_in_schema=False)
async def serve_tools_js():         return _text(tools_js, "application/javascript")

@router.get("/js/android.js",       include_in_schema=False)
async def serve_android_js():       return _text(android_js, "application/javascript")

@router.get("/js/guides.js",        include_in_schema=False)
async def serve_guides_js():        return _text(guides_js, "application/javascript")


# ── Manifest, SW, robots ──────────────────────────────────────────────────────

@router.get("/manifest.json",  include_in_schema=False)
async def serve_manifest():    return _text(manifest_json, "application/manifest+json")

@router.get("/sw.js",          include_in_schema=False)
async def serve_sw():          return _text(sw_js, "application/javascript", cache="no-store")

@router.get("/robots.txt",     include_in_schema=False)
async def serve_robots():      return _text(robots_txt, "text/plain")


# ── Icons & images ────────────────────────────────────────────────────────────

@router.get("/favicon.svg",    include_in_schema=False)
async def serve_favicon_svg(): return _text(favicon_svg, "image/svg+xml")

@router.get("/favicon.ico",    include_in_schema=False)
async def serve_favicon_ico(): return _binary(favicon_ico_b64, "image/x-icon")

@router.get("/icons/icon-192.png", include_in_schema=False)
async def serve_icon_192():    return _binary(icon_192_b64, "image/png")

@router.get("/icons/icon-512.png", include_in_schema=False)
async def serve_icon_512():    return _binary(icon_512_b64, "image/png")

@router.get("/apple-touch-icon.png",                    include_in_schema=False)
@router.get("/apple-touch-icon-precomposed.png",        include_in_schema=False)
@router.get("/apple-touch-icon-120x120.png",            include_in_schema=False)
@router.get("/apple-touch-icon-120x120-precomposed.png",include_in_schema=False)
async def serve_apple_touch(): return _binary(apple_touch_b64, "image/png")


# ── HTML pages ────────────────────────────────────────────────────────────────

@router.get("/",                include_in_schema=False)
@router.get("/index.html",      include_in_schema=False)
async def serve_index():        return _html(pages.index)

@router.get("/devices.html",    include_in_schema=False)
@router.get("/devices",         include_in_schema=False)
async def serve_devices():      return _html(pages.devices)

@router.get("/device.html",     include_in_schema=False)
@router.get("/device",          include_in_schema=False)
async def serve_device():       return _html(pages.device)

@router.get("/roms.html",       include_in_schema=False)
@router.get("/roms",            include_in_schema=False)
async def serve_roms():         return _html(pages.roms)

@router.get("/recoveries.html", include_in_schema=False)
@router.get("/recoveries",      include_in_schema=False)
async def serve_recoveries():   return _html(pages.recoveries)

@router.get("/tools.html",      include_in_schema=False)
@router.get("/tools",           include_in_schema=False)
async def serve_tools():        return _html(pages.tools)

@router.get("/android.html",    include_in_schema=False)
@router.get("/android",         include_in_schema=False)
async def serve_android():      return _html(pages.android)

@router.get("/guides.html",     include_in_schema=False)
@router.get("/guides",          include_in_schema=False)
async def serve_guides():       return _html(pages.guides)

@router.get("/privacy.html",    include_in_schema=False)
async def serve_privacy():      return _html(pages.privacy())

@router.get("/404.html",        include_in_schema=False)
async def serve_404():          return HTMLResponse(content=pages.page_404, status_code=404)


# ── HEAD routes ───────────────────────────────────────────────────────────────
# FastAPI doesn't auto-handle HEAD on GET routes (issue #1773).
# Content-Length computed from actual asset bytes at import time — never stale.

@router.head("/css/style.css",        include_in_schema=False)
async def head_css():                 return _head(style_css, "text/css")

@router.head("/js/api.js",            include_in_schema=False)
async def head_api():                 return _head(api_js, "application/javascript")

@router.head("/js/home.js",           include_in_schema=False)
async def head_home():                return _head(home_js, "application/javascript")

@router.head("/js/devices.js",        include_in_schema=False)
async def head_devices_js():          return _head(devices_js, "application/javascript")

@router.head("/js/device-detail.js",  include_in_schema=False)
async def head_device_detail():       return _head(device_detail_js, "application/javascript")

@router.head("/js/roms.js",           include_in_schema=False)
async def head_roms():                return _head(roms_js, "application/javascript")

@router.head("/js/recoveries.js",     include_in_schema=False)
async def head_recoveries():          return _head(recoveries_js, "application/javascript")

@router.head("/js/tools.js",          include_in_schema=False)
async def head_tools():               return _head(tools_js, "application/javascript")

@router.head("/js/android.js",        include_in_schema=False)
async def head_android():             return _head(android_js, "application/javascript")

@router.head("/js/guides.js",         include_in_schema=False)
async def head_guides():              return _head(guides_js, "application/javascript")

@router.head("/manifest.json",        include_in_schema=False)
async def head_manifest():            return _head(manifest_json, "application/manifest+json")

@router.head("/sw.js",                include_in_schema=False)
async def head_sw():                  return _head(sw_js, "application/javascript")

@router.head("/robots.txt",           include_in_schema=False)
async def head_robots():              return _head(robots_txt, "text/plain")

@router.head("/favicon.svg",          include_in_schema=False)
async def head_favicon_svg():         return _head(favicon_svg, "image/svg+xml")

@router.head("/favicon.ico",          include_in_schema=False)
async def head_favicon_ico():         return _head(base64.b64decode(favicon_ico_b64), "image/x-icon", long_cache=True)

@router.head("/icons/icon-192.png",   include_in_schema=False)
async def head_icon_192():            return _head(base64.b64decode(icon_192_b64), "image/png", long_cache=True)

@router.head("/icons/icon-512.png",   include_in_schema=False)
async def head_icon_512():            return _head(base64.b64decode(icon_512_b64), "image/png", long_cache=True)

@router.head("/apple-touch-icon.png",                     include_in_schema=False)
@router.head("/apple-touch-icon-precomposed.png",         include_in_schema=False)
@router.head("/apple-touch-icon-120x120.png",             include_in_schema=False)
@router.head("/apple-touch-icon-120x120-precomposed.png", include_in_schema=False)
async def head_apple():               return _head(base64.b64decode(apple_touch_b64), "image/png", long_cache=True)

@router.head("/",                include_in_schema=False)
@router.head("/index.html",      include_in_schema=False)
@router.head("/devices.html",    include_in_schema=False)
@router.head("/device.html",     include_in_schema=False)
@router.head("/roms.html",       include_in_schema=False)
@router.head("/recoveries.html", include_in_schema=False)
@router.head("/tools.html",      include_in_schema=False)
@router.head("/android.html",    include_in_schema=False)
@router.head("/guides.html",     include_in_schema=False)
@router.head("/privacy.html",    include_in_schema=False)
@router.head("/404.html",        include_in_schema=False)
async def head_html():
    return Response(content=b"", status_code=200,
                    headers={"Content-Type": "text/html; charset=utf-8"})
