"""UBports / Ubuntu Touch scraper.

Source: https://devices.ubuntu-touch.io/
Free, no auth. Device list extracted from data-* HTML attributes.
110 devices including Samsung Galaxy S7 Edge (hero2lte).
"""
import re
from bs4 import BeautifulSoup
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

UBPORTS_URL = "https://devices.ubuntu-touch.io/"

# Channel → display name
CHANNEL_NAMES = {
    "noble":  "Ubuntu 24.04 (Noble)",
    "focal":  "Ubuntu 20.04 (Focal)",
    "xenial": "Ubuntu 16.04 (Xenial)",
}


async def get_ubports_devices() -> list[dict]:
    ck = "ubports_devices"
    cached = await cache_get(ck)
    if cached:
        return cached

    async with get_client() as client:
        resp = await fetch(client, UBPORTS_URL)

    if not resp or resp.status_code != 200:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    devices: list[dict] = []

    for el in soup.find_all(attrs={"data-codename": True}):
        codename = el.get("data-codename", "").strip()
        name     = el.get("data-name", "").strip()
        channel  = el.get("data-release", "").strip()
        progress = el.get("data-progress", "").strip()
        if not codename:
            continue

        devices.append({
            "codename":       codename,
            "model_name":     name,
            "manufacturer":   _infer_manufacturer(name),
            "channel":        channel,
            "channel_name":   CHANNEL_NAMES.get(channel, channel),
            "progress_pct":   progress,
            "rom":            "Ubuntu Touch",
            "rom_slug":       "ubports",
            "source_url":     f"https://devices.ubuntu-touch.io/device/{codename}",
            "download_url":   f"https://devices.ubuntu-touch.io/device/{codename}",
            "source":         "ubports",
            "is_official":    True,
            "status":         "active",
            "description":    (
                f"Ubuntu Touch {CHANNEL_NAMES.get(channel, channel)} — "
                f"{progress}% feature complete. Privacy-focused Linux phone OS."
            ),
        })

    await cache_set(ck, devices, ttl=3600)
    return devices


async def check_ubports_device(codename: str) -> dict | None:
    """Return UBports ROM entry for a specific device codename."""
    ck = f"ubports:{codename}"
    cached = await cache_get(ck)
    if cached is not None:
        return cached if cached else None

    devices = await get_ubports_devices()
    match = next((d for d in devices if d["codename"].lower() == codename.lower()), None)

    if not match:
        await cache_set(ck, {}, ttl=3600)
        return None

    result = {
        "name":          "Ubuntu Touch (UBports)",
        "slug":          "ubports",
        "android_base":  None,
        "version_label": match["channel_name"],
        "maintainer":    "UBports Foundation",
        "is_official":   True,
        "status":        "active",
        "rom_type":      "linux",
        "source_url":    match["source_url"],
        "download_urls": [match["download_url"]],
        "source":        "ubports",
        "description":   match["description"],
    }
    await cache_set(ck, result, ttl=3600)
    return result


def _infer_manufacturer(name: str) -> str:
    n = name.lower()
    for mfr, keywords in {
        "Google":    ["nexus", "pixel"],
        "Samsung":   ["galaxy", "samsung"],
        "OnePlus":   ["oneplus"],
        "Xiaomi":    ["xiaomi", "poco", "redmi", "mi "],
        "Fairphone": ["fairphone"],
        "BQ":        ["bq "],
        "Meizu":     ["meizu"],
        "Sony":      ["xperia", "sony"],
        "Lenovo":    ["lenovo"],
        "JingLing":  ["jingpad"],
        "Pine64":    ["pinephone", "pinetab"],
        "Volla":     ["volla"],
        "Shift":     ["shift"],
    }.items():
        if any(k in n for k in keywords):
            return mfr
    return name.split()[0] if name else "Unknown"
