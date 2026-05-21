"""Droidify — FastAPI backend + frontend server.

Single process: serves REST API at /api/* and static frontend files at /.
All data fetched live from free public sources — zero hardcoded content.
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.devices import router as devices_router
from app.api.android_versions import router as android_router
from app.api.tools import router as tools_router
from app.api.roms import router as roms_router
from app.api.recoveries import router as recoveries_router
from app.api.guides import router as guides_router

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Frontend directory — set via FRONTEND_DIR env var or auto-detect
_FRONTEND = Path(
    os.environ.get("FRONTEND_DIR", str(Path(__file__).parent.parent.parent / "frontend"))
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Warm critical caches on startup so first device page requests are fast."""
    async def _warm():
        try:
            from app.scrapers.sourceforge_roms import get_sourceforge_roms
            from app.scrapers.unofficialtwrp import get_unofficialtwrp_devices
            from app.scrapers.pixelexperience import get_pixelexperience_roms
            await asyncio.gather(
                get_sourceforge_roms(),
                get_pixelexperience_roms(),
                get_unofficialtwrp_devices(),
                return_exceptions=True,
            )
        except Exception:
            pass

    # Fire cache warming in background — works with single or multi-worker
    try:
        asyncio.get_event_loop().create_task(_warm())
    except RuntimeError:
        pass  # no running loop yet — cache warms on first request
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Droidify API",
    description=(
        "Live Android ecosystem indexer. "
        "No hardcoded data — all fetched from free public sources. "
        "No authentication required."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
_cors_origins = [o.strip() for o in os.environ.get("CORS_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["meta"])
async def health():
    return {
        "status": "ok",
        "version": "2.0.0",
        "hardcoded_data": False,
        "auth_required": False,
    }


# ── API routers ───────────────────────────────────────────────────────────────
app.include_router(devices_router,    prefix="/api/devices",          tags=["devices"])
app.include_router(android_router,    prefix="/api/android-versions", tags=["android"])
app.include_router(tools_router,      prefix="/api/tools",            tags=["tools"])
app.include_router(roms_router,       prefix="/api/roms",             tags=["roms"])
app.include_router(recoveries_router, prefix="/api/recoveries",       tags=["recoveries"])
app.include_router(guides_router,     prefix="/api/guides",           tags=["guides"])


# ── Frontend static files ─────────────────────────────────────────────────────
# FastAPI serves the SPA directly — no nginx needed.
# Clean URL mapping: /devices → devices.html, etc.
_frontend = str(_FRONTEND)

if _FRONTEND.is_dir():
    _clean_routes = {
        "/":           "index.html",
        "/devices":    "devices.html",
        "/roms":       "roms.html",
        "/recoveries": "recoveries.html",
        "/tools":      "tools.html",
        "/android":    "android.html",
        "/guides":     "guides.html",
    }

    for _path, _file in _clean_routes.items():
        _abs = os.path.join(_frontend, _file)
        if os.path.exists(_abs):
            def _make(p):
                async def _h():
                    return FileResponse(p, media_type="text/html")
                return _h
            app.get(_path, include_in_schema=False)(_make(_abs))

    @app.exception_handler(StarletteHTTPException)
    async def _404(request, exc):
        if exc.status_code == 404:
            p = os.path.join(_frontend, "404.html")
            if os.path.exists(p):
                return FileResponse(p, status_code=404, media_type="text/html")
        raise exc

    # Mount static assets (CSS, JS, icons, manifest, sw.js, robots.txt)
    app.mount("/", StaticFiles(directory=_frontend, html=True), name="frontend")
