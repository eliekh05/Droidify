"""Extended ROM sources — crDroid, iodéOS, OmniROM, AXP.OS, crDroid SF."""
import asyncio
import re
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client, fetch, fetch

# crDroid has a per-device JSON at: https://sourceforge.net/projects/crdroid/files/{codename}/
# The OTA repo lists ALL official devices as JSON files
async def _fetch_crdroid_ota() -> list[dict]:
    """crDroid devices from crdroid.net website — no GitHub API."""
    ck = "roms:crdroid_ota"
    if c := await cache_get(ck): return c
    try:
        async with get_client() as client:
            r = await fetch(client, "https://crdroid.net/downloads")
            if not r or r.status_code != 200:
                return []
        codenames = re.findall(r"id=\'([a-z][a-z0-9_]{2,24})\'", r.text)
        if not codenames:
            codenames = re.findall(r'id="([a-z][a-z0-9_]{2,24})"', r.text)
        skip = {"header","navbar","main","search","footer","content","root"}
        # Extract crDroid version from page — look for version number in download links
        crd_ver = "unknown"
        ver_m = re.search(r"crdroid\.net/\w+/(\d+)", r.text)
        if not ver_m:
            # Try the SF listing version pattern
            ver_m = re.search(r"/crdroid/files/\w+/(\d+)/", r.text)
        if ver_m:
            crd_ver = ver_m.group(1)
        else:
            # Fallback: check latest Android version from crdroid.net changelog
            try:
                ver_text = re.search(r"crDroid Android[\s]+([0-9.]+)", r.text)
                if ver_text:
                    crd_ver = ver_text.group(1).split(".")[0]
            except Exception:
                pass

        result = [{
            "name": "crDroid", "codename": cn, "android_base": crd_ver,
            "rom_type": "custom", "status": "active", "source": "crdroid_web",
            "description": f"Official crDroid — Android {crd_ver}, LineageOS-based",
            "download_url": f"https://crdroid.net/{cn}/{crd_ver}",
            "official": True, "maintainer": "crDroid Team",
        } for cn in codenames if cn not in skip]
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_iodeos() -> list[dict]:
    ck = "roms:iodeos"
    if c := await cache_get(ck): return c
    try:
        async with get_client() as client:
            r = await fetch(client, "https://ota.iode.tech/v1/devices")
            if not r or r.status_code != 200:
                return []
        data = r.json()
        result = []
        if isinstance(data, list):
            for d in data:
                codename = (d.get("model") or d.get("codename") or "").lower()
                if codename:
                    result.append({
                        "name":         "iodéOS",
                        "codename":     codename,
                        "android_base": str(d.get("android_version", "15")),
                        "rom_type":     "privacy",
                        "status":       "active",
                        "source":       "iodeos",
                        "description":  "Privacy ROM with built-in adblocker, LineageOS-based",
                        "download_url": f"https://iode.tech/get-iodeos/#{codename}",
                        "official":     True,
                    })
        await cache_set(ck, result, ttl=3600)
        return result
    except Exception:
        return []

async def _fetch_omnirom() -> list[dict]:
    """OmniROM devices from dl.omnirom.org — no GitHub API."""
    ck = "roms:omnirom"
    if c := await cache_get(ck): return c
    try:
        async with get_client() as client:
            r = await fetch(client, "https://dl.omnirom.org/")
            if not r or r.status_code != 200:
                return []
        codenames = re.findall(r'href="/([a-z][a-z0-9_]{2,24})/"', r.text)
        result = [{
            "name": "OmniROM", "codename": cn, "android_base": "unknown",
            "rom_type": "custom", "status": "active", "source": "omnirom",
            "description": "AOSP-based ROM from OmniROM team",
            "download_url": f"https://dl.omnirom.org/{cn}/", "official": True,
        } for cn in codenames if re.match(r"^[a-z][a-z0-9_]{2,24}$", cn)]
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_axpos() -> list[dict]:
    """Scrape AXP.OS device list from axpos.org/devices/ — no hardcoded devices."""
    ck = "roms:axpos"
    if c := await cache_get(ck): return c
    try:
        async with get_client() as client:
            r = await fetch(client, "https://axpos.org/")
            if not r or r.status_code != 200:
                return []
        from bs4 import BeautifulSoup as _BS
        soup = _BS(r.text, "html.parser")
        result = []
        seen = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            # Pattern: /devices/{brand}/{codename}/
            m = re.match(r"^/devices/([a-z][a-z0-9]+)/([a-zA-Z][a-zA-Z0-9_]{1,30})/?$", href)
            if not m:
                continue
            brand, codename = m.group(1), m.group(2)
            if codename in seen or brand in ("changelogs",):
                continue
            seen.add(codename)
            result.append({
                "name":         "AXP.OS",
                "codename":     codename,
                "android_base": "unknown",
                "rom_type":     "privacy",
                "status":       "active",
                "source":       "axpos",
                "official":     True,
                "description":  f"AXP.OS privacy ROM for {a.get_text(strip=True)}",
                "download_url": f"https://axpos.org{href}",
                "source_url":   "https://axpos.org/devices/",
            })
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return []

# These are devices confirmed to have ROMs via XDA/wiki research
# but not covered by automated scraping

async def _fetch_crdroid_sf(client) -> list[dict]:
    """
    Fetch crDroid device list from SourceForge project file listing.
    The SF project root page lists all device codename folders.
    """
    ck = "roms:crdroid_sf"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://sourceforge.net/projects/crdroid/files/",
                       headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
        if not r or r.status_code != 200:
            return []
        # SF lists folder names in the page
        codenames = set(re.findall(
            r'/projects/crdroid/files/([a-z][a-z0-9_]{2,24})/',
            r.text
        )) - {'latest', 'download', 'stats', 'OldReleases'}
        result = []
        for codename in codenames:
            result.append({
                "name":         "crDroid",
                "codename":     codename,
                "android_base": "unknown",
                "rom_type":     "custom",
                "status":       "active",
                "source":       "crdroid_sf",
                "description":  "crDroid Android — feature-rich LineageOS fork",
                "download_url": f"https://sourceforge.net/projects/crdroid/files/{codename}/",
                "source_url":   "https://crdroid.net/",
                "official":     True,
            })
        await cache_set(ck, result, ttl=21600)
        return result
    except Exception:
        return []

async def get_extended_roms() -> list[dict]:
    """All extended ROM sources combined."""
    ck = "roms:extended_all"
    if c := await cache_get(ck): return c

    async with get_client() as _ext_client:
        crdroid_sf = await _fetch_crdroid_sf(_ext_client)

    sources = await asyncio.gather(
        _fetch_crdroid_ota(),
        _fetch_iodeos(),
        _fetch_omnirom(),
        return_exceptions=True,
    )
    sources = list(sources) + [crdroid_sf]

    result: list[dict] = []
    for source in sources:
        if isinstance(source, list):
            result.extend(source)

    await cache_set(ck, result, ttl=3600)
    return result
