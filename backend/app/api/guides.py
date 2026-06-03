import re

_CODENAME_RE = re.compile(r"^[a-z0-9_-]{1,40}$")

"""
guides.py — API endpoints for flashing, rooting, and resale guides.
"""
from fastapi import APIRouter, Query, HTTPException
from app.scrapers.guides import get_guides_for_device, get_all_guides
from app.scrapers.resell_guides import get_resell_guides

router = APIRouter()

@router.get("")
async def list_guides(
    guide_type: str | None = Query(
        None,
        description=(
            "Filter by type: install | upgrade | root | bootloader-unlock | "
            "recovery | unbrick | buy | sell"
        ),
    ),
    manufacturer: str | None = Query(
        None,
        description="Filter buy/sell guides by manufacturer (Samsung, Xiaomi, Google…)",
    ),
):
    """Universal guides not tied to a specific device."""
    tech_guides = await get_all_guides()
    tech_list   = tech_guides.get("guides", [])

    resale = get_resell_guides(
        guide_type=guide_type if guide_type in ("buy", "sell") else None,
        manufacturer=manufacturer,
    )

    all_guides = tech_list + resale

    if guide_type and guide_type not in ("buy", "sell"):
        all_guides = [g for g in tech_list if g.get("guide_type") == guide_type]
    elif guide_type in ("buy", "sell"):
        all_guides = resale

    return {"total": len(all_guides), "guides": all_guides}

@router.get("/{codename}")
async def device_guides(
    codename: str,
    manufacturer: str | None = Query(
        None,
        description="Manufacturer name — improves guide accuracy",
    ),
    guide_type: str | None = Query(
        None,
        description=(
            "Filter by type: install | upgrade | root | bootloader-unlock | "
            "recovery | unbrick | buy | sell"
        ),
    ),
):
    """All guides for a specific device."""
    if not _CODENAME_RE.match(codename):
        raise HTTPException(status_code=400, detail="Invalid codename")
    device_specific = await get_guides_for_device(
        codename=codename,
        manufacturer=manufacturer,
    )

    resale = get_resell_guides(manufacturer=manufacturer)

    all_guides = device_specific + resale

    if not all_guides:
        raise HTTPException(
            status_code=404,
            detail=f"No guides found for '{codename}'",
        )

    if guide_type:
        all_guides = [g for g in all_guides if g.get("guide_type") == guide_type]
        if not all_guides:
            raise HTTPException(
                status_code=404,
                detail=f"No '{guide_type}' guide found for '{codename}'",
            )

    return {"codename": codename, "total": len(all_guides), "guides": all_guides}