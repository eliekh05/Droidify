"""/e/OS unofficial builds from sourceforge.net/projects/eosbuildsronnz98 (~500 devices)."""
import asyncio
import re
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client, fetch

_BASE = "https://sourceforge.net/projects/eosbuildsronnz98/files"
_CODENAME_RE = re.compile(r'^[a-z][a-z0-9_]{2,30}$')
_CATEGORIES = [
    "SamsungSmartphones",
    "SamsungTabs",
    "XiaomiSmartphones",
    "OtherSmartphones",
    "LG",
    "Motorola",
    "Realme",
    "OnePlus",
    "Fairphone",
    "OtherCustomROMS",
]

async def _fetch_category(client, category: str) -> list[dict]:
    """Fetch all devices in a category folder."""
    ck = f"roms:eosbuilds:{category}"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, f"{_BASE}/{category}/",
                       headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
        if not r or r.status_code != 200:
            return []
        # Extract codenames from zip filenames: UNOFFICIAL-{codename}.zip
        codenames = set(re.findall(r'UNOFFICIAL-([a-z][a-z0-9_]{2,24})\.zip', r.text))
        result = []
        for codename in codenames:
            if not _CODENAME_RE.match(codename):
                continue
            result.append({
                "name": "/e/OS (Community Build)",
                "codename": codename,
                "android_base": "unknown",
                "rom_type": "privacy",
                "status": "active",
                "source": "eosbuilds_community",
                "description": "Unofficial /e/OS build — community maintained",
                "download_url": f"{_BASE}/{category}/",
                "source_url": "https://sourceforge.net/projects/eosbuildsronnz98/",
                "official": False,
            })
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return []

async def get_eosbuilds_roms() -> list[dict]:
    """Fetch all community /e/OS builds across all categories."""
    ck = "roms:eosbuilds_all"
    if c := await cache_get(ck): return c

    async with get_client() as client:
        results = await asyncio.gather(
            *[_fetch_category(client, cat) for cat in _CATEGORIES],
            return_exceptions=True,
        )

    seen = set()
    all_roms: list[dict] = []
    for r in results:
        if not isinstance(r, list):
            continue
        for rom in r:
            cn = rom["codename"]
            if cn not in seen:
                seen.add(cn)
                all_roms.append(rom)

    await cache_set(ck, all_roms, ttl=43200)
    return all_roms
