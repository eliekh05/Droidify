"""
Replicant scraper — fully free Android for old Samsung Galaxy devices
Source: https://replicant.us/supported-devices.php
"""
import re
import httpx
from bs4 import BeautifulSoup
from ..services.cache import get as cache_get, set as cache_set

_URL = "https://replicant.us/supported-devices.php"

# Device name → codename map for Replicant (fixed historical project, Android 6 era)
# Replicant uses Samsung display names; this translates them to Android codenames
_CODENAMES = {
    "Galaxy S 2": "i9100", "Galaxy Note": "n7000", "Galaxy Nexus": "maguro",
    "Galaxy S 3": "i9300", "Galaxy Note 2": "n7100", "Galaxy Note 8.0": "n5100",
    "Galaxy Tab 2 7.0": "p3100", "Galaxy Tab 2 10.1": "p5100",
    "Galaxy S 3 4G": "i9305", "Galaxy S": "i9000", "Galaxy S Plus": "i9001",
    "Galaxy Ace": "s5830",
}

async def get_replicant_roms() -> list[dict]:
    ck = "roms:replicant"
    if c := await cache_get(ck): return c

    try:
        async with httpx.AsyncClient(timeout=15, headers={"User-Agent": "Mozilla/5.0"}) as client:
            r = await client.get(_URL)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
    except Exception:
        return []

    text = soup.get_text(separator=" ")
    devices = re.findall(r"Galaxy [A-Z][a-zA-Z0-9 \.]+", text)
    seen, results = set(), []

    for dev in devices:
        dev = dev.strip()
        if dev in seen or len(dev) < 8:
            continue
        seen.add(dev)
        codename = _CODENAMES.get(dev, dev.lower().replace(" ", "_"))
        results.append({
            "name":         f"Samsung {dev}",
            "codename":     codename,
            "manufacturer": "Samsung",
            "android_base": "6",  # Replicant targets Android 6.0 AOSP — historically immutable
            "rom_type":     "custom",
            "status":       "active",
            "official":     True,
            "maintainer":   "Replicant Project",
            "source_url":   "https://replicant.us/supported-devices.php",
            "download_url": None,  # Replicant has no direct per-device download — use source_url
            "data_source":  "replicant",
            "rom_name":     "Replicant",
            "description":  "Fully free software Android — no proprietary blobs",
        })

    await cache_set(ck, results, ttl=7200)
    return results
