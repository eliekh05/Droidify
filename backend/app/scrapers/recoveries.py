"""Recovery scraper — TWRP (896) and OrangeFox (159) from free public APIs."""
import asyncio
import re

from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

TWRP_SEARCH   = "https://twrp.me/search.json"
ORANGEFOX_API = "https://api.orangefox.download/v3/devices/?per_page=500"

_OEM_MAP: dict[str, str] = {
    "alcatel":"Alcatel","asus":"ASUS","bq":"BQ","essential":"Essential",
    "fairphone":"Fairphone","google":"Google","htc":"HTC","huawei":"Huawei",
    "lenovo":"Lenovo","lg":"LG","motorola":"Motorola","nokia":"Nokia",
    "nothing":"Nothing","oneplus":"OnePlus","oppo":"OPPO","realme":"Realme",
    "samsung":"Samsung","shift":"Shift","sony":"Sony","xiaomi":"Xiaomi",
    "zte":"ZTE","amazon":"Amazon","blackberry":"BlackBerry","wileyfox":"Wileyfox",
    "yandex":"Yandex","umidigi":"UMIDIGI","oukitel":"Oukitel",
}


async def _fetch_twrp(client) -> list[dict]:
    ck = "twrp_list"
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

        oem_key      = url.strip("/").split("/")[0].lower() if "/" in url else ""
        manufacturer = _OEM_MAP.get(oem_key, oem_key.title())

        devices.append({
            "codename":     codename,
            "model_name":   model_name,
            "manufacturer": manufacturer,
            "recovery":     "TWRP",
            "status":       "active",
            "source_url":   f"https://twrp.me{url}",
            "download_url": f"https://dl.twrp.me/{codename}/",
            "source":       "twrp",
        })

    await cache_set(ck, devices, ttl=600)
    return devices


async def _fetch_orangefox(client) -> list[dict]:
    ck = "orangefox_list"
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
            "recovery":     "OrangeFox",
            "status":       "active" if dev.get("supported", True) else "unmaintained",
            "source_url":   dev.get("url", f"https://orangefox.download/device/{codename}"),
            "download_url": dev.get("url", ""),
            "source":       "orangefox",
        })

    await cache_set(ck, devices, ttl=600)
    return devices


async def get_recoveries(
    q: str | None = None,
    recovery: str | None = None,
    manufacturer: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    """Return merged TWRP + OrangeFox device list."""
    ck = "all_recoveries_merged"
    cached = await cache_get(ck)

    if cached is None:
        async with get_client() as client:
            twrp_list, fox_list = await asyncio.gather(
                _fetch_twrp(client),
                _fetch_orangefox(client),
            )

        merged: list[dict] = []
        seen: set[str] = set()
        for d in twrp_list:
            k = f"twrp:{d['codename']}"
            if k not in seen:
                seen.add(k)
                merged.append(d)
        for d in fox_list:
            k = f"orangefox:{d['codename']}"
            if k not in seen:
                seen.add(k)
                merged.append(d)

        await cache_set(ck, merged, ttl=600)
        cached = merged

    devices = list(cached or [])

    if q:
        ql = q.lower()
        qn = re.sub('[-_ ]', '', ql)

        def _rec_matches(d: dict) -> bool:
            codename = (d.get("codename")     or "").lower()
            model    = (d.get("model_name")   or "").lower()
            mfr      = (d.get("manufacturer") or "").lower()
            return (
                ql in codename or ql in model or ql in mfr
                or qn in re.sub('[-_ ]', '', codename)
                or qn in re.sub('[-_ ]', '', model)
                or qn in re.sub('[-_ ]', '', mfr)
                or codename.startswith(ql)
            )

        devices = [d for d in devices if _rec_matches(d)]
    if recovery:
        devices = [d for d in devices if d["recovery"].lower() == recovery.lower()]
    if manufacturer:
        ml = manufacturer.lower()
        devices = [d for d in devices if ml in d.get("manufacturer", "").lower()]

    total = len(devices)
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "recoveries": devices[offset: offset + limit],
    }


async def get_recovery_for_device(codename: str) -> list[dict]:
    result = await get_recoveries(limit=1000)
    return [r for r in result["recoveries"] if r["codename"].lower() == codename.lower()]
