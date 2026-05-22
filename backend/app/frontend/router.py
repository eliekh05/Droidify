"""
frontend/router.py
==================
Serves the entire frontend from Python string / bytes literals embedded in
assets.py and pages.py.  No filesystem reads at runtime — zero dependency on
the /frontend directory.

Mount order (applied in main.py):
  app.include_router(frontend_router)   ← must come AFTER all /api/* routers
"""
import base64
import hashlib
from typing import Callable

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response

from . import assets, pages

router = APIRouter()

# ── ETag helpers ──────────────────────────────────────────────────────────────

def _etag(content: str | bytes) -> str:
    if isinstance(content, str):
        content = content.encode()
    return '"' + hashlib.sha1(content).hexdigest()[:16] + '"'


def _text_response(
    content: str,
    media_type: str,
    *,
    charset: str = "utf-8",
    extra_headers: dict | None = None,
) -> Response:
    tag = _etag(content)
    headers = {"ETag": tag, "Cache-Control": "public, max-age=300, must-revalidate"}
    if extra_headers:
        headers.update(extra_headers)
    return Response(
        content=content,
        media_type=f"{media_type}; charset={charset}",
        headers=headers,
    )


def _binary_response(b64: str, media_type: str) -> Response:
    data = base64.b64decode(b64)
    tag = _etag(data)
    return Response(
        content=data,
        media_type=media_type,
        headers={
            "ETag": tag,
            "Cache-Control": "public, max-age=86400",
        },
    )


def _html(page: str) -> HTMLResponse:
    tag = _etag(page)
    return HTMLResponse(
        content=page,
        headers={
            "ETag": tag,
            "Cache-Control": "no-cache",   # HTML: always revalidate
        },
    )


# ── Static assets ─────────────────────────────────────────────────────────────

@router.get("/css/style.css", include_in_schema=False)
async def serve_css():
    return _text_response(assets.style_css, "text/css")


@router.get("/js/api.js", include_in_schema=False)
async def serve_api_js():
    return _text_response(assets.api_js, "application/javascript")


@router.get("/js/home.js", include_in_schema=False)
async def serve_home_js():
    return _text_response(assets.home_js, "application/javascript")


@router.get("/js/devices.js", include_in_schema=False)
async def serve_devices_js():
    return _text_response(assets.devices_js, "application/javascript")


@router.get("/js/device-detail.js", include_in_schema=False)
async def serve_device_detail_js():
    return _text_response(assets.device_detail_js, "application/javascript")


@router.get("/js/roms.js", include_in_schema=False)
async def serve_roms_js():
    return _text_response(assets.roms_js, "application/javascript")


@router.get("/js/recoveries.js", include_in_schema=False)
async def serve_recoveries_js():
    return _text_response(assets.recoveries_js, "application/javascript")


@router.get("/js/tools.js", include_in_schema=False)
async def serve_tools_js():
    return _text_response(assets.tools_js, "application/javascript")


@router.get("/js/android.js", include_in_schema=False)
async def serve_android_js():
    return _text_response(assets.android_js, "application/javascript")


@router.get("/js/guides.js", include_in_schema=False)
async def serve_guides_js():
    return _text_response(assets.guides_js, "application/javascript")


@router.get("/manifest.json", include_in_schema=False)
async def serve_manifest():
    return _text_response(assets.manifest_json, "application/manifest+json")


@router.get("/sw.js", include_in_schema=False)
async def serve_sw():
    # Service workers must not be cached by the browser
    return _text_response(
        assets.sw_js,
        "application/javascript",
        extra_headers={"Cache-Control": "no-store"},
    )


@router.get("/robots.txt", include_in_schema=False)
async def serve_robots():
    return _text_response(assets.robots_txt, "text/plain")


@router.get("/favicon.svg", include_in_schema=False)
async def serve_favicon():
    return _text_response(assets.favicon_svg, "image/svg+xml")


@router.get("/icons/icon-192.png", include_in_schema=False)
def _head_response(content_length: int, media_type: str, etag: str) -> Response:
    """Correct HEAD response — headers only, no body, no Content-Length mismatch."""
    return Response(
        content=b"",
        status_code=200,
        media_type=media_type,
        headers={
            "ETag": etag,
            "Cache-Control": "public, max-age=86400",
            "Content-Length": str(content_length),
            "X-Content-Type-Options": "nosniff",
        },
    )


async def serve_icon_192():
    return _binary_response(assets.icon_192_b64, "image/png")


@router.get("/icons/icon-512.png", include_in_schema=False)
async def serve_icon_512():
    return _binary_response(assets.icon_512_b64, "image/png")


# Browsers auto-probe these — 404s spam logs and break iOS PWA icon
@router.get("/favicon.ico", include_in_schema=False)
async def serve_favicon_ico():
    return _binary_response(assets.favicon_ico_b64, "image/x-icon")


@router.get("/apple-touch-icon.png", include_in_schema=False)
@router.get("/apple-touch-icon-precomposed.png", include_in_schema=False)
@router.get("/apple-touch-icon-120x120.png", include_in_schema=False)
@router.get("/apple-touch-icon-120x120-precomposed.png", include_in_schema=False)
async def serve_apple_touch_icon():
    # 180x180 PNG — Safari uses this for home screen / dock icon
    return _binary_response(assets.apple_touch_b64, "image/png")


# ── HTML pages ────────────────────────────────────────────────────────────────

@router.get("/", include_in_schema=False)
async def serve_index():
    return _html(pages.index)


@router.get("/index.html", include_in_schema=False)
async def serve_index_html():
    return _html(pages.index)


@router.get("/devices.html", include_in_schema=False)
@router.get("/devices", include_in_schema=False)
async def serve_devices():
    return _html(pages.devices)


@router.get("/device.html", include_in_schema=False)
@router.get("/device", include_in_schema=False)
async def serve_device():
    return _html(pages.device)


@router.get("/roms.html", include_in_schema=False)
@router.get("/roms", include_in_schema=False)
async def serve_roms():
    return _html(pages.roms)


@router.get("/recoveries.html", include_in_schema=False)
@router.get("/recoveries", include_in_schema=False)
async def serve_recoveries():
    return _html(pages.recoveries)


@router.get("/tools.html", include_in_schema=False)
@router.get("/tools", include_in_schema=False)
async def serve_tools():
    return _html(pages.tools)


@router.get("/android.html", include_in_schema=False)
@router.get("/android", include_in_schema=False)
async def serve_android():
    return _html(pages.android)


@router.get("/guides.html", include_in_schema=False)
@router.get("/guides", include_in_schema=False)
async def serve_guides():
    return _html(pages.guides)


@router.get("/privacy.html", include_in_schema=False)
async def privacy_page():
    from .pages import privacy
    return HTMLResponse(privacy())


@router.get("/404.html", include_in_schema=False)
async def serve_404():
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=pages.page_404, status_code=404)


# ── HEAD routes for all static assets ───────────────────────────────────────
# Required because FastAPI doesn't auto-support HEAD on GET routes (issue #1773)
# BaseHTTPMiddleware approach causes Content-Length mismatch crash
# Explicit routes are the only correct fix

@router.head("/css/style.css", include_in_schema=False)
async def head_style():
    return _head_response(48136, "text/css", "b83ee84fc705538c")

@router.head("/js/api.js", include_in_schema=False)
async def head_api_js():
    return _head_response(11983, "application/javascript", "7355be8533a24e8b")

@router.head("/js/home.js", include_in_schema=False)
async def head_home_js():
    return _head_response(8594, "application/javascript", "89532eb9c5ebc57e")

@router.head("/js/devices.js", include_in_schema=False)
async def head_devices_js():
    return _head_response(3277, "application/javascript", "0a8adce0b731f774")

@router.head("/js/device-detail.js", include_in_schema=False)
async def head_device_detail_js():
    return _head_response(5569, "application/javascript", "bb5633c4b63d27a9")

@router.head("/js/roms.js", include_in_schema=False)
async def head_roms_js():
    return _head_response(3391, "application/javascript", "564d7f2fd6120668")

@router.head("/js/recoveries.js", include_in_schema=False)
async def head_recoveries_js():
    return _head_response(3348, "application/javascript", "e1569b3062510723")

@router.head("/js/tools.js", include_in_schema=False)
async def head_tools_js():
    return _head_response(3120, "application/javascript", "bb6a10e5877d19b5")

@router.head("/js/android.js", include_in_schema=False)
async def head_android_js():
    return _head_response(3342, "application/javascript", "d7946b948de5e433")

@router.head("/js/guides.js", include_in_schema=False)
async def head_guides_js():
    return _head_response(6197, "application/javascript", "969823a926e6921f")

@router.head("/manifest.json", include_in_schema=False)
async def head_manifest():
    return _head_response(4259, "application/manifest+json", "dc2ca8cba08837e2")

@router.head("/sw.js", include_in_schema=False)
async def head_sw():
    return _head_response(1854, "application/javascript", "571b131ccadd6eec")

@router.head("/robots.txt", include_in_schema=False)
async def head_robots():
    return _head_response(152, "text/plain", "a6d4626541b6e8db")

@router.head("/favicon.svg", include_in_schema=False)
async def head_favicon_svg():
    return _head_response(1038, "image/svg+xml", "b729d0176f3e030b")

@router.head("/icons/icon-192.png", include_in_schema=False)
async def head_icon_192():
    return _head_response(7507, "image/png", "433934e66890920a")

@router.head("/icons/icon-512.png", include_in_schema=False)
async def head_icon_512():
    return _head_response(21218, "image/png", "925bd126dea7177a")

@router.head("/favicon.ico", include_in_schema=False)
async def head_favicon_ico():
    return _head_response(774, "image/x-icon", "113e6f0207a6d1e7")

@router.head("/apple-touch-icon.png", include_in_schema=False)
@router.head("/apple-touch-icon-precomposed.png", include_in_schema=False)
@router.head("/apple-touch-icon-120x120.png", include_in_schema=False)
@router.head("/apple-touch-icon-120x120-precomposed.png", include_in_schema=False)
async def head_apple_touch():
    return _head_response(12251, "image/png", "ec9ca45fa405bec8")

@router.head("/", include_in_schema=False)
@router.head("/index.html", include_in_schema=False)
@router.head("/devices.html", include_in_schema=False)
@router.head("/device.html", include_in_schema=False)
@router.head("/roms.html", include_in_schema=False)
@router.head("/recoveries.html", include_in_schema=False)
@router.head("/tools.html", include_in_schema=False)
@router.head("/android.html", include_in_schema=False)
@router.head("/guides.html", include_in_schema=False)
@router.head("/privacy.html", include_in_schema=False)
async def head_html_pages():
    """HEAD for HTML pages — return 200 with no body."""
    return Response(status_code=200, headers={"Content-Type": "text/html; charset=utf-8"})
