"""Live device scraper — fetches from free public sources only.

Sources (no auth, no payment required):
  1. LineageOS Download API  — 281 codenames, branch info, download URLs
  2. LineageOS Wiki search.json — device model names + manufacturer
  3. LineageOS Wiki device page  — SoC, RAM, CPU, release date (parsed from HTML)
  4. OrangeFox API           — 159 devices with OEM, model, recovery support
  5. TWRP search.json        — 896 devices for recovery cross-reference
"""
import asyncio
import re
from typing import Any

from bs4 import BeautifulSoup

from app.services.cache import cache_key, get as cache_get, set as cache_set
from app.services.http import fetch, get_client

# ── Source URLs ───────────────────────────────────────────────────────────────
LOS_DEVICES_API    = "https://download.lineageos.org/api/v1/devices"
LOS_WIKI_SEARCH    = "https://wiki.lineageos.org/search.json"
LOS_WIKI_DEVICE    = "https://wiki.lineageos.org/devices/{codename}/"
LOS_DOWNLOAD       = "https://download.lineageos.org/devices/{codename}"
ORANGEFOX_API      = "https://api.orangefox.download/v3/devices/?per_page=500"
TWRP_SEARCH        = "https://twrp.me/search.json"

# Regex to strip HTML tags
_TAG_RE = re.compile(r"<[^>]+>")


def _clean(text: str) -> str:
    return _TAG_RE.sub("", text).strip()


# ── Primary: LineageOS Download API ───────────────────────────────────────────
async def _fetch_los_devices(client) -> dict[str, dict]:
    """Returns {codename: {branches: [...], download_url: ...}}"""
    ck = "los_devices_api"
    cached = await cache_get(ck)
    if cached:
        return cached

    resp = await fetch(client, LOS_DEVICES_API)
    if not resp or resp.status_code != 200:
        return {}

    data = resp.json()  # {branch: [codename, ...]}
    result: dict[str, dict] = {}
    for branch, codenames in data.items():
        for codename in codenames:
            if codename not in result:
                result[codename] = {"codename": codename, "branches": [], "download_urls": []}
            result[codename]["branches"].append(branch)
            result[codename]["download_urls"].append(
                LOS_DOWNLOAD.format(codename=codename)
            )

    await cache_set(ck, result, ttl=600)
    return result


# ── LineageOS Wiki — device model/name mapping ────────────────────────────────
async def _fetch_los_wiki_names(client) -> dict[str, dict]:
    """Returns {codename: {model_name, manufacturer}} from wiki search.json"""
    ck = "los_wiki_names"
    cached = await cache_get(ck)
    if cached:
        return cached

    resp = await fetch(client, LOS_WIKI_SEARCH)
    if not resp or resp.status_code != 200:
        return {}

    result: dict[str, dict] = {}
    for entry in resp.json():
        url = entry.get("url", "")
        # URL format: /devices/CODENAME/
        if not url.startswith("/devices/"):
            continue
        parts = url.strip("/").split("/")
        if len(parts) < 2:
            continue
        codename = parts[1]
        title = entry.get("title", "")  # "panther - Google Pixel 7"
        if " - " in title:
            _, model_name = title.split(" - ", 1)
        elif title:
            model_name = title
        else:
            model_name = ""
        # Try to infer manufacturer from model name
        manufacturer = _infer_manufacturer(model_name)
        result[codename] = {
            "codename": codename,
            "model_name": model_name.strip(),
            "manufacturer": manufacturer,
            "wiki_url": f"https://wiki.lineageos.org/devices/{codename}/",
        }

    await cache_set(ck, result, ttl=600)
    return result


def _infer_manufacturer(model_name: str) -> str:
    """Infer manufacturer from device model name."""
    m = model_name.lower()
    for mfr, keywords in {
        "Google": ["pixel", "nexus", "android one"],
        "Samsung": ["galaxy", "samsung"],
        "OnePlus": ["oneplus"],
        "Xiaomi": ["xiaomi", "poco", "redmi", "mi "],
        "Motorola": ["moto", "motorola"],
        "Nokia": ["nokia"],
        "Sony": ["xperia", "sony"],
        "Fairphone": ["fairphone"],
        "Asus": ["asus", "zenfone", "rog phone"],
        "LG": ["lg ", " lg"],
        "HTC": ["htc"],
        "Huawei": ["huawei", "honor"],
        "OPPO": ["oppo", "find x", "reno"],
        "Realme": ["realme"],
        "Vivo": ["vivo"],
        "Nothing": ["nothing phone"],
        "Lenovo": ["lenovo"],
        "BQ": ["bq "],
        "Yandex": ["yandex"],
        "Shift": ["shift"],
        "Essential": ["essential"],
    }.items():
        if any(k in m for k in keywords):
            return mfr
    # Title-case first word as fallback
    first = model_name.split()[0] if model_name else ""
    return first if first else "Unknown"


# ── LineageOS Wiki device page — hardware specs ───────────────────────────────
async def _fetch_los_wiki_specs(client, codename: str) -> dict:
    """Scrape SoC, RAM, CPU, release date from LineageOS wiki device page."""
    ck = cache_key("los_wiki_specs", codename)
    cached = await cache_get(ck)
    if cached is not None:
        return cached

    url = LOS_WIKI_DEVICE.format(codename=codename)
    resp = await fetch(client, url)
    if not resp or resp.status_code != 200:
        await cache_set(ck, {}, ttl=3600)
        return {}

    soup = BeautifulSoup(resp.text, "lxml")
    specs: dict[str, str] = {}

    # LineageOS wiki uses a <table> with <tr> rows: key cell + value cell
    for row in soup.find_all("tr"):
        cells = row.find_all(["td", "th"])
        if len(cells) >= 2:
            key = _clean(cells[0].get_text()).rstrip(":")
            val = _clean(cells[1].get_text())
            if key and val:
                specs[key] = val

    # Normalise keys
    result = {
        "soc": specs.get("SoC", specs.get("Chipset", "")),
        "ram": specs.get("RAM", ""),
        "cpu": specs.get("CPU", ""),
        "gpu": specs.get("GPU", ""),
        "released": specs.get("Released", ""),
        "architecture": specs.get("Architecture", ""),
        "wiki_url": url,
    }
    # Extract release year
    year_match = re.search(r"\b(20\d{2})\b", result.get("released", ""))
    result["release_year"] = int(year_match.group(1)) if year_match else None

    await cache_set(ck, result, ttl=3600)
    return result


# ── OrangeFox API ─────────────────────────────────────────────────────────────
async def _fetch_orangefox_devices(client) -> dict[str, dict]:
    """Returns {codename: {oem, model, full_name, orangefox_url}}"""
    ck = "orangefox_devices"
    cached = await cache_get(ck)
    if cached:
        return cached

    resp = await fetch(client, ORANGEFOX_API)
    if not resp or resp.status_code != 200:
        return {}

    result: dict[str, dict] = {}
    for dev in resp.json().get("data", []):
        codename = dev.get("codename", "")
        if not codename:
            continue
        result[codename] = {
            "codename": codename,
            "manufacturer": dev.get("oem_name", ""),
            "model_name": dev.get("full_name", dev.get("model_name", "")),
            "orangefox_url": dev.get("url", ""),
            "orangefox_supported": dev.get("supported", True),
        }
        # Also register alternate codenames
        for alt in dev.get("codenames", []):
            if alt and alt != codename:
                result[alt] = result[codename]

    await cache_set(ck, result, ttl=600)
    return result


# ── TWRP search.json ──────────────────────────────────────────────────────────
async def _fetch_twrp_devices(client) -> dict[str, dict]:
    """Returns {codename: {title, manufacturer, twrp_url}}"""
    ck = "twrp_devices"
    cached = await cache_get(ck)
    if cached:
        return cached

    resp = await fetch(client, TWRP_SEARCH)
    if not resp or resp.status_code != 200:
        return {}

    result: dict[str, dict] = {}
    for entry in resp.json():
        title = entry.get("title", "")  # "Google Pixel 7 (panther)"
        url   = entry.get("url", "")    # "/google/googlepixel7.html"

        # Extract codename from parentheses
        code_match = re.search(r"\(([a-zA-Z0-9_]+)\)$", title)
        if not code_match:
            continue
        codename = code_match.group(1)

        # Extract manufacturer from URL path: /google/...
        url_parts = url.strip("/").split("/")
        manufacturer = url_parts[0].title() if url_parts else ""
        # Fix common ones
        mfr_map = {
            "Lg": "LG", "Htc": "HTC", "Bq": "BQ",
            "Oneplus": "OnePlus", "Asus": "ASUS",
        }
        manufacturer = mfr_map.get(manufacturer, manufacturer)

        result[codename] = {
            "codename": codename,
            "model_name": re.sub(r"\s*\([^)]+\)$", "", title).strip(),
            "manufacturer": manufacturer,
            "twrp_url": f"https://twrp.me{url}",
        }

    await cache_set(ck, result, ttl=600)
    return result


# ── Merge all sources into unified device list ────────────────────────────────
async def get_devices(
    q: str | None = None,
    manufacturer: str | None = None,
    limit: int = 50,
    offset: int = 0,
    codename: str | None = None,
) -> list[dict]:
    """Fetch and merge devices from all free sources."""
    async with get_client() as client:
        los_devices, los_names, orangefox, twrp = await asyncio.gather(
            _fetch_los_devices(client),
            _fetch_los_wiki_names(client),
            _fetch_orangefox_devices(client),
            _fetch_twrp_devices(client),
        )

    # Merge: start with LineageOS (281 devices), enrich with other sources
    all_codenames: set[str] = set(los_devices.keys())
    # Add OrangeFox-only and TWRP-only devices
    all_codenames |= set(orangefox.keys())
    all_codenames |= set(twrp.keys())

    devices: list[dict] = []
    for cn in sorted(all_codenames):
        los   = los_devices.get(cn, {})
        wiki  = los_names.get(cn, {})
        fox   = orangefox.get(cn, {})
        tw    = twrp.get(cn, {})

        # Prefer: wiki > twrp > orangefox for name/manufacturer
        model = (
            wiki.get("model_name")
            or tw.get("model_name")
            or fox.get("model_name")
            or cn
        )
        mfr = (
            wiki.get("manufacturer")
            or tw.get("manufacturer")
            or fox.get("manufacturer")
            or _infer_manufacturer(model)
        )

        device: dict[str, Any] = {
            "codename":       cn,
            "model_name":     model,
            "manufacturer":   mfr,
            "lineageos_branches": los.get("branches", []),
            "lineageos_download_url": (
                LOS_DOWNLOAD.format(codename=cn) if los else None
            ),
            "wiki_url": wiki.get("wiki_url"),
            "twrp_url": tw.get("twrp_url"),
            "orangefox_url": fox.get("orangefox_url"),
            "orangefox_supported": fox.get("orangefox_supported"),
            "has_lineageos": bool(los),
            "has_twrp":      bool(tw),
            "has_orangefox": bool(fox),
            "sources": list({
                s for s, v in [("lineageos", los), ("orangefox", fox), ("twrp", tw)]
                if v
            }),
        }
        devices.append(device)

    # Filter
    if codename:
        devices = [d for d in devices if d["codename"].lower() == codename.lower()]
    if q:
        q_lower = q.lower()
        # Normalise: strip hyphens/spaces so "j701f" matches "SM-J701F" and vice versa
        q_norm = re.sub('[-_ ]', '', q_lower)
        devices = [
            d for d in devices
            if q_lower in (d["codename"] or "").lower()
            or q_lower in (d["model_name"] or "").lower()
            or q_lower in (d["manufacturer"] or "").lower()
            or q_norm in re.sub('[-_ ]', '', (d["model_name"] or "").lower())
            or q_norm in re.sub('[-_ ]', '', (d["codename"] or "").lower())
            or (d["codename"] or "").lower().startswith(q_lower)
        ]
    if manufacturer:
        mfr_lower = manufacturer.lower()
        devices = [
            d for d in devices
            if mfr_lower in d["manufacturer"].lower()
        ]

    total = len(devices)
    page  = devices[offset : offset + limit]
    return {"total": total, "offset": offset, "limit": limit, "devices": page}


async def get_device_detail(codename: str) -> dict | None:
    """Get full detail for a single device including wiki specs."""
    result = await get_devices(codename=codename, limit=1, offset=0)
    devices = result.get("devices", [])
    if not devices:
        return None

    device = devices[0]

    # Fetch wiki specs (SoC, RAM, etc.)
    async with get_client() as client:
        specs = await _fetch_los_wiki_specs(client, codename)

    device.update({
        "soc":          specs.get("soc", ""),
        "ram":          specs.get("ram", ""),
        "cpu":          specs.get("cpu", ""),
        "gpu":          specs.get("gpu", ""),
        "release_year": specs.get("release_year"),
        "architecture": specs.get("architecture", ""),
        "released":     specs.get("released", ""),
    })
    return device
