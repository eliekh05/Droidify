"""Community ROM scrapers — project websites and APIs. No GitHub API calls."""
import asyncio
import re
from bs4 import BeautifulSoup
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client, fetch

_CODENAME_RE = re.compile(r'^[a-z][a-z0-9_]{2,24}$')
_SKIP = frozenset([
    'header','navbar','main','search','footer','content','container',
    'wrapper','body','nav','root','app','download','devices','home',
    'about','contact','all','none','undefined',
])

def _extract_card_ids(html: str) -> list[str]:
    """Extract codenames from card IDs like id='beryllium'."""
    found = re.findall(r'id=["\']([a-z][a-z0-9_]{2,24})["\']', html)
    return [c for c in found if c not in _SKIP and _CODENAME_RE.match(c)]

def _make_rom_entry(name, codename, android_base, description, download_url, source):
    return {
        "name": name, "codename": codename,
        "android_base": android_base, "rom_type": "custom",
        "status": "active", "source": source,
        "description": description,
        "download_url": download_url,
        "official": True,
    }

async def _fetch_crdroid(client) -> list[dict]:
    ck = "roms:crdroid_web"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://crdroid.net/downloads")
        if not r or r.status_code != 200: return []
        codenames = _extract_card_ids(r.text)
        result = [_make_rom_entry(
            "crDroid", cn, "16",
            "Feature-rich LineageOS-based ROM with deep customization",
            f"https://crdroid.net/{cn}/16", "crdroid"
        ) for cn in codenames]
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_evolutionx(client) -> list[dict]:
    ck = "roms:evolutionx_web"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://sourceforge.net/projects/evolution-x/files/")
        if not r or r.status_code != 200: return []
        soup = BeautifulSoup(r.text, "html.parser")
        result = []
        for a in soup.select("tr[id] td.name a"):
            name = a.get_text(strip=True)
            if _CODENAME_RE.match(name):
                result.append(_make_rom_entry(
                    "Evolution X", name, "16",
                    "Pixel-style AOSP ROM with extra features",
                    f"https://sourceforge.net/projects/evolution-x/files/{name}/",
                    "evolution_x"
                ))
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_los_microg(client) -> list[dict]:
    ck = "roms:los_microg"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://download.lineage.microg.org/")
        if not r or r.status_code != 200: return []
        codenames = re.findall(r'href="([a-z][a-z0-9_]{2,24})/"', r.text)
        result = [_make_rom_entry(
            "LineageOS for MicroG", cn, "21",
            "LineageOS with built-in MicroG (no Google Play Services needed)",
            f"https://download.lineage.microg.org/{cn}/", "los_microg"
        ) for cn in codenames if _CODENAME_RE.match(cn)]
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_aospa(client) -> list[dict]:
    ck = "roms:aospa_web"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://aospa.co/downloads")
        if not r or r.status_code != 200: return []
        # AOSPA lists devices with their codenames
        codenames = re.findall(r'/downloads/([a-z][a-z0-9_]{2,24})', r.text)
        codenames = list(set(codenames))
        result = [_make_rom_entry(
            "Paranoid Android", cn, "16",
            "Pioneer of unique Android UI experiences",
            f"https://aospa.co/downloads/{cn}", "aospa"
        ) for cn in codenames if _CODENAME_RE.match(cn)]
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_divestos_web(client) -> list[dict]:
    ck = "roms:divestos_web"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://divestos.org/pages/devices")
        if not r or r.status_code != 200: return []
        soup = BeautifulSoup(r.text, "html.parser")
        result = []
        seen = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            m = re.search(r'/devices/([a-z][a-z0-9_]{2,24})', href)
            if m and m.group(1) not in seen:
                cn = m.group(1)
                seen.add(cn)
                result.append(_make_rom_entry(
                    "DivestOS", cn, "20",
                    "Privacy-focused LineageOS fork with extra hardening",
                    f"https://divestos.org/pages/devices#{cn}", "divestos"
                ))
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_calyxos_web(client) -> list[dict]:
    ck = "roms:calyxos_web"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://calyxos.org/install/devices/")
        if not r or r.status_code != 200: return []
        codenames = re.findall(r'/install/([a-z][a-z0-9_]{2,24})/', r.text)
        codenames = list(set(codenames))
        result = [_make_rom_entry(
            "CalyxOS", cn, "15",
            "Privacy-focused Android with built-in VPN and adblocker",
            f"https://calyxos.org/install/{cn}/", "calyxos"
        ) for cn in codenames if _CODENAME_RE.match(cn)]
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_eos_web(client) -> list[dict]:
    ck = "roms:eos_web"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://doc.e.foundation/devices")
        if not r or r.status_code != 200: return []
        codenames = re.findall(r'/devices/([a-z][a-z0-9_]{2,24})', r.text)
        codenames = list(set(codenames))
        result = [_make_rom_entry(
            "/e/OS", cn, "14",
            "Privacy-focused Google-free Android",
            f"https://doc.e.foundation/devices/{cn}", "eos"
        ) for cn in codenames if _CODENAME_RE.match(cn)]
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_postmarketos_web(client) -> list[dict]:
    ck = "roms:pmos_web"
    if c := await cache_get(ck): return c
    try:
        result = []
        page = 1
        while True:
            r = await client.get(
                f"https://gitlab.com/api/v4/projects/postmarketOS%2Fpmaports/repository/tree"
                f"?ref=master&per_page=100&page={page}&path=device",
                headers={"User-Agent": "DroidifyBot/2.0"}
            )
            if r.status_code != 200: break
            items = r.json()
            if not items: break
            for item in items:
                name = item.get("name", "")
                # device folders: device-vendor-codename
                m = re.match(r'^device-[a-z]+-([a-z][a-z0-9_]{2,30})$', name)
                if m:
                    cn = m.group(1)
                    result.append(_make_rom_entry(
                        "postmarketOS", cn, "linux",
                        "Linux-based OS for old Android devices",
                        f"https://wiki.postmarketos.org/wiki/{name}", "postmarketos"
                    ))
            if len(items) < 100: break
            page += 1
        await cache_set(ck, result, ttl=7200)
        return result
    except Exception:
        return []

async def _fetch_grapheneos_web(client) -> list[dict]:
    ck = "roms:grapheneos_web"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://releases.grapheneos.org/releases")
        if not r or r.status_code != 200: return []
        codenames = list({line.split("-")[0] for line in r.text.splitlines()
                         if line and not line.startswith("#") and "-" in line})
        result = [_make_rom_entry(
            "GrapheneOS", cn, "16",
            "Privacy and security focused OS for Google Pixel devices",
            "https://grapheneos.org/install/web", "grapheneos"
        ) for cn in codenames if _CODENAME_RE.match(cn.lower())]
        await cache_set(ck, result, ttl=3600)
        return result
    except Exception:
        return []

async def get_all_community_roms() -> list[dict]:
    """All community ROMs combined — zero GitHub API calls."""
    ck = "roms:community_all"
    if c := await cache_get(ck): return c

    async with get_client() as client:
        results = await asyncio.gather(
            _fetch_crdroid(client),
            _fetch_evolutionx(client),
            _fetch_los_microg(client),
            _fetch_aospa(client),
            _fetch_divestos_web(client),
            _fetch_calyxos_web(client),
            _fetch_eos_web(client),
            _fetch_postmarketos_web(client),
            _fetch_grapheneos_web(client),
            return_exceptions=True,
        )

    all_roms: list[dict] = []
    for result in results:
        if isinstance(result, list):
            all_roms.extend(result)

    await cache_set(ck, all_roms, ttl=7200)
    return all_roms
