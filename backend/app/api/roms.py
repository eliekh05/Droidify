import re
from fastapi import APIRouter, HTTPException, Query
from app.scrapers.roms import get_all_roms

router = APIRouter()


@router.get("")
async def list_roms(
    q:            str | None = Query(None, description="Search by name or codename"),
    android_base: str | None = Query(None, description="Filter by Android version, e.g. '16'"),
    rom_type:     str | None = Query(None, description="custom | stock | gsi"),
    limit:        int = Query(100, ge=1, le=500),
    offset:       int = Query(0, ge=0),
):
    """
    ROM index across all supported devices.
    Data fetched live from LineageOS Download API and GrapheneOS releases.
    LineageOS: 281 devices. GrapheneOS: 14 Pixel devices.
    """
    return await get_all_roms(
        q=q,
        rom_type=rom_type,
        android_base=android_base,
        limit=limit,
        offset=offset,
    )
