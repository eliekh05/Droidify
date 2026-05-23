"""Droidify — FastAPI backend + embedded frontend.

Single process: serves REST API at /api/* and the entire frontend from
Python string literals embedded in app/frontend/assets.py and pages.py.

No filesystem reads at runtime — the /frontend directory is gone.
All data fetched live from free public sources — zero hardcoded content.
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.devices import router as devices_router
from app.api.android_versions import router as android_router
from app.api.tools import router as tools_router
from app.api.roms import router as roms_router
from app.api.recoveries import router as recoveries_router
from app.api.guides import router as guides_router
from app.frontend.router import router as frontend_router
from app.frontend import pages

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Warm critical caches on startup so first device page requests are fast."""
    _log = logging.getLogger("droidify.startup")

    async def _warm():
        """Pre-warm all caches on startup so first user request is instant.
        Runs concurrently in the background — never blocks startup."""
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

            # Phase 1: fast scrapers — devices, tools, android versions (< 2s)
            await asyncio.gather(
                get_devices(limit=50),
                get_android_versions(),
                get_tools(),
                return_exceptions=True,
            )
            _log.warning("Phase 1 warm complete (devices, tools, versions)")

            # Phase 2: recoveries + ROM sources (5-15s)
            await asyncio.gather(
                get_recoveries(limit=1),
                get_sourceforge_roms(),
                get_pixelexperience_roms(),
                return_exceptions=True,
            )
            _log.warning("Phase 2 warm complete (recoveries, SF, PE)")

            # Phase 3: heavy scrapers in background (uTWRP, full ROM index)
            await asyncio.gather(
                get_unofficialtwrp_devices(),
                get_all_roms(limit=1),
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
    description=(
        "Live Android ecosystem indexer. "
        "No hardcoded data — all fetched from free public sources. "
        "No authentication required."
    ),
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
        "frontend": "embedded",
    }


# ── API routers ───────────────────────────────────────────────────────────────
app.include_router(devices_router,    prefix="/api/devices",          tags=["devices"])
app.include_router(android_router,    prefix="/api/android-versions", tags=["android"])
app.include_router(tools_router,      prefix="/api/tools",            tags=["tools"])
app.include_router(roms_router,       prefix="/api/roms",             tags=["roms"])
app.include_router(recoveries_router, prefix="/api/recoveries",       tags=["recoveries"])
app.include_router(guides_router,     prefix="/api/guides",           tags=["guides"])


# ── Frontend router (embedded assets + HTML pages) ────────────────────────────
# Must be included AFTER all /api/* routers so API paths take priority.
app.include_router(frontend_router)

# ── Static files — CSS, JS, icons served directly from disk ──────────────────
# Must be mounted AFTER all explicit routes so /api/* routes take priority.
from pathlib import Path
from fastapi.staticfiles import StaticFiles as _SF
_static = Path(__file__).parent / "frontend" / "static"
app.mount("/css",    _SF(directory=str(_static / "css"),   html=False), name="css")
app.mount("/js",     _SF(directory=str(_static / "js"),    html=False), name="js")
app.mount("/icons",  _SF(directory=str(_static / "icons"), html=False), name="icons")


# ── 404 fallback — serve embedded 404 page ────────────────────────────────────
@app.exception_handler(StarletteHTTPException)
async def _http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return HTMLResponse(content=pages.page_404, status_code=404)
    # Re-raise everything else as a plain JSON error
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
