"""
Pixel Experience scraper
Source: GitHub raw JSON — 148 devices with brand/name/codename/versions
"""
import httpx
from ..services.cache import get as cache_get, set as cache_set

_URL = "https://raw.githubusercontent.com/PixelExperience/official_devices/master/devices.json"

_VER = {
    "eleven": "11", "twelve": "12", "twelve_plus": "12.1",
    "thirteen": "13", "thirteen_plus": "13.1",
    "fourteen": "14", "fourteen_plus": "14.1", "fifteen": "15",
}

async def get_pixelexperience_roms() -> list[dict]:
    ck = "roms:pixelexperience"
    if c := await cache_get(ck): return c

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(_URL)
            r.raise_for_status()
            raw = r.json()
    except Exception:
        return []

    results = []
    for dev in raw:
        codename = dev.get("codename", "")
        if not codename:
            continue
        brand = dev.get("brand", "")
        name  = dev.get("name", "")
        versions = [v for v in dev.get("supported_versions", []) if not v.get("deprecated", False)]
        if not versions:
            versions = dev.get("supported_versions", [])[-1:]

        latest = versions[-1] if versions else {}
        android = _VER.get(latest.get("version_code", ""), "14")

        results.append({
            "name":         f"{brand} {name}",
            "codename":     codename,
            "manufacturer": brand,
            "android_base": android,
            "rom_type":     "custom",
            "status":       "active",
            "official":     True,
            "maintainer":   "Pixel Experience Team",
            "source_url":   f"https://download.pixelexperience.org/{codename}",
            "download_url": f"https://download.pixelexperience.org/{codename}",
            "data_source":  "pixelexperience",
            "rom_name":     "Pixel Experience",
            "description":  "Stock Pixel UI experience on more devices",
        })

    await cache_set(ck, results, ttl=1800)
    return results
