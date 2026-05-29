"""Droidify — FastAPI backend (API only).

nginx serves the static frontend on port 80 and proxies /api/* here.
This process handles only /api/* routes — no static file serving.
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
            # Pre-warm new recovery sources
            from app.scrapers.recoveries import _fetch_pbrp, _fetch_shrp, get_recovery_for_device
            from app.services.http import get_client as _gc
            async with _gc() as _cl:
                await asyncio.gather(
                    _fetch_pbrp(_cl),
                    _fetch_shrp(_cl),
                    return_exceptions=True,
                )
            _log.warning("PBRP + SHRP recovery indexes warmed")
            _log.warning("Phase 2 warm complete")

            from app.scrapers.roms import _build_lookup
            await asyncio.gather(
                get_unofficialtwrp_devices(),
                _build_lookup(),
                return_exceptions=True,
            )
            _log.warning("Phase 3 warm complete — all caches hot")

        except Exception as e:
            _log.warning("Warmup error (non-fatal): %s", e)

    # Restore cache from disk (warms up from last run)
    from app.services.cache import load_from_disk, save_to_disk
    restored = load_from_disk()
    _log.warning("Cache restored: %d entries from disk", restored)

    asyncio.get_event_loop().create_task(_warm())
    yield

    # Save cache to disk on shutdown
    save_to_disk()
    _log.warning("Cache saved to disk on shutdown")


app = FastAPI(
    lifespan=lifespan,
    title="Droidify API",
    description="Live Android ecosystem indexer. No hardcoded data. No authentication required.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=False,
)

# CORS
_cors = [o.strip() for o in os.environ.get("CORS_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/api/health", tags=["meta"])
async def health():
    return {"status": "ok", "version": "2.0.0", "hardcoded_data": False, "auth_required": False}

app.include_router(devices_router,    prefix="/api/devices",          tags=["devices"])
app.include_router(android_router,    prefix="/api/android-versions", tags=["android"])
app.include_router(tools_router,      prefix="/api/tools",            tags=["tools"])
app.include_router(roms_router,       prefix="/api/roms",             tags=["roms"])
app.include_router(recoveries_router, prefix="/api/recoveries",       tags=["recoveries"])
app.include_router(guides_router,     prefix="/api/guides",           tags=["guides"])
