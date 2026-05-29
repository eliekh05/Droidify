"""Kali NetHunter scraper.

Source: https://nethunter.kali.org/device-kernels.html
Free, no auth. HTML table with 113 devices.
67 have pre-built images. hero2lte (Samsung Galaxy S7 Edge) has 4 kernels.

NetHunter is a mobile penetration testing platform built on top of
Android/LineageOS. It provides kernel-level network tools, HID attacks,
bad USB attacks, and Kali Linux tools in a chroot environment.
"""
import re
from bs4 import BeautifulSoup
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

NETHUNTER_URL   = "https://nethunter.kali.org/device-kernels.html"
NETHUNTER_DL    = "https://www.kali.org/get-kali/#kali-mobile"
NETHUNTER_DOCS  = "https://www.kali.org/docs/nethunter/"


async def get_nethunter_devices() -> list[dict]:
    ck = "nethunter_devices"
    cached = await cache_get(ck)
    if cached:
        return cached

    async with get_client() as client:
        resp = await fetch(client, NETHUNTER_URL)

    if not resp or resp.status_code != 200:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    devices: list[dict] = []

    for row in soup.find_all("tr")[1:]:
        cells = row.find_all("td")
        if not cells:
            continue

        full_name     = cells[0].get_text(strip=True)
        qty_images    = cells[1].get_text(strip=True) if len(cells) > 1 else "0"
        qty_kernels   = cells[2].get_text(strip=True) if len(cells) > 2 else "0"
        qty_versions  = cells[3].get_text(strip=True) if len(cells) > 3 else "0"

        # Extract codename from trailing parentheses: "Samsung Galaxy S7 Edge (hero2lte)"
        m = re.search(r"\(([a-zA-Z0-9_]+)\)\s*$", full_name)
        codename   = m.group(1) if m else ""
        model_name = re.sub(r"\s*\([^)]+\)\s*$", "", full_name).strip()

        if not codename:
            continue

        has_prebuilt = qty_images not in ("0", "")

        devices.append({
            "codename":        codename,
            "model_name":      model_name,
            "manufacturer":    _infer_manufacturer(model_name),
            "has_prebuilt":    has_prebuilt,
            "kernel_count":    qty_kernels,
            "kernel_versions": qty_versions,
            "source_url":      NETHUNTER_URL,
            "download_url":    NETHUNTER_DL if has_prebuilt else NETHUNTER_DOCS,
            "source":          "nethunter",
        })

    await cache_set(ck, devices, ttl=3600)
    return devices


async def check_nethunter_device(codename: str) -> dict | None:
    """Return Kali NetHunter ROM entry for a device codename."""
    ck = f"nethunter:{codename}"
    cached = await cache_get(ck)
    if cached is not None:
        return cached if cached else None

    devices = await get_nethunter_devices()
    match = next(
        (d for d in devices if d["codename"].lower() == codename.lower()), None
    )

    if not match:
        await cache_set(ck, {}, ttl=3600)
        return None

    result = {
        "name":          "Kali NetHunter",
        "slug":          "nethunter",
        "android_base":  None,
        "version_label": "Latest",
        "maintainer":    "Kali Linux / Offensive Security",
        "is_official":   True,
        "status":        "active",
        "rom_type":      "security",
        "source_url":    NETHUNTER_DOCS,
        "download_urls": [match["download_url"]],
        "source":        "nethunter",
        "description":   (
            f"Kali NetHunter for {match['model_name']}. "
            f"{match['kernel_count']} custom kernel(s) available. "
            + ("Pre-built image available. " if match["has_prebuilt"] else "Kernel-only, no pre-built image. ")
            + "Full Kali Linux toolset in a chroot. Requires LineageOS or AOSP base."
        ),
    }
    await cache_set(ck, result, ttl=3600)
    return result


def _infer_manufacturer(model_name: str) -> str:
    n = model_name.lower()
    for mfr, kws in {
        "Google":   ["nexus", "pixel"],
        "Samsung":  ["galaxy", "samsung"],
        "OnePlus":  ["oneplus"],
        "Xiaomi":   ["xiaomi", "poco", "redmi", "mi "],
        "Motorola": ["moto", "motorola"],
        "LG":       ["lg ", "nexus 5"],
        "Sony":     ["xperia"],
        "HTC":      ["htc"],
        "Asus":     ["asus", "zenfone"],
    }.items():
        if any(k in n for k in kws):
            return mfr
    return model_name.split()[0] if model_name else "Unknown"
