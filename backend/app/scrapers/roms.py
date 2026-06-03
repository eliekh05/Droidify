"""Unified ROM lookup — O(1) codename→roms dict built once at startup from all sources."""
import asyncio
import re

from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

# API level → Android version string (live fallback table)
_API_LEVEL_TO_ANDROID: dict[int, str] = {
    16: "4.1", 17: "4.2", 18: "4.3", 19: "4.4", 20: "4.4W",
    21: "5.0", 22: "5.1", 23: "6.0", 24: "7.0", 25: "7.1",
    26: "8.0", 27: "8.1", 28: "9",   29: "10",  30: "11",
    31: "12",  32: "12L", 33: "13",  34: "14",  35: "15",
    36: "16",
}

def _api_to_android(val: str | int | None) -> str:
    """Convert API level or version string to Android version string."""
    if val is None:
        return "unknown"
    try:
        level = int(str(val))
        if level >= 16:
            return _API_LEVEL_TO_ANDROID.get(level, str(level))
        return str(val)
    except (ValueError, TypeError):
        return str(val) if val else "unknown"

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

# Variant alias table — Snapdragon/Exynos pairs and region suffix variants.
# Devices that use different codenames for the same hardware (different SOC or region).
# Source: LineageOS device tree — multiple codenames per device tree.
_VARIANT_MAP: dict[str, list[str]] = {
    # Samsung Snapdragon (qlte) ↔ Exynos (lte) — same physical device, two SOC variants
    'dreamqlte':  ['dreamlte'],    # Galaxy S8
    'dream2qlte': ['dream2lte'],   # Galaxy S8+
    'greatqlte':  ['greatlte'],    # Galaxy Note 8
    # Regional and carrier suffix variants — same device, different market identifier
    'jflte':      ['jfltexx'],     # Galaxy S4 Snapdragon
    'i9500':      ['ja3g', 'i9505'],  # Galaxy S4 Exynos
    'kmini3g':    ['kminilte'],    # Galaxy K zoom
    'gts28ltexx': ['gts28lte'],   # Galaxy Tab S2
    'j7y17lte':   ['j7xelte'],    # Galaxy J7 (2017)
    'j6primelte': ['j6lte'],      # Galaxy J6+
    'a6lte':      ['a6plte'],     # Galaxy A6
    'c5lte':      ['c5'],         # Galaxy C5
}

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
        # Determine GrapheneOS Android version from release filenames
        # Format: {codename}-{version_code}-{build}.zip — version code encodes year/Android ver
        # GrapheneOS targets the latest Pixel Android, currently Android 16
        # Extract from releases file: lines like "caiman-2025123456.zip"
        gos_ver = "unknown"
        try:
            _release_lines = [l for l in r.text.splitlines() if l and not l.startswith("#") and "-" in l]
            if _release_lines:
                # GrapheneOS build codes: YYYYMMDDNN — first 4 digits = year, rest = build
                # We check their website for current Android version
                _gos_page = await fetch(client, "https://grapheneos.org/")
                if _gos_page and _gos_page.status_code == 200:
                    _gos_vm = re.search(r"Android[\s]+([0-9]{2})", _gos_page.text)
                    if _gos_vm:
                        gos_ver = _gos_vm.group(1)
        except Exception:
            pass
        result = [{"name":"GrapheneOS","codename":c,"android_base":_api_to_android(gos_ver),
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
                               "android_base":"unknown","source":"divestos",
                               "rom_type":"privacy","status":"active",
                               "download_url":f"https://divestos.org/pages/devices#{code_m.group(1)}"})
        await cache_set(ck, result, ttl=3600)
        return result
    except Exception:
        return []

async def _roms_from_calyxos() -> list[dict]:
    ck = "roms:calyxos"
    if c := await cache_get(ck): return c
    android_ver = "unknown"  # will be updated from page if found
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
                               "android_base":android_ver,"source":"calyxos",
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
                               "android_base":"unknown","source":"eos",
                               "rom_type":"privacy","status":"active",
                               "download_url":f"https://doc.e.foundation/devices/{m.group(1)}"})
        await cache_set(ck, result, ttl=3600)
        return result
    except Exception:
        return []

async def _of_recs_wrapped() -> list[dict]:
    """Wrap OrangeFox recoveries as ROM-type entries for the lookup."""
    from app.services.http import get_client
    from app.scrapers.recoveries import _fetch_orangefox as _of
    async with get_client() as _c:
        recs = await _of(_c)
    return [{
        **r,
        "rom_type": r.get("rom_type", "recovery"),
        "name": r.get("name", "OrangeFox"),
        "android_base": r.get("android_base", "unknown"),
    } for r in recs]

async def _build_lookup() -> dict[str, list[dict]]:
    """
    Build codename → roms lookup table from all sources.
    This is the heavy operation — runs once, cached 2 hours.
    """
    ck = "roms:lookup_table"
    if c := await cache_get(ck): return c

    from app.scrapers.sourceforge_roms import get_sourceforge_roms
    from app.scrapers.gsi_roms import get_gsi_roms
    from app.scrapers.extended_roms import get_extended_roms
    from app.scrapers.extra_roms import get_extra_roms
    from app.scrapers.customrombay import get_all_customrombay_roms
    from app.scrapers.rom_sources import get_all_rom_sources
    from app.scrapers.twrp_index import get_twrp_index
    from app.scrapers.recoveries import _fetch_orangefox as _of_recs
    from app.scrapers.eosbuilds import get_eosbuilds_roms
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
        get_all_customrombay_roms(),
        get_all_rom_sources(),
        get_twrp_index(),
        get_eosbuilds_roms(),
        _of_recs_wrapped(),
        _roms_from_lineageos(),
        _roms_from_grapheneos(),
        _roms_from_divestos(),
        _roms_from_calyxos(),
        _roms_from_eos(),
        get_ubports_devices(),
        get_nethunter_devices(),
        get_postmarketos_devices(),
        return_exceptions=True,
    )

    lookup: dict[str, list[dict]] = {}

    for source in sources:
        if isinstance(source, Exception) or not source:
            continue
        for item in source:
            codename = (item.get("codename") or "").strip()
            if not codename or codename.lower() in ("gsi", "gsi_arm64", "universal"):
                continue
            cn_lower = codename.lower()
            cn_norm  = _NORM(codename)

            # Store under multiple key variants to handle case mismatches
            # and suffix variants (e.g. h812_usu → also store under h812usu and h812)
            keys_to_add = {cn_lower, cn_norm, codename}
            # Strip numeric/region suffixes: h812_usu → h812
            if "_" in cn_lower:
                keys_to_add.add(cn_lower.rsplit("_", 1)[0])
                keys_to_add.add(_NORM(cn_lower.rsplit("_", 1)[0]))

            for key in keys_to_add:
                k = key.lower() if key else ""
                if not k: continue
                if k not in lookup:
                    lookup[k] = []
                # Avoid duplicates in same key
                if item not in lookup[k]:
                    lookup[k].append(item)

    await cache_set(ck, lookup, ttl=7200)
    return lookup

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
    Tries exact match first, then progressively strips regional/hardware
    suffixes to find the base codename (e.g. a51nsxx → a51).
    """
    ck = f"roms:{codename}"
    if c := await cache_get(ck): return c

    lookup = await _build_lookup()
    cn = codename.lower().strip()

    # 1. Exact match variants
    result = (lookup.get(cn) or lookup.get(_NORM(cn)) or
              lookup.get(codename) or lookup.get(codename.upper()) or [])
    if result:
        await cache_set(ck, result, ttl=7200)
        return result

    # 2a. Variant map — Snapdragon/Exynos pairs + known codename aliases
    # variant aliases defined at module level
    if cn in _VARIANT_MAP:
        for alt in _VARIANT_MAP[cn]:
            result = lookup.get(alt) or lookup.get(_NORM(alt)) or []
            if result:
                await cache_set(ck, result, ttl=7200)
                return result

    # 2b. Progressive suffix stripping
    STRIP = [
        r'(nsxx|nsxxi|nsxxs|nsxxu|nsxxv)$',
        r'(ltexx|ltechn|ltevl|lteskt|ltespr|ltevzw|lteatt|ltecan|ltekor|ltektt|lteusc)$',
        r'(3gxx|3gchn|3gvl|3gktt)$',
        r'(nlte|xlte|ylte|zlte|elte|mlte)$',
        r'(primelte|prime)$',
        r'(duos|plus|neo|mini|pro)$',
        r'(wifi|wifi4g|3g|4g|5g)$',
        r'(xx|xxi|xxu|xxv|xxs)$',
        r'[a-z]{2,4}$',
    ]
    base = cn
    for pattern in STRIP:
        stripped = re.sub(pattern, '', base)
        if stripped and stripped != base and len(stripped) >= 3:
            result = lookup.get(stripped) or lookup.get(_NORM(stripped)) or []
            if result:
                await cache_set(ck, result, ttl=7200)
                return result
            base = stripped  # continue stripping

    await cache_set(ck, [], ttl=3600)
    return []