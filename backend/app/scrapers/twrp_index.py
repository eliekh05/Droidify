"""TWRP device index — search.json (896 devices) plus manufacturer page scraping."""
import asyncio
import re
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client, fetch

_TWRP_BASE = "https://twrp.me"
_CODENAME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{1,30}$')

# Known TWRP manufacturer pages — scraped live from /Devices/
_MANUFACTURERS = [
    'Alcatel', 'Asus', 'BQ', 'Essential', 'Fairphone', 'Google', 'HTC',
    'Huawei', 'Infinix', 'LeEco', 'Lenovo', 'LG', 'Meizu', 'Mobvoi',
    'Motorola', 'Nokia', 'Nothing', 'Nubia', 'OnePlus', 'Oppo', 'Oukitel',
    'Realme', 'Samsung', 'Sony', 'Tecno', 'Unihertz', 'Xiaomi', 'ZTE',
]

def _extract_codename(text: str) -> str | None:
    """Extract codename from 'Device Name (codename)' format.
    Handles multiple parenthesized groups like 'Galaxy A13 (Exynos) (a13)'.
    Returns the last group that matches a codename pattern.
    """
    all_groups = re.findall(r'\(([^)]+)\)', text)
    if not all_groups:
        return None
    # Codename is the LAST group that looks like a device codename
    # (starts with lowercase, only alphanumeric/underscore/slash)
    for group in reversed(all_groups):
        cn = group.split('/')[0].lower().strip()
        if _CODENAME_RE.match(cn):
            return cn
    return None

async def _fetch_search_json(client) -> list[dict]:
    """Fetch from the global search.json."""
    try:
        r = await fetch(client, f"{_TWRP_BASE}/search.json")
        if not r or r.status_code != 200:
            return []
        result = []
        seen = set()
        for item in r.json():
            title = item.get("title", "")
            url = item.get("url", "")
            codename = _extract_codename(title)
            if not codename or codename in seen:
                continue
            seen.add(codename)
            name = re.sub(r'\s*\([^)]+\)\s*$', '', title).strip()
            result.append({
                "codename": codename,
                "name": name,
                "recovery_url": f"{_TWRP_BASE}{url}",
            })
        return result
    except Exception:
        return []

async def _fetch_manufacturer_page(client, manufacturer: str) -> list[dict]:
    """Fetch device list from a manufacturer's TWRP page."""
    ck = f"twrp:mfr:{manufacturer}"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, f"{_TWRP_BASE}/Devices/{manufacturer}/")
        if not r or r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        result = []
        seen = set()

        # Find all links that contain codenames in parentheses
        for a in soup.find_all("a", href=True):
            href = a["href"]
            # Only device pages
            if not re.match(r'/[a-z][a-z0-9]+/[a-z]', href):
                continue
            text = a.get_text(strip=True)
            codename = _extract_codename(text)
            if not codename or codename in seen:
                continue
            seen.add(codename)
            name = re.sub(r'\s*\([^)]+\)\s*$', '', text).strip()
            result.append({
                "codename": codename,
                "name": name,
                "recovery_url": f"{_TWRP_BASE}{href}",
            })

        await cache_set(ck, result, ttl=86400)
        return result
    except Exception:
        return []

async def get_twrp_index() -> list[dict]:
    """
    Build complete TWRP device index from search.json + all manufacturer pages.
    Returns list of recovery entry dicts.
    """
    ck = "recoveries:twrp_full_index"
    if c := await cache_get(ck): return c

    async with get_client() as client:
        # Fetch search.json and all manufacturer pages concurrently
        all_results = await asyncio.gather(
            _fetch_search_json(client),
            *[_fetch_manufacturer_page(client, mfr) for mfr in _MANUFACTURERS],
            return_exceptions=True,
        )

    # Merge — manufacturer pages take priority (more complete)
    seen: dict[str, dict] = {}

    for batch in all_results:
        if not isinstance(batch, list):
            continue
        for entry in batch:
            cn = entry["codename"]
            if cn not in seen:
                seen[cn] = entry

    result = []
    for cn, entry in seen.items():
        result.append({
            "name": entry["name"],
            "codename": cn,
            "recovery_type": "TWRP",
            "rom_type": "recovery",
            "status": "active",
            "source": "twrp",
            "description": f"TWRP Recovery for {entry['name']}",
            "recovery_url": entry["recovery_url"],
            "download_url": entry["recovery_url"],
            "official": True,
        })

    await cache_set(ck, result, ttl=86400)
    return result

async def get_twrp_for_codename(codename: str) -> list[dict]:
    """Get TWRP entry for a specific codename."""
    index = await get_twrp_index()
    cn = codename.lower()
    lookup = {e["codename"]: e for e in index}
    if cn in lookup:
        return [lookup[cn]]
    # Suffix stripping
    for pattern in [r'xx$', r'lte$', r'3g$', r'4g$', r'wifi$', r'[a-z]{2,3}$']:
        stripped = re.sub(pattern, '', cn)
        if stripped and stripped != cn and stripped in lookup:
            return [lookup[stripped]]
    return []
