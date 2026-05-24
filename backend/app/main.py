"""Droidify — FastAPI backend + Svelte frontend.

Single process: serves REST API at /api/* and the Svelte SPA at /*.
Frontend built with Vite during Docker build — output copied to app/frontend/static/.
All data fetched live from free public sources — zero hardcoded content.
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
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

# Docker copies Vite build output here: frontend/dist/ -> /home/user/app/frontend/static/
STATIC = Path(__file__).parent / "frontend" / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    _log = logging.getLogger("droidify.startup")

    async def _warm():
        _log.warning("Warming caches...")
        try:
            from app.scrapers.devices import get_devices
            from app.scrapers.android_versions import get_android_versions
            from app.scrapers.tools import get_tools
            from app.scrapers.recoveries import get_recoveries
            from app.scrapers.sourceforge_roms import get_sourceforge_roms
            from app.scrapers.pixelexperience import get_pixelexperience_roms
            from app.scrapers.unofficialtwrp import get_unofficialtwrp_devices
            from app.scrapers.roms import get_all_roms

            await asyncio.gather(
                get_devices(limit=50), get_android_versions(), get_tools(),
                return_exceptions=True,
            )
            _log.warning("Phase 1 warm complete")

            await asyncio.gather(
                get_recoveries(limit=1), get_sourceforge_roms(), get_pixelexperience_roms(),
                return_exceptions=True,
            )
            _log.warning("Phase 2 warm complete")

            await asyncio.gather(
                get_unofficialtwrp_devices(), get_all_roms(limit=1),
                return_exceptions=True,
            )
            _log.warning("Phase 3 warm complete — all caches hot")

        except Exception as e:
            _log.warning("Warmup error (non-fatal): %s", e)

    asyncio.get_event_loop().create_task(_warm())
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Droidify API",
    description="Live Android ecosystem indexer. No hardcoded data. No authentication required.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
_cors_origins = [
    o.strip() for o in os.environ.get("CORS_ORIGINS", "*").split(",") if o.strip()
]
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
        "frontend": "svelte",
    }

# ── API routers ───────────────────────────────────────────────────────────────
app.include_router(devices_router,    prefix="/api/devices",          tags=["devices"])
app.include_router(android_router,    prefix="/api/android-versions", tags=["android"])
app.include_router(tools_router,      prefix="/api/tools",            tags=["tools"])
app.include_router(roms_router,       prefix="/api/roms",             tags=["roms"])
app.include_router(recoveries_router, prefix="/api/recoveries",       tags=["recoveries"])
app.include_router(guides_router,     prefix="/api/guides",           tags=["guides"])

# ── SW — no-cache header ─────────────────────────────────────────────────────
@app.get("/sw.js", include_in_schema=False)
async def sw():
    return FileResponse(STATIC / "sw.js", headers={"Cache-Control": "no-store"})

# ── SPA + static file handler ─────────────────────────────────────────────────
# Serves real files from STATIC dir, falls back to index.html for SPA routes.
# No StaticFiles mount — avoids 404 conflicts with catch-all route.
@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str, request: Request):
    if full_path.startswith("api/"):
        return JSONResponse(status_code=404, content={"detail": "Not found"})

    file_path = STATIC / full_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)

    index = STATIC / "index.html"
    if index.exists():
        return FileResponse(index)

    return JSONResponse(status_code=503, content={"detail": "Frontend not built"})

# ── Exception handler ─────────────────────────────────────────────────────────
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404 and not request.url.path.startswith("/api/"):
        index = STATIC / "index.html"
        if index.exists():
            return FileResponse(index)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
