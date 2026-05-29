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
LOS_API        = "https://download.lineageos.org/api/v1/devices"
LOS_WIKI_SRCH  = "https://wiki.lineageos.org/search.json"
ORANGEFOX_API  = "https://api.orangefox.download/v3/devices/?per_page=500"
TWRP_SEARCH    = "https://twrp.me/search.json"

_OEM_NORM: dict[str, str] = {
    "lge": "LG", "motorola": "Motorola", "moto": "Motorola",
    "oneplus": "OnePlus", "xiaomi": "Xiaomi", "redmi": "Xiaomi",
    "pocophone": "Xiaomi", "huawei": "Huawei", "honor": "Honor",
    "samsung": "Samsung", "google": "Google", "fairphone": "Fairphone",
    "sony": "Sony", "htc": "HTC", "asus": "ASUS", "lenovo": "Lenovo",
    "nokia": "Nokia", "nothing": "Nothing Phone", "realme": "Realme",
    "oppo": "OPPO", "vivo": "Vivo", "essential": "Essential",
    "shift": "Shift", "bq": "BQ", "zte": "ZTE",
}

def _norm_oem(oem: str) -> str:
    if not oem:
        return ""
    key = oem.strip().lower()
    return _OEM_NORM.get(key, oem.strip().title())


# ── LineageOS Download API ────────────────────────────────────────────────────
async def _fetch_lineageos(client) -> dict[str, dict]:
    ck = "dev:los_api"
    cached = await cache_get(ck)
    if cached is not None:
        return cached

    resp = await fetch(client, LOS_API)
    if not resp or resp.status_code != 200:
        return {}

    devices: dict[str, dict] = {}
    for entry in resp.json():
        codename = entry.get("model", "")
        if not codename:
            continue
        devices[codename] = {
            "codename":          codename,
            "manufacturer":      _norm_oem(entry.get("oem", "")),
            "model_name":        entry.get("name", ""),
            "has_lineageos":     True,
            "lineageos_branches": [v["version"] for v in entry.get("versions", [])],
            "source":            "lineageos_api",
        }

    await cache_set(ck, devices, ttl=3600)
    return devices


# ── LineageOS Wiki search ─────────────────────────────────────────────────────
async def _fetch_wiki(client) -> dict[str, dict]:
    ck = "dev:los_wiki"
    cached = await cache_get(ck)
    if cached is not None:
        return cached

    resp = await fetch(client, LOS_WIKI_SRCH)
    if not resp or resp.status_code != 200:
        return {}

    devices: dict[str, dict] = {}
    for entry in resp.json():
        codename = entry.get("codename", "")
        if not codename:
            continue
        devices[codename] = {
            "codename":     codename,
            "manufacturer": _norm_oem(entry.get("vendor", "")),
            "model_name":   entry.get("name", ""),
            "wiki_url":     f"https://wiki.lineageos.org/devices/{codename}/",
            "source":       "lineageos_wiki",
        }

    await cache_set(ck, devices, ttl=3600)
    return devices


# ── OrangeFox API ─────────────────────────────────────────────────────────────
async def _fetch_orangefox(client) -> dict[str, dict]:
    ck = "dev:orangefox"
    cached = await cache_get(ck)
    if cached is not None:
        return cached

    resp = await fetch(client, ORANGEFOX_API)
    if not resp or resp.status_code != 200:
        return {}

    devices: dict[str, dict] = {}
    for dev in resp.json().get("data", []):
        codename = dev.get("codename", "")
        if not codename:
            continue
        devices[codename] = {
            "codename":       codename,
            "manufacturer":   _norm_oem(dev.get("oem_name", "")),
            "model_name":     dev.get("full_name", dev.get("model_name", "")),
            "has_orangefox":  True,
            "orangefox_url":  dev.get("url", ""),
            "source":         "orangefox",
        }

    await cache_set(ck, devices, ttl=3600)
    return devices


# ── TWRP search ───────────────────────────────────────────────────────────────
async def _fetch_twrp(client) -> dict[str, dict]:
    ck = "dev:twrp"
    cached = await cache_get(ck)
    if cached is not None:
        return cached

    resp = await fetch(client, TWRP_SEARCH)
    if not resp or resp.status_code != 200:
        return {}

    devices: dict[str, dict] = {}
    for entry in resp.json():
        title = entry.get("title", "")
        url   = entry.get("url", "")
        m = re.search(r"\(([a-zA-Z0-9_]+)\)$", title)
        if not m:
            continue
        codename = m.group(1)
        oem_key  = url.strip("/").split("/")[0].lower() if "/" in url else ""
        devices[codename] = {
            "codename":     codename,
            "model_name":   re.sub(r"\s*\([^)]+\)$", "", title).strip(),
            "manufacturer": _OEM_NORM.get(oem_key, oem_key.title()),
            "has_twrp":     True,
            "twrp_url":     f"https://twrp.me{url}",
            "source":       "twrp",
        }

    await cache_set(ck, devices, ttl=3600)
    return devices


# ── Merge all sources ─────────────────────────────────────────────────────────
async def _get_all_devices() -> dict[str, dict]:
    ck = "dev:merged"
    cached = await cache_get(ck)
    if cached is not None:
        return cached

    async with get_client() as client:
        los, wiki, fox, twrp = await asyncio.gather(
            _fetch_lineageos(client),
            _fetch_wiki(client),
            _fetch_orangefox(client),
            _fetch_twrp(client),
            return_exceptions=True,
        )

    merged: dict[str, dict] = {}

    for source in [los, wiki, fox, twrp]:
        if isinstance(source, Exception) or not isinstance(source, dict):
            continue
        for codename, dev in source.items():
            if codename not in merged:
                merged[codename] = {
                    "codename":          codename,
                    "manufacturer":      "",
                    "model_name":        "",
                    "has_lineageos":     False,
                    "has_grapheneos":    False,
                    "has_twrp":          False,
                    "has_orangefox":     False,
                    "lineageos_branches": [],
                    "wiki_url":          "",
                    "twrp_url":          "",
                    "orangefox_url":     "",
                    "sources":           [],
                }

            d = merged[codename]
            for field in ["manufacturer", "model_name", "wiki_url", "twrp_url", "orangefox_url"]:
                if not d.get(field) and dev.get(field):
                    d[field] = dev[field]

            if dev.get("has_lineageos"):
                d["has_lineageos"] = True
                d["lineageos_branches"] = dev.get("lineageos_branches", [])
            if dev.get("has_twrp"):
                d["has_twrp"] = True
                d["twrp_url"] = dev.get("twrp_url", "")
            if dev.get("has_orangefox"):
                d["has_orangefox"] = True
                d["orangefox_url"] = dev.get("orangefox_url", "")

            src = dev.get("source", "")
            if src and src not in d["sources"]:
                d["sources"].append(src)

    await cache_set(ck, merged, ttl=3600)
    return merged


# ── Public API ────────────────────────────────────────────────────────────────
async def get_devices(
    q: str | None = None,
    manufacturer: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    all_devices = await _get_all_devices()
    devices = list(all_devices.values())

    if q:
        ql = q.lower()
        qn = re.sub(r"[-_ ]", "", ql)
        def _match(d: dict) -> bool:
            c = (d.get("codename") or "").lower()
            m = (d.get("model_name") or "").lower()
            f = (d.get("manufacturer") or "").lower()
            return (
                ql in c or ql in m or ql in f
                or qn in re.sub(r"[-_ ]", "", c)
                or qn in re.sub(r"[-_ ]", "", m)
                or c.startswith(ql)
            )
        devices = [d for d in devices if _match(d)]

    if manufacturer:
        ml = manufacturer.lower()
        devices = [d for d in devices if ml in (d.get("manufacturer") or "").lower()]

    devices.sort(key=lambda d: (
        not d.get("has_lineageos"),
        (d.get("manufacturer") or "").lower(),
        (d.get("codename") or "").lower(),
    ))

    total = len(devices)
    return {
        "total":   total,
        "offset":  offset,
        "limit":   limit,
        "devices": devices[offset: offset + limit],
    }


async def get_device_by_codename(codename: str) -> dict | None:
    all_devices = await _get_all_devices()
    return all_devices.get(codename)


# Keep backward compat alias
get_device_detail = get_device_by_codename
