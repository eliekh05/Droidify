"""Live ROM sources — AXP.OS, /e/OS, Ubuntu Touch, LineageOS Wiki, DivestOS."""
import asyncio
import re
from bs4 import BeautifulSoup
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client, fetch

_CODENAME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{2,30}$')

def _entry(name, codename, android_base, description, download_url, source,
           rom_type="custom", status="active", official=True):
    return {
        "name": name, "codename": codename.lower(),
        "android_base": android_base, "rom_type": rom_type,
        "status": status, "source": source, "description": description,
        "download_url": download_url, "official": official,
    }

async def _fetch_axpos(client) -> list[dict]:
    """Scrape AXP.OS device list from axpos.org main page."""
    ck = "roms:axpos_v2"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://axpos.org/")
        if not r or r.status_code != 200: return []
        soup = BeautifulSoup(r.text, "html.parser")
        result = []
        seen = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            m = re.match(r"^/devices/([a-z][a-z0-9]+)/([a-zA-Z][a-zA-Z0-9_]{1,30})/?$", href)
            if not m: continue
            brand, codename = m.group(1), m.group(2)
            if brand in ("changelogs",) or codename in seen: continue
            seen.add(codename)
            label = a.get_text(strip=True) or f"{brand.title()} {codename}"
            result.append(_entry(
                "AXP.OS", codename, "16",
                f"AXP.OS privacy ROM for {label}",
                f"https://axpos.org{href}", "axpos",
                rom_type="privacy",
            ))
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return []

async def _fetch_eos(client) -> list[dict]:
    """Scrape /e/OS device list from doc.e.foundation/devices."""
    ck = "roms:eos_v2"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://doc.e.foundation/devices")
        if not r or r.status_code != 200: return []
        soup = BeautifulSoup(r.text, "html.parser")
        seen = set()
        result = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            m = re.search(r'/devices/([a-z][a-z0-9_]{2,24})(?:/|$)', href)
            if not m: continue
            codename = m.group(1)
            if codename in seen: continue
            seen.add(codename)
            result.append(_entry(
                "/e/OS", codename, "14",
                "Privacy-focused Google-free Android distribution",
                f"https://doc.e.foundation/devices/{codename}", "eos",
                rom_type="privacy",
            ))
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return []

async def _fetch_ubuntu_touch(client) -> list[dict]:
    """Scrape Ubuntu Touch device list."""
    ck = "roms:ubuntu_touch_v2"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://devices.ubuntu-touch.io/")
        if not r or r.status_code != 200: return []
        soup = BeautifulSoup(r.text, "html.parser")
        seen = set()
        result = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            m = re.search(r'/device/([a-zA-Z][a-zA-Z0-9_-]{2,30})/?$', href)
            if not m: continue
            codename = m.group(1).replace("-", "_").lower()
            if codename in seen or not _CODENAME_RE.match(codename): continue
            seen.add(codename)
            label = a.get_text(strip=True) or codename
            result.append(_entry(
                "Ubuntu Touch", codename, "linux",
                f"Ubuntu Touch Linux OS for {label}",
                f"https://devices.ubuntu-touch.io/device/{m.group(1)}/",
                "ubuntu_touch", rom_type="linux",
            ))
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return []

async def _fetch_los_wiki_devices(client) -> list[dict]:
    """
    Fetch all LineageOS wiki device pages.
    wiki.lineageos.org/devices is a JSON API — returns all supported devices.
    """
    ck = "roms:los_wiki_v2"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://wiki.lineageos.org/devices/")
        if not r or r.status_code != 200: return []
        soup = BeautifulSoup(r.text, "html.parser")
        seen = set()
        result = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            m = re.match(r'^/devices/([a-zA-Z][a-zA-Z0-9_]{2,30})/?$', href)
            if not m: continue
            codename = m.group(1).lower()
            if codename in seen: continue
            seen.add(codename)
            result.append(_entry(
                "LineageOS", codename, "20",
                "Official LineageOS — see wiki for exact Android version",
                f"https://wiki.lineageos.org/devices/{m.group(1)}/",
                "lineageos_wiki",
            ))
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_divestos(client) -> list[dict]:
    """
    DivestOS discontinued December 2024 but builds still available.
    Scrape their device list from the archived site.
    """
    ck = "roms:divestos_v2"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://divestos.org/pages/devices")
        if not r or r.status_code != 200: return []
        soup = BeautifulSoup(r.text, "html.parser")
        seen = set()
        result = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            m = re.search(r'/devices/([a-z][a-z0-9_]{2,24})', href)
            if not m: continue
            codename = m.group(1)
            if codename in seen: continue
            seen.add(codename)
            result.append(_entry(
                "DivestOS", codename, "20",
                "DivestOS — privacy/security ROM (discontinued Dec 2024, builds archived)",
                f"https://divestos.org/pages/devices#{codename}",
                "divestos", status="discontinued",
            ))
        await cache_set(ck, result, ttl=86400)
        return result
    except Exception:
        return []

async def get_all_rom_sources() -> list[dict]:
    """All additional ROM sources combined."""
    ck = "roms:all_sources"
    if c := await cache_get(ck): return c

    async with get_client() as client:
        results = await asyncio.gather(
            _fetch_axpos(client),
            _fetch_eos(client),
            _fetch_ubuntu_touch(client),
            _fetch_los_wiki_devices(client),
            _fetch_divestos(client),
            return_exceptions=True,
        )

    all_roms: list[dict] = []
    for r in results:
        if isinstance(r, list):
            all_roms.extend(r)

    await cache_set(ck, all_roms, ttl=7200)
    return all_roms
