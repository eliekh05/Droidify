"""
roms.py — Unified ROM index with O(1) device lookup.

Key design: build a codename→roms lookup table ONCE at startup using
all ROM indexes. Device lookup is then a simple dict key lookup instead
of 9 sequential HTTP calls.

Sources indexed at startup:
  - SourceForge (23 ROM projects, ~1,600 entries)
  - PixelExperience (~200 devices)
  - LineageOS API (from devices scraper)
  - Community ROMs (Evolution X, crDroid extra, etc.)
  - DivestOS, CalyxOS, /e/OS, GrapheneOS
  - Ubuntu Touch, NetHunter, postmarketOS

Per-device lookup: O(1) dict lookup from pre-built index.
First build: ~30s on cold start (concurrent fetching).
Subsequent builds: cached 2 hours.
"""
import asyncio
import re
from typing import Any

from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

# Alias for backward compat
cache_get = cache_get
cache_set = cache_set

# LineageOS branch → Android version mapping
LOS_BRANCH_TO_ANDROID: dict[str, str] = {
    "lineage-21": "14", "lineage-20": "13", "lineage-19.1": "12.1",
    "lineage-19": "12", "lineage-18.1": "11", "lineage-17.1": "10",
    "lineage-16.0": "9", "lineage-15.1": "8.1", "lineage-14.1": "7.1",
}

_NORM = lambda s: re.sub(r'[-_ .]', '', (s or '').lower())


async def _roms_from_lineageos() -> list[dict]:
    """Fetch LineageOS builds from official download API.
    Returns one entry per device codename with official download link.
    """
    ck = "roms:lineageos_downloads"
    if c := await cache_get(ck): return c
    try:
        async with get_client() as client:
            r = await fetch(client, "https://download.lineageos.org/api/v1/devices")
            if not r or r.status_code != 200:
                return []
        data = r.json()
        result = []
        for version, codenames in data.items():
            if not isinstance(codenames, list):
                continue
            android_ver = LOS_BRANCH_TO_ANDROID.get(
                f"lineage-{version.split('.')[0]}", version
            )
            for codename in codenames:
                cn = codename.lower().strip()
                result.append({
                    "name":         "LineageOS",
                    "codename":     cn,
                    "android_base": android_ver,
                    "rom_type":     "custom",
                    "status":       "active",
                    "source":       "lineageos_official",
                    "description":  "Official LineageOS build",
                    "download_url": f"https://download.lineageos.org/{cn}",
                    "version_label": f"LineageOS {version}",
                    "official":     True,
                    "maintainer":   "LineageOS Team",
                })
        await cache_set(ck, result, ttl=3600)
        return result
    except Exception:
        return []


# ── Source fetchers ───────────────────────────────────────────────────────────

async def _roms_from_grapheneos() -> list[dict]:
    ck = "roms:grapheneos_devices"
    if c := await cache_get(ck): return c
    try:
        async with get_client() as client:
            r = await fetch(client, "https://releases.grapheneos.org/releases")
            if not r or r.status_code != 200:
                return []
        codenames = list({line.split("-")[0] for line in r.text.splitlines()
                         if line and not line.startswith("#") and "-" in line})
        result = [{"name":"GrapheneOS","codename":c,"android_base":"14",
                   "source":"grapheneos","rom_type":"privacy","status":"active",
                   "download_url":f"https://grapheneos.org/install/web"} for c in codenames]
        await cache_set(ck, result, ttl=3600)
        return result
    except Exception:
        return []


async def _roms_from_divestos() -> list[dict]:
    ck = "roms:divestos"
    if c := await cache_get(ck): return c
    try:
        async with get_client() as client:
            r = await fetch(client, "https://divestos.org/pages/devices")
            if not r or r.status_code != 200:
                return []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        result = []
        for a in soup.select("a[href*='/devices/']"):
            text = a.get_text(strip=True)
            href = a.get("href", "")
            code_m = re.search(r'/devices/([a-z][a-z0-9_]+)', href)
            if code_m:
                result.append({"name":"DivestOS","codename":code_m.group(1),
                               "android_base":"20","source":"divestos",
                               "rom_type":"privacy","status":"active",
                               "download_url":f"https://divestos.org/pages/devices#{code_m.group(1)}"})
        await cache_set(ck, result, ttl=3600)
        return result
    except Exception:
        return []


async def _roms_from_calyxos() -> list[dict]:
    ck = "roms:calyxos"
    if c := await cache_get(ck): return c
    try:
        async with get_client() as client:
            r = await fetch(client, "https://calyxos.org/install/devices/")
            if not r or r.status_code != 200:
                return []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        result = []
        for a in soup.select("a[href*='/install/']"):
            href = a.get("href","")
            m = re.search(r'/install/([a-z][a-z0-9_]+)/', href)
            if m:
                result.append({"name":"CalyxOS","codename":m.group(1),
                               "android_base":"14","source":"calyxos",
                               "rom_type":"privacy","status":"active",
                               "download_url":f"https://calyxos.org/install/{m.group(1)}/"})
        await cache_set(ck, result, ttl=3600)
        return result
    except Exception:
        return []


async def _roms_from_eos() -> list[dict]:
    ck = "roms:eos"
    if c := await cache_get(ck): return c
    try:
        async with get_client() as client:
            r = await fetch(client, "https://doc.e.foundation/devices")
            if not r or r.status_code != 200:
                return []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        result = []
        seen: set[str] = set()
        for a in soup.select("a[href]"):
            href = a.get("href","")
            m = re.search(r'/devices/([a-z][a-z0-9_]+)', href)
            if m and m.group(1) not in seen:
                seen.add(m.group(1))
                result.append({"name":"/e/OS","codename":m.group(1),
                               "android_base":"13","source":"eos",
                               "rom_type":"privacy","status":"active",
                               "download_url":f"https://doc.e.foundation/devices/{m.group(1)}"})
        await cache_set(ck, result, ttl=3600)
        return result
    except Exception:
        return []


# ── Lookup table ──────────────────────────────────────────────────────────────

async def _build_lookup() -> dict[str, list[dict]]:
    """
    Build codename → roms lookup table from all sources.
    This is the heavy operation — runs once, cached 2 hours.
    """
    ck = "roms:lookup_table"
    if c := await cache_get(ck): return c

    # Fetch all indexes concurrently
    from app.scrapers.sourceforge_roms import get_sourceforge_roms
    from app.scrapers.gsi_roms import get_gsi_roms
    from app.scrapers.extended_roms import get_extended_roms
    from app.scrapers.extra_roms import get_extra_roms
    from app.scrapers.pixelexperience import get_pixelexperience_roms
    from app.scrapers.unofficialtwrp import get_unofficialtwrp_devices
    from app.scrapers.community_roms import get_all_community_roms
    from app.scrapers.ubports import get_ubports_devices
    from app.scrapers.nethunter import get_nethunter_devices
    from app.scrapers.postmarketos import get_postmarketos_devices

    sources = await asyncio.gather(
        get_sourceforge_roms(),
        get_pixelexperience_roms(),
        get_unofficialtwrp_devices(),
        get_all_community_roms(),
        get_gsi_roms(),
        get_extended_roms(),
        get_extra_roms(),
        _roms_from_lineageos(),
        _roms_from_grapheneos(),
        _roms_from_divestos(),
        _roms_from_calyxos(),
        _roms_from_eos(),
        return_exceptions=True,
    )

    # Build lookup table
    lookup: dict[str, list[dict]] = {}

    for source in sources:
        if isinstance(source, Exception) or not source:
            continue
        for item in source:
            codename = (item.get("codename") or "").lower().strip()
            if not codename:
                continue
            normalized = _NORM(codename)
            if normalized not in lookup:
                lookup[normalized] = []
            lookup[normalized].append(item)

    await cache_set(ck, lookup, ttl=7200)
    return lookup


# ── Public API ────────────────────────────────────────────────────────────────

async def get_all_roms(
    q: str | None = None,
    source: str | None = None,
    android_base: str | None = None,
    rom_type: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    """Return paginated ROM list with optional filtering."""
    ck = "roms:all_flat"
    flat = await cache_get(ck)

    if flat is None:
        lookup = await _build_lookup()
        flat = [rom for roms in lookup.values() for rom in roms]
        # Deduplicate by (name, codename)
        seen: set[tuple] = set()
        deduped = []
        for r in flat:
            key = (r.get("name",""), r.get("codename",""))
            if key not in seen:
                seen.add(key)
                deduped.append(r)
        flat = deduped
        await cache_set(ck, flat, ttl=7200)

    roms = list(flat)

    if q:
        ql = q.lower()
        roms = [r for r in roms if
                ql in (r.get("name") or "").lower() or
                ql in (r.get("codename") or "").lower() or
                ql in (r.get("rom_name") or "").lower()]

    if source:
        sl = source.lower()
        roms = [r for r in roms if sl in (r.get("source") or r.get("data_source") or "").lower()]

    if android_base:
        roms = [r for r in roms if (r.get("android_base") or "") == android_base]

    if rom_type:
        roms = [r for r in roms if (r.get("rom_type") or "custom") == rom_type]

    return {
        "total": len(roms),
        "offset": offset,
        "limit": limit,
        "roms": roms[offset: offset + limit],
    }


async def get_roms_for_device(codename: str) -> list[dict]:
    """
    O(1) lookup of all ROMs for a device codename.
    Uses pre-built lookup table — no HTTP calls after first warm-up.
    Also checks LineageOS for official builds.
    """
    ck = f"roms:{codename}"
    if c := await cache_get(ck): return c

    normalized = _NORM(codename)
    lookup = await _build_lookup()

    # Direct lookup
    roms = list(lookup.get(normalized, []))

    # Also check slight variations (e.g. "mido" vs "mido_global")
    for key, val in lookup.items():
        if key != normalized and (key.startswith(normalized) or normalized.startswith(key)):
            for r in val:
                if r not in roms:
                    roms.append(r)

    # Check ubports/nethunter/pmos separately (they have different structures)
    try:
        from app.scrapers.ubports import get_ubports_devices
        from app.scrapers.nethunter import get_nethunter_devices
        from app.scrapers.postmarketos import get_postmarketos_devices
        cn_lower = codename.lower()
        extra = await asyncio.gather(
            get_ubports_devices(),
            get_nethunter_devices(),
            get_postmarketos_devices(),
            return_exceptions=True,
        )
        for source in extra:
            if isinstance(source, Exception):
                continue
            for item in source:
                item_cn = (item.get("codename") or "").lower()
                if item_cn == cn_lower and item not in roms:
                    roms.append(item)
    except Exception:
        pass

    await cache_set(ck, roms, ttl=3600)
    return roms
