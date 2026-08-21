"""Live device scraper — LineageOS API and Wiki, OrangeFox, TWRP."""
import asyncio
import re

from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

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


# Codename alias map — maps TWRP model numbers to LineageOS/ROM community codenames
# TWRP uses manufacturer model numbers; ROM projects use community codenames
# This map lets ROMs and recoveries match across the same device
# Automatically bidirectional — if A maps to B, B also maps to A
_CODENAME_ALIASES_RAW: dict[str, str] = {
    # ── ASUS ──────────────────────────────────────────────────────────────────
    "I002D":   "sake",        # ZenFone 8 (2021)
    "I004D":   "vodka",       # ZenFone 8 Flip (2021)
    "AI2202":  "sake2",       # ZenFone 9 (2022)
    "AI2302":  "davinci",     # ZenFone 10 (2023)
    "AI2401":  "asus_AI2401", # ZenFone 11 Ultra (2024)
    "I003D":   "obiwan",      # ROG Phone 3 (2020)
    "I005D":   "asus_I005D",  # ROG Phone 5 (2021)
    "AI2201":  "asus_AI2201", # ROG Phone 6 (2022)
    "AI2203":  "asus_AI2203", # ROG Phone 6D (2022)
    "AI2301":  "asus_AI2301", # ROG Phone 7 (2023)
    "ZS620KL": "Z01R",        # ZenFone 5Z (2018)
    "ZS630KL": "I01WD",       # ZenFone 6 (2019)
    "ZS670KS": "asus_I002D",  # ZenFone 7 (2020)
    "ZS671KS": "asus_I002D",  # ZenFone 7 Pro (2020)
    "X00TD":   "X00TD",       # ZenFone Max Pro M1
    "X01BD":   "X01BD",       # ZenFone Max Pro M2
    # ── Alcatel ───────────────────────────────────────────────────────────────
    "4060O":   "pop3_5",      # Alcatel Pop 3 5"
    "5085A":   "a571vl",      # Alcatel Verso / Jitterbug Smart2
    "5059A":   "5059A",       # Alcatel 1X
    "5002F":   "5002F",       # Alcatel 1
    "5033A":   "5033A",       # Alcatel 3
    # ── Amazon ────────────────────────────────────────────────────────────────
    "KFASWI":  "suez",        # Fire HD 10 (2021)
    "KFTRWI":  "mustang",     # Fire HD 10 (2019)
    "KFMAWI":  "maverick",    # Fire HD 10 (2017)
    "KFFOWI":  "ford",        # Fire HD 6/7 (2014)
    "KFSUWI":  "suez",        # Fire HD 10 Plus (2021)
    "KFONWI":  "karnak",      # Fire 7 (2019)
    "KFKAWI":  "karnak",      # Fire 7 (2022)
    "KFMEWI":  "meso",        # Fire HD 8 (2020)
    "KFOCWI":  "meso",        # Fire HD 8 Plus (2020)
    # ── Nothing ───────────────────────────────────────────────────────────────
    "A063":    "Spacewar",    # Nothing Phone (1)
    "A065":    "Pong",        # Nothing Phone (2)
    "A142":    "PacManPro",   # Nothing Phone (2a)
    # ── Fairphone ─────────────────────────────────────────────────────────────
    "FP3":     "FP3",         # Fairphone 3
    "FP4":     "FP4",         # Fairphone 4
    "FP5":     "FP5",         # Fairphone 5
    # ── OnePlus ───────────────────────────────────────────────────────────────
    "OP594BL": "lemonade",    # OnePlus 9 (NA)
    "OP594DL": "lemonade",    # OnePlus 9 (NA T-Mobile)
}

# Build bidirectional map automatically
_CODENAME_ALIASES: dict[str, list[str]] = {}
for _k, _v in _CODENAME_ALIASES_RAW.items():
    _CODENAME_ALIASES.setdefault(_k.upper(), []).append(_v)
    _CODENAME_ALIASES.setdefault(_v.upper(), []).append(_k)

def _norm_oem(oem: str) -> str:
    if not oem:
        return ""
    key = oem.strip().lower()
    return _OEM_NORM.get(key, oem.strip().title())

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
                    "has_crDroid":       False,
                    "has_matrixx":       False,
                    "has_eos":           False,
                    "has_calyxos":       False,
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

            # Set ROM-specific flags from source field
            src_val = (dev.get("source") or "").lower()
            if "crdroid" in src_val or "crdroid" in (dev.get("rom_name") or "").lower():
                d["has_crDroid"] = True
            if "matrixx" in src_val or "matrixx" in (dev.get("rom_name") or "").lower():
                d["has_matrixx"] = True
            if "/e/" in src_val or "eos" in src_val or "/e/os" in (dev.get("rom_name") or "").lower():
                d["has_eos"] = True
            if "calyx" in src_val or "calyx" in (dev.get("rom_name") or "").lower():
                d["has_calyxos"] = True

            src = dev.get("source", "")
            if src and src not in d["sources"]:
                d["sources"].append(src)

    await cache_set(ck, merged, ttl=3600)
    return merged



def _trim_device(d: dict) -> dict:
    """Remove heavy fields not needed in list/search results."""
    heavy = {"lineageos_branches", "raw_data", "extra", "specs", "full_name"}
    return {k: v for k, v in d.items() if k not in heavy}

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
        "devices": [_trim_device(d) for d in devices[offset: offset + limit]],
    }

async def get_aliases(codename: str) -> list[str]:
    """Return all known codenames for a device including aliases."""
    base = _CODENAME_ALIASES.get(codename, [])
    return [codename] + base


async def get_device_by_codename(codename: str) -> dict | None:
    all_devices = await _get_all_devices()
    return all_devices.get(codename)

# Keep backward compat alias
get_device_detail = get_device_by_codename
