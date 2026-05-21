import re
from fastapi import APIRouter, Query, HTTPException
from app.scrapers.guides import get_guides_for_device, get_all_guides

router = APIRouter()


@router.get("")
async def list_guides(
    guide_type: str | None = Query(
        None,
        description="Filter by type: install | upgrade | root | backup | bootloader-unlock | recovery | unbrick"
    ),
):
    """
    Universal guides not tied to a specific device.
    Includes root guides (Magisk, KernelSU), backup guide, and general bootloader unlock.
    """
    guides = await get_all_guides()
    if guide_type:
        guides = [g for g in guides if g["type"] == guide_type]
    return {"total": len(guides), "guides": guides}


@router.get("/{codename}")
async def device_guides(
    codename: str,
    manufacturer: str | None = Query(None, description="Manufacturer name (improves guide accuracy)"),
    guide_type: str | None = Query(None, description="Filter by guide type"),
):
    """
    All guides for a specific device — install ROM, unlock bootloader,
    root, backup, install recovery, and unbrick.

    Sources: LineageOS Wiki (live), GrapheneOS docs, Magisk docs, KernelSU docs,
    compiled OEM/XDA documentation.
    """
    guides = await get_guides_for_device(codename=codename, manufacturer=manufacturer)
    if not guides:
        raise HTTPException(status_code=404, detail=f"No guides found for '{codename}'")
    if guide_type:
        guides = [g for g in guides if g["type"] == guide_type]
        if not guides:
            raise HTTPException(
                status_code=404,
                detail=f"No '{guide_type}' guide found for '{codename}'"
            )
    return {"codename": codename, "total": len(guides), "guides": guides}
