"""
recoveries.py — expanded recovery scraper
Sources:
  TWRP       — twrp.me/search.json          ~900 devices
  OrangeFox  — api.orangefox.download        ~160 devices
  PBRP       — GitHub PitchBlackRecoveryProject org repos  ~80+ devices
  SHRP       — GitHub SHRP-Devices org repos ~60+ devices
  LineageOS  — lineageos.org wiki devices with recovery tags
  uTWRP      — unofficialtwrp.com scrape    already in unofficialtwrp.py
Total target: 300+ unique codenames
"""
import asyncio
import re

from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

TWRP_SEARCH   = "https://twrp.me/search.json"
ORANGEFOX_API = "https://api.orangefox.download/v3/devices/?per_page=500"
GH_API        = "https://api.github.com"
GH_UA         = "DroidifyBot/2.0 (+https://github.com/eliekh05/Droidify)"

_OEM_MAP: dict[str, str] = {
    "alcatel":"Alcatel","asus":"ASUS","bq":"BQ","essential":"Essential",
    "fairphone":"Fairphone","google":"Google","htc":"HTC","huawei":"Huawei",
    "honor":"Honor","infinix":"Infinix","itel":"itel","lenovo":"Lenovo",
    "lg":"LG","motorola":"Motorola","nokia":"Nokia","nothing":"Nothing",
    "oneplus":"OnePlus","oppo":"OPPO","realme":"Realme","samsung":"Samsung",
    "shift":"Shift","sony":"Sony","tecno":"Tecno","vivo":"Vivo",
    "xiaomi":"Xiaomi","zte":"ZTE","amazon":"Amazon","blackberry":"BlackBerry",
    "wileyfox":"Wileyfox","yandex":"Yandex","umidigi":"UMIDIGI",
    "oukitel":"Oukitel","blackview":"Blackview","doogee":"DOOGEE",
    "ulefone":"Ulefone","meizu":"Meizu","nubia":"Nubia","zte":"ZTE",
    "lge":"LG","moto":"Motorola","redmi":"Xiaomi","pocophone":"Xiaomi",
}

def _oem_from_repo(repo_name: str) -> str:
    """Extract manufacturer from android_device_BRAND_codename repo name."""
    # android_device_xiaomi_whyred-pbrp → xiaomi
    # device_samsung_d2x → samsung
    parts = repo_name.split("_")
    for i, part in enumerate(parts):
        if part in ("device",) and i + 1 < len(parts):
            brand = parts[i + 1].lower()
            return _OEM_MAP.get(brand, brand.title())
    return ""

def _codename_from_repo(repo_name: str, suffix: str) -> str:
    """Extract codename from repo name."""
    # android_device_xiaomi_whyred-pbrp → whyred
    # device_samsung_d2x → d2x
    name = repo_name
    if suffix and name.endswith(suffix):
        name = name[: -len(suffix)]
    parts = name.split("_")
    if len(parts) >= 3:
        return parts[-1]
    return ""


# ── TWRP ─────────────────────────────────────────────────────────────────────
async def _fetch_twrp(client) -> list[dict]:
    ck = "rec:twrp"
    cached = await cache_get(ck)
    if cached:
        return cached

    resp = await fetch(client, TWRP_SEARCH)
    if not resp or resp.status_code != 200:
        return []

    devices: list[dict] = []
    for entry in resp.json():
        title = entry.get("title", "")
        url   = entry.get("url", "")
        code_m = re.search(r"\(([a-zA-Z0-9_]+)\)$", title)
        if not code_m:
            continue
        codename   = code_m.group(1)
        model_name = re.sub(r"\s*\([^)]+\)$", "", title).strip()
        oem_key    = url.strip("/").split("/")[0].lower() if "/" in url else ""
        devices.append({
            "codename":     codename,
            "model_name":   model_name,
            "manufacturer": _OEM_MAP.get(oem_key, oem_key.title()),
            "recovery_type":"TWRP",
            "status":       "active",
            "source_url":   f"https://twrp.me{url}",
            "download_url": f"https://dl.twrp.me/{codename}/",
            "source":       "twrp",
        })

    await cache_set(ck, devices, ttl=3600)
    return devices


# ── OrangeFox ─────────────────────────────────────────────────────────────────
async def _fetch_orangefox(client) -> list[dict]:
    ck = "rec:orangefox"
    cached = await cache_get(ck)
    if cached:
        return cached

    resp = await fetch(client, ORANGEFOX_API)
    if not resp or resp.status_code != 200:
        return []

    devices: list[dict] = []
    for dev in resp.json().get("data", []):
        codename = dev.get("codename", "")
        if not codename:
            continue
        devices.append({
            "codename":     codename,
            "model_name":   dev.get("full_name", dev.get("model_name", "")),
            "manufacturer": dev.get("oem_name", ""),
            "recovery_type":"OrangeFox",
            "status":       "active" if dev.get("supported", True) else "unmaintained",
            "source_url":   dev.get("url", f"https://orangefox.download/device/{codename}"),
            "download_url": dev.get("url", ""),
            "source":       "orangefox",
        })

    await cache_set(ck, devices, ttl=3600)
    return devices


# ── PBRP (PitchBlack) via GitHub org repos ───────────────────────────────────
async def _fetch_pbrp(client) -> list[dict]:
    ck = "rec:pbrp"
    cached = await cache_get(ck)
    if cached:
        return cached

    devices: list[dict] = []
    page = 1
    headers = {"User-Agent": GH_UA, "Accept": "application/vnd.github+json"}

    while True:
        url = f"{GH_API}/orgs/PitchBlackRecoveryProject/repos?type=public&per_page=100&page={page}"
        try:
            resp = await client.get(url, headers=headers)
            if resp.status_code != 200:
                break
            repos = resp.json()
            if not repos:
                break
        except Exception:
            break

        for repo in repos:
            name = repo.get("name", "")
            if not name.startswith("android_device_") or not name.endswith("-pbrp"):
                continue

            # Extract brand and codename
            # android_device_xiaomi_whyred-pbrp
            inner = name[len("android_device_"):-len("-pbrp")]  # xiaomi_whyred
            parts = inner.split("_", 1)
            if len(parts) < 2:
                continue
            brand    = parts[0].lower()
            codename = parts[1]
            mfr      = _OEM_MAP.get(brand, brand.title())

            # Use repo description as model name if available
            desc = repo.get("description") or ""
            model_name = desc.split("Device Tree")[0].strip() if "Device Tree" in desc else codename

            devices.append({
                "codename":     codename,
                "model_name":   model_name or codename,
                "manufacturer": mfr,
                "recovery_type":"PBRP",
                "status":       "unmaintained" if repo.get("archived") else "active",
                "source_url":   repo.get("html_url", ""),
                "download_url": f"https://sourceforge.net/projects/pbrp/files/{codename}/",
                "source":       "pbrp",
            })

        if len(repos) < 100:
            break
        page += 1

    await cache_set(ck, devices, ttl=3600)
    return devices


# ── SHRP (SkyHawk) via GitHub org repos ──────────────────────────────────────
async def _fetch_shrp(client) -> list[dict]:
    ck = "rec:shrp"
    cached = await cache_get(ck)
    if cached:
        return cached

    devices: list[dict] = []
    page = 1
    headers = {"User-Agent": GH_UA, "Accept": "application/vnd.github+json"}

    while True:
        url = f"{GH_API}/orgs/SHRP-Devices/repos?type=public&per_page=100&page={page}"
        try:
            resp = await client.get(url, headers=headers)
            if resp.status_code != 200:
                break
            repos = resp.json()
            if not repos:
                break
        except Exception:
            break

        for repo in repos:
            name = repo.get("name", "")
            # device_samsung_d2x or device_xiaomi_whyred
            if not name.startswith("device_"):
                continue

            parts = name.split("_", 2)  # ['device', 'samsung', 'd2x']
            if len(parts) < 3:
                continue
            brand    = parts[1].lower()
            codename = parts[2]
            mfr      = _OEM_MAP.get(brand, brand.title())

            desc = repo.get("description") or ""
            model_name = desc or codename

            devices.append({
                "codename":     codename,
                "model_name":   model_name,
                "manufacturer": mfr,
                "recovery_type":"SHRP",
                "status":       "unmaintained" if repo.get("archived") else "active",
                "source_url":   repo.get("html_url", ""),
                "download_url": f"https://sourceforge.net/projects/shrp/files/{codename}/",
                "source":       "shrp",
            })

        if len(repos) < 100:
            break
        page += 1

    await cache_set(ck, devices, ttl=3600)
    return devices


# ── Unified get_recoveries ─────────────────────────────────────────────────────
async def get_recoveries(
    q: str | None = None,
    recovery: str | None = None,
    manufacturer: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    ck = "rec:all_merged"
    cached = await cache_get(ck)

    if cached is None:
        async with get_client() as client:
            twrp, fox, pbrp, shrp = await asyncio.gather(
                _fetch_twrp(client),
                _fetch_orangefox(client),
                _fetch_pbrp(client),
                _fetch_shrp(client),
                return_exceptions=True,
            )

        merged: list[dict] = []
        seen: set[str] = set()

        for source_list in [twrp, fox, pbrp, shrp]:
            if isinstance(source_list, Exception):
                continue
            for d in source_list:
                key = f"{d.get('source','?')}:{d.get('codename','?')}"
                if key not in seen:
                    seen.add(key)
                    merged.append(d)

        await cache_set(ck, merged, ttl=3600)
        cached = merged

    devices = list(cached or [])

    if q:
        ql = q.lower()
        qn = re.sub(r"[-_ ]", "", ql)
        def _match(d: dict) -> bool:
            c = (d.get("codename") or "").lower()
            m = (d.get("model_name") or "").lower()
            f = (d.get("manufacturer") or "").lower()
            r = (d.get("recovery_type") or "").lower()
            return (
                ql in c or ql in m or ql in f or ql in r
                or qn in re.sub(r"[-_ ]", "", c)
                or qn in re.sub(r"[-_ ]", "", m)
                or c.startswith(ql)
            )
        devices = [d for d in devices if _match(d)]

    if recovery:
        devices = [d for d in devices if (d.get("recovery_type") or "").lower() == recovery.lower()]
    if manufacturer:
        ml = manufacturer.lower()
        devices = [d for d in devices if ml in (d.get("manufacturer") or "").lower()]

    total = len(devices)
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "recoveries": devices[offset: offset + limit],
    }


async def get_recovery_for_device(codename: str) -> list[dict]:
    result = await get_recoveries(limit=9999)
    cl = codename.lower()
    return [r for r in result["recoveries"] if r.get("codename", "").lower() == cl]
