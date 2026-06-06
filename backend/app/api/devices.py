import asyncio
import re

_CODENAME_RE = re.compile(r'^[a-z0-9_-]{1,40}$')
from fastapi import APIRouter, Query, HTTPException
from app.scrapers.devices import get_devices, get_device_detail
from app.scrapers.roms import get_roms_for_device, LOS_BRANCH_TO_ANDROID
from app.scrapers.recoveries import get_recovery_for_device
from app.scrapers.samfw import get_samfw_for_device

router = APIRouter()

# Only allow safe characters in search — codename/model chars only
_SAFE_Q  = re.compile(r"[^a-zA-Z0-9 _.+\-]")
_SAFE_CN = re.compile(r"[^a-zA-Z0-9_\-]")

@router.get("")
async def list_devices(
    q:            str | None = Query(None, min_length=1, max_length=64,  description="Search by model, codename, or manufacturer"),
    manufacturer: str | None = Query(None, min_length=1, max_length=64,  description="Filter by manufacturer"),
    limit:        int        = Query(50,   ge=1, le=50),
    offset:       int        = Query(0,    ge=0),
):
    # Strip any character that has no business being in a device search
    if q:            q            = _SAFE_Q.sub("", q).strip()[:64]  or None
    if manufacturer: manufacturer = _SAFE_Q.sub("", manufacturer).strip()[:64] or None
    """
    Live device index from:
    - LineageOS Download API (281 codenames, active ROM branches)
    - LineageOS Wiki search.json (583 devices with model names)
    - OrangeFox API (159 devices with OEM/model info)
    - TWRP search.json (896 devices with manufacturer/codename)

    All merged and deduplicated. No auth required.
    """
    result = await get_devices(q=q, manufacturer=manufacturer, limit=limit, offset=offset)

    # Enrich devices with rom_count from pre-built lookup table (O(1) per device)
    try:
        from app.scrapers.roms import _build_lookup
        import re as _re
        lookup = await _build_lookup()
        for d in result["devices"]:
            cn_n = _re.sub(r'[-_ .]', '', (d.get("codename") or "").lower())
            los_c = len(d.get("lineageos_branches", [])) if d.get("has_lineageos") else 0
            d["rom_count"] = los_c + len(lookup.get(cn_n, []))
    except Exception:
        raise

    return result

@router.get("/{codename}")
async def get_device(codename: str):
    # Codenames are alphanumeric + underscore/hyphen only — reject anything else
    if not re.fullmatch(r"[a-zA-Z0-9_\-]{1,64}", codename):
        raise HTTPException(status_code=400, detail="Invalid codename.")
    """
    Full device detail including hardware specs (from LineageOS Wiki),
    available ROMs, and recovery options. All fetched live.
    """
    device, roms, recoveries, samfw = await asyncio.gather(
        get_device_detail(codename),
        get_roms_for_device(codename),
        get_recovery_for_device(codename),
        get_samfw_for_device(codename),
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
    device["stock_firmware"] = samfw if not isinstance(samfw, Exception) else []
    device["rom_count"]  = len(roms)
    return device
