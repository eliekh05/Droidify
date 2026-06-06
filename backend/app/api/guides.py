"""
guides.py — API endpoints for flashing, rooting, and modding guides.
"""
import re
from fastapi import APIRouter, Query, HTTPException
from app.scrapers.guides import get_guides_for_device, get_all_guides

router = APIRouter()
_CODENAME_RE = re.compile(r"^[a-z0-9_-]{1,40}$")


@router.get("")
async def list_guides(
    guide_type: str | None = Query(None, description=(
        "Filter by type: bootloader-unlock | install-recovery | install-rom | "
        "root | restore | sell-buy"
    )),
):
    """Universal guides — all types."""
    data   = await get_all_guides()
    guides = data.get("guides", [])
    if guide_type:
        guides = [g for g in guides if g.get("guide_type") == guide_type]
    return {"total": len(guides), "guides": guides}


@router.get("/{codename}")
async def device_guides(codename: str, guide_type: str | None = Query(None)):
    """All guides for a specific device codename."""
    if not _CODENAME_RE.match(codename):
        raise HTTPException(status_code=400, detail="Invalid codename")
    guides = await get_guides_for_device(codename=codename)
    if not guides:
        raise HTTPException(status_code=404, detail=f"No guides found for '{codename}'")
    if guide_type:
        guides = [g for g in guides if g.get("guide_type") == guide_type]
        if not guides:
            raise HTTPException(status_code=404, detail=f"No '{guide_type}' guide for '{codename}'")
    return {"codename": codename, "total": len(guides), "guides": guides}
