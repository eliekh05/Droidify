"""FastAPI application — startup, CORS, route registration, cache warm."""
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
from app.api.auth import router as auth_router
from app.api.not_read import router as not_read_router
from app.api.terms_api import router as terms_router

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

            await asyncio.gather(
                get_devices(limit=50), get_android_versions(), get_tools(),
                return_exceptions=True,
            )
            _log.warning("Phase 1 warm complete")

            await asyncio.gather(
                get_recoveries(limit=1), get_sourceforge_roms(), get_pixelexperience_roms(),
                return_exceptions=True,
            )
            _log.warning("Recovery indexes will warm on first request")
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
    from app.db import init_db
    await init_db()
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
    description="Live Android ROM, device and recovery indexer. No auth required. All endpoints are GET-only.",
    version="2.0.0",
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=None,
    redirect_slashes=False,
)

# CORS
_cors = [o.strip() for o in os.environ.get("CORS_ORIGINS", "https://eliekh05-droidify-hf.hf.space").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/api-reference", include_in_schema=False)
async def api_reference():
    """Human-readable styled API reference page."""
    import pathlib as _pl2
    from fastapi.responses import FileResponse as _FR2
    _static = _pl2.Path(
        os.environ.get("STATIC_DIR",
            str(_pl2.Path(__file__).parent.parent.parent / "frontend"))
    )
    return _FR2(str(_static / "openapi.html"))

@app.get("/docs", include_in_schema=False)
async def custom_docs():
    import pathlib as _pl
    from fastapi.responses import FileResponse as _FR
    _static2 = _pl.Path(
        os.environ.get("STATIC_DIR",
            str(_pl.Path(__file__).parent.parent.parent / "frontend"))
    )
    return _FR(str(_static2 / "docs.html"))

# Reject bodies over 64KB — this is a read-only API, no large payloads expected
@app.middleware("http")
async def limit_body_size(request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 65536:
        from fastapi.responses import JSONResponse
        return JSONResponse({"detail": "Request too large"}, status_code=413)
    return await call_next(request)

@app.get("/api/health", tags=["meta"])
async def health():
    return {"status": "ok", "version": "2.0.0", "hardcoded_data": False, "auth_required": False}

app.include_router(devices_router,    prefix="/api/devices",          tags=["devices"])
app.include_router(android_router,    prefix="/api/android-versions", tags=["android"])
app.include_router(tools_router,      prefix="/api/tools",            tags=["tools"])
app.include_router(roms_router,       prefix="/api/roms",             tags=["roms"])
app.include_router(recoveries_router, prefix="/api/recoveries",       tags=["recoveries"])
app.include_router(guides_router,     prefix="/api/guides",           tags=["guides"])
app.include_router(not_read_router, prefix="")
app.include_router(auth_router,       prefix="/api/auth",            tags=["auth"])
app.include_router(terms_router,      prefix="/api/terms",            tags=["auth"])
