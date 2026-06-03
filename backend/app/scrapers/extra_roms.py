"""Additional ROM sources via raw.githubusercontent.com — LineageOS MicroG, ProjectSakura."""
import asyncio
import re
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client, fetch

_CODENAME_RE = re.compile(r'^[a-z][a-z0-9_]{2,30}$')

def _entry(name, codename, android_base, description, download_url, source, maintainer=None, xda=None):
    e = {
        "name": name, "codename": codename,
        "android_base": android_base, "rom_type": "custom",
        "status": "active", "source": source,
        "description": description, "download_url": download_url,
        "official": True,
    }
    if maintainer: e["maintainer"] = maintainer
    if xda: e["xda_thread"] = xda
    return e

async def _fetch_los_microg(client) -> list[dict]:
    ck = "roms:los_microg_v2"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://download.lineage.microg.org/")
        if not r or r.status_code != 200: return []
        data = r.json()
        result = []
        for item in data:
            name = item.get('name', '').rstrip('/')
            if _CODENAME_RE.match(name):
                result.append(_entry(
                    "LineageOS for MicroG", name, "21",
                    "Official LineageOS with built-in MicroG — no Google Play Services required",
                    f"https://download.lineage.microg.org/{name}/",
                    "los_microg",
                ))
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_raw_ota(client, rom_name, raw_url, android_base, description,
                          source, dl_template) -> list[dict]:
    ck = f"roms:raw_ota_{source}"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, raw_url)
        if not r or r.status_code != 200: return []
        data = r.json()
        # Handle both list and {devices:[...]} formats
        if isinstance(data, dict):
            data = data.get('devices', data.get('response', []))
        if not isinstance(data, list): return []

        result = []
        for item in data:
            if not isinstance(item, dict): continue
            # Try multiple codename field names
            codename = (item.get('codename') or item.get('device') or
                       item.get('model') or '').lower().strip()
            if not codename or not _CODENAME_RE.match(codename): continue
            maintainer = item.get('maintainer_name') or item.get('maintainer') or f"{rom_name} Team"
            xda = item.get('xda_thread') or item.get('xda') or None
            active = item.get('active', True)
            result.append(_entry(
                rom_name, codename, android_base, description,
                dl_template.replace("{codename}", codename),
                source, maintainer, xda,
            ))
            if not active:
                result[-1]['status'] = 'unmaintained'

        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_project_sakura(client) -> list[dict]:
    return await _fetch_raw_ota(
        client,
        "Project Sakura",
        "https://raw.githubusercontent.com/ProjectSakura/OTA/11/devices.json",
        "11",
        "Pixel-like AOSP ROM with smooth animations and Sakura features",
        "project_sakura",
        "https://github.com/ProjectSakura/OTA",
    )

async def _fetch_havoc(client) -> list[dict]:
    # HavocOS has SF listing — already in SF scraper
    # Try their direct JSON
    return await _fetch_raw_ota(
        client,
        "HavocOS",
        "https://raw.githubusercontent.com/Havoc-Devices/android_vendor_HavocOTA/ten/devices.json",
        "10",
        "AOSP ROM with extensive feature set",
        "havoc_ota",
        "https://sourceforge.net/projects/havoc-os/files/{codename}/",
    )

async def _fetch_nusantara(client) -> list[dict]:
    return await _fetch_raw_ota(
        client,
        "Nusantara Project",
        "https://raw.githubusercontent.com/nusantara-devices/official_devices/main/devices.json",
        "13",
        "Indonesian AOSP ROM with unique features",
        "nusantara",
        "https://sourceforge.net/projects/nusantaraproject/files/{codename}/",
    )

async def _fetch_dotos(client) -> list[dict]:
    return await _fetch_raw_ota(
        client,
        "DotOS",
        "https://raw.githubusercontent.com/DotOS-Devices/official_devices/dot12/devices.json",
        "12",
        "Pixel-like AOSP ROM with Dot features",
        "dotos",
        "https://sourceforge.net/projects/dotos/files/{codename}/",
    )

async def _fetch_stagos(client) -> list[dict]:
    return await _fetch_raw_ota(
        client,
        "StagOS",
        "https://raw.githubusercontent.com/StagOS-Devices/official_devices/tiramisu/devices.json",
        "13",
        "Clean AOSP-based ROM",
        "stagos",
        "https://sourceforge.net/projects/stagos/files/{codename}/",
    )

async def _fetch_pixeldust(client) -> list[dict]:
    return await _fetch_raw_ota(
        client,
        "PixelDust",
        "https://raw.githubusercontent.com/pixeldust-devices/official_devices/twelve/devices.json",
        "12",
        "Pixel-like ROM with dust of extras",
        "pixeldust",
        "https://sourceforge.net/projects/pixeldust/files/{codename}/",
    )

async def _fetch_ancientos(client) -> list[dict]:
    return await _fetch_raw_ota(
        client,
        "AncientOS",
        "https://raw.githubusercontent.com/Ancient-Project/official_devices/ancient-v6/devices.json",
        "13",
        "AOSP ROM with unique ancient theme",
        "ancientos",
        "https://sourceforge.net/projects/ancientos/files/{codename}/",
    )

async def _fetch_sparkos(client) -> list[dict]:
    return await _fetch_raw_ota(
        client,
        "SparkOS",
        "https://raw.githubusercontent.com/Spark-OS-Devices/official_devices/12.1/devices.json",
        "12",
        "AOSP ROM with spark of customization",
        "sparkos",
        "https://sourceforge.net/projects/spark-os/files/{codename}/",
    )

async def _fetch_pixel_extended(client) -> list[dict]:
    return await _fetch_raw_ota(
        client,
        "Pixel Extended",
        "https://raw.githubusercontent.com/PixelExtended/official_devices/thirteen/devices.json",
        "13",
        "Stock Android with extra features",
        "pixel_extended",
        "https://sourceforge.net/projects/pixelextended/files/{codename}/",
    )

async def _fetch_yaap(client) -> list[dict]:
    # YAAP stores device JSONs individually — get listing from tree
    ck = "roms:yaap"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://raw.githubusercontent.com/yaap/devices/main/devices.json")
        if not r or r.status_code != 200:
            return []
        data = r.json()
        if isinstance(data, dict):
            data = list(data.values()) if not data.get('devices') else data['devices']
        result = []
        for item in (data if isinstance(data, list) else []):
            cn = (item.get('codename') or item.get('device') or '').lower()
            if cn and _CODENAME_RE.match(cn):
                result.append(_entry(
                    "YAAP", cn, "14",
                    "Yet Another AOSP Project — minimal and clean",
                    f"https://github.com/yaap/devices",
                    "yaap",
                ))
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def get_extra_roms() -> list[dict]:
    """All extra ROM sources combined."""
    ck = "roms:extra_all"
    if c := await cache_get(ck): return c

    async with get_client() as client:
        results = await asyncio.gather(
            _fetch_los_microg(client),
            _fetch_project_sakura(client),
            _fetch_havoc(client),
            _fetch_nusantara(client),
            _fetch_dotos(client),
            _fetch_stagos(client),
            _fetch_pixeldust(client),
            _fetch_ancientos(client),
            _fetch_sparkos(client),
            _fetch_yaap(client),
            return_exceptions=True,
        )

    all_roms: list[dict] = []
    for r in results:
        if isinstance(r, list):
            all_roms.extend(r)

    await cache_set(ck, all_roms, ttl=7200)
    return all_roms
