import asyncio
from fastapi import APIRouter, Query, HTTPException
from app.scrapers.devices import get_devices, get_device_detail
from app.scrapers.roms import get_roms_for_device, LOS_BRANCH_TO_ANDROID
from app.scrapers.recoveries import get_recovery_for_device

router = APIRouter()


@router.get("")
async def list_devices(
    q:            str | None = Query(None, description="Search by model, codename, or manufacturer"),
    manufacturer: str | None = Query(None, description="Filter by manufacturer"),
    limit:        int        = Query(50, ge=1, le=200),
    offset:       int        = Query(0, ge=0),
):
    """
    Live device index from:
    - LineageOS Download API (281 codenames, active ROM branches)
    - LineageOS Wiki search.json (583 devices with model names)
    - OrangeFox API (159 devices with OEM/model info)
    - TWRP search.json (896 devices with manufacturer/codename)

    All merged and deduplicated. No auth required.
    """
    return await get_devices(q=q, manufacturer=manufacturer, limit=limit, offset=offset)


@router.get("/{codename}")
async def get_device(codename: str):
    """
    Full device detail including hardware specs (from LineageOS Wiki),
    available ROMs, and recovery options. All fetched live.
    """
    device, roms, recoveries = await asyncio.gather(
        get_device_detail(codename),
        get_roms_for_device(codename),
        get_recovery_for_device(codename),
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail=f"Device '{codename}' not found in LineageOS, OrangeFox, or TWRP indexes."
        )

    # Prepend LineageOS ROM entries from the device's branch info
    if device.get("has_lineageos"):
        los_roms = []
        for branch in device.get("lineageos_branches", []):
            android = LOS_BRANCH_TO_ANDROID.get(branch, "?")
            los_roms.append({
                "name":         "LineageOS",
                "slug":         "lineageos",
                "android_base": android,
                "version_label": branch,
                "maintainer":   "LineageOS team",
                "is_official":  True,
                "status":       "active",
                "rom_type":     "custom",
                "source_url":   f"https://wiki.lineageos.org/devices/{codename}/",
                "download_urls": [f"https://download.lineageos.org/devices/{codename}"],
                "source":       "lineageos_api",
                "description":  f"LineageOS {branch} (Android {android}). Official nightly builds.",
            })
        roms = los_roms + [r for r in roms if r["name"] != "LineageOS"]

    device["roms"]       = roms
    device["recoveries"] = recoveries
    device["rom_count"]  = len(roms)
    return device
