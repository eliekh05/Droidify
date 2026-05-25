import logging
_log = logging.getLogger(__name__)
"""ROM scraper — fetches live ROM data from free public sources.

Download URL policy (verified May 2026):
  LineageOS   → https://download.lineageos.org/devices/{codename}
                (their download page lists actual .zip builds)
  GrapheneOS  → https://grapheneos.org/releases#{codename}
                (factory image: releases.grapheneos.org/{codename}-factory-latest.zip)
  crDroid     → https://crdroid.net/downloads
                (crdroid.net/{codename}/{ver} redirects to homepage — not a download link)
  DivestOS    → https://divestos.org/pages/devices#{codename}
  CalyxOS     → https://calyxos.org/get/
  /e/OS       → https://doc.e.foundation/devices/{codename}
  OrangeFox   → https://orangefox.download/device/{codename}
  TWRP        → https://dl.twrp.me/{codename}/  (lists actual .img files)
"""
import asyncio
import re

from app.services.cache import get, set as cache_set
cache_get = get
from app.services.http import fetch, get_client

# ── Branch → Android version maps ────────────────────────────────────────────
LOS_BRANCH_TO_ANDROID: dict[str, str] = {
    "23.2": "16", "23.1": "16", "23.0": "16",
    "22.2": "15", "22.1": "15", "22.0": "15",
    "21.0": "14", "20.0": "13",
    "19.1": "12L", "19.0": "12",
    "18.1": "11", "17.1": "10",
    "16.0": "9",  "15.1": "8.1",
}

CRDROID_TO_ANDROID: dict[int, str] = {
    14: "16", 13: "15", 12: "16", 11: "15",
    10: "14", 9: "13", 8: "12",
}

# GrapheneOS supported Pixels
GRAPHENEOS_PIXELS = [
    "tokay", "caiman", "komodo", "comet",
    "shiba", "husky", "felix", "tangorpro",
    "lynx", "cheetah", "panther", "bluejay",
    "oriole", "raven",
]

GRAPHENEOS_CHECK_URL   = "https://releases.grapheneos.org/{codename}-stable"
GRAPHENEOS_RELEASE_URL = "https://grapheneos.org/releases#{codename}"
GRAPHENEOS_FACTORY_URL = "https://releases.grapheneos.org/{codename}-factory-latest.zip"

DIVESTOS_DEVICES_URL = "https://divestos.org/pages/devices"
CALYXOS_URL          = "https://calyxos.org/get/"
EOS_DEVICE_URL       = "https://doc.e.foundation/devices/{codename}"

# ── GrapheneOS ────────────────────────────────────────────────────────────────
async def _check_grapheneos(client, codename: str) -> dict | None:
    # GrapheneOS device check is now handled by the dynamic list
    # Just try to build the URL; if invalid, it returns None
    pass
    if not re.match(r'^[a-z][a-z0-9_]+$', codename):
        return None
    ck = f"grapheneos:{codename}"
    cached = await get(ck)
    if cached is not None:
        return cached if cached else None

    resp = await fetch(client, GRAPHENEOS_CHECK_URL.format(codename=codename))
    result = None
    if resp and resp.status_code == 200:
        build_id = resp.text.strip().split()[0] if resp.text.strip() else ""
        result = {
            "name":          "GrapheneOS",
            "slug":          "grapheneos",
            "android_base":  "16",
            "version_label": build_id,
            "maintainer":    "GrapheneOS project",
            "is_official":   True,
            "status":        "active",
            "rom_type":      "custom",
            # source_url = info page, download_urls = direct factory zip
            "source_url":    GRAPHENEOS_RELEASE_URL.format(codename=codename),
            "download_urls": [GRAPHENEOS_FACTORY_URL.format(codename=codename)],
            "source":        "grapheneos_official",
            "description":   "Privacy-focused OS. Direct factory image download.",
        }
    await cache_set(ck, result or {}, ttl=1800)
    return result


# ── crDroid ───────────────────────────────────────────────────────────────────
async def _check_crdroid(client, codename: str) -> dict | None:
    """Check crDroid support via SourceForge index (307 devices, 1 HTTP req total).

    Uses the cached SF device list instead of scraping crdroid.net per-device.
    Avoids 7 sequential HTTP requests per device.
    """
    ck = f"crdroid:{codename}"
    cached = await get(ck)
    if cached is not None:
        return cached if cached else None

    try:
        from app.scrapers.sourceforge_roms import get_sourceforge_roms
        sf_roms = await get_sourceforge_roms()
        cn_lower = codename.lower()
        for r in sf_roms:
            if r.get("data_source") == "sf_crdroid" and (r.get("codename") or "").lower() == cn_lower:
                result = {
                    "name":          "crDroid",
                    "slug":          "crdroid",
                    "android_base":  r.get("android_base", "14"),
                    "version_label": None,
                    "maintainer":    "crDroid Team",
                    "is_official":   True,
                    "status":        "active",
                    "rom_type":      "custom",
                    "source_url":    r.get("source_url"),
                    "download_urls": [r.get("download_url")] if r.get("download_url") else [],
                    "source":        "crdroid_sf",
                    "description":   "crDroid — feature-rich AOSP ROM with deep customization.",
                }
                await cache_set(ck, result, ttl=3600)
                return result
    except Exception:
        pass

    await cache_set(ck, {}, ttl=3600)
    return None


# ── DivestOS ──────────────────────────────────────────────────────────────────
async def _check_divestos(client, codename: str) -> dict | None:
    ck = "divestos_page"
    cached = await get(ck)
    if cached is None:
        resp = await fetch(client, DIVESTOS_DEVICES_URL)
        page = resp.text.lower() if resp and resp.status_code == 200 else ""
        await cache_set(ck, page, ttl=3600)
        cached = page

    if codename.lower() not in cached:
        return None

    dl_url = f"https://divestos.org/pages/devices#{codename}"
    return {
        "name":          "DivestOS",
        "slug":          "divestos",
        "android_base":  None,
        "version_label": None,
        "maintainer":    "Tad (DivestOS project)",
        "is_official":   True,
        "status":        "active",
        "rom_type":      "custom",
        "source_url":    dl_url,
        "download_urls": [dl_url],
        "source":        "divestos_official",
        "description":   "Security-hardened LineageOS fork. Privacy focused.",
    }


# ── CalyxOS ───────────────────────────────────────────────────────────────────
async def _check_calyxos(client, codename: str) -> dict | None:
    ck = "calyxos_page"
    cached = await get(ck)
    if cached is None:
        resp = await fetch(client, CALYXOS_URL)
        page = resp.text.lower() if resp and resp.status_code == 200 else ""
        await cache_set(ck, page, ttl=3600)
        cached = page

    if codename.lower() not in cached:
        return None

    return {
        "name":          "CalyxOS",
        "slug":          "calyxos",
        "android_base":  None,
        "version_label": None,
        "maintainer":    "Calyx Institute",
        "is_official":   True,
        "status":        "active",
        "rom_type":      "custom",
        "source_url":    CALYXOS_URL,
        "download_urls": [CALYXOS_URL],
        "source":        "calyxos_official",
        "description":   "Privacy OS with optional microG and sandboxed Google Play.",
    }


# ── /e/OS ─────────────────────────────────────────────────────────────────────
async def _check_eos(client, codename: str) -> dict | None:
    ck = f"eos:{codename}"
    cached = await get(ck)
    if cached is not None:
        return cached if cached else None

    url = EOS_DEVICE_URL.format(codename=codename)
    resp = await fetch(client, url)
    result = None
    if resp and resp.status_code == 200:
        # /e/OS device page — this IS the install/download guide page
        result = {
            "name":          "/e/OS",
            "slug":          "eos",
            "android_base":  None,
            "version_label": None,
            "maintainer":    "Murena / e Foundation",
            "is_official":   True,
            "status":        "active",
            "rom_type":      "custom",
            "source_url":    url,
            "download_urls": [url],
            "source":        "eos_official",
            "description":   "De-Googled Android with microG. Privacy by default.",
        }
    await cache_set(ck, result or {}, ttl=3600)
    return result


# ── Per-device ROM check ──────────────────────────────────────────────────────
# get_roms_for_device defined below (merged)


# ── Global ROM index ──────────────────────────────────────────────────────────
async def _fetch_grapheneos_devices() -> list[str]:
    """Fetch supported GrapheneOS devices from their live releases.json — no hardcoding."""
    import re as _re
    ck = "grapheneos:devices"
    cached = await get(ck)
    if cached:
        return cached
    try:
        async with get_client() as client:
            r = await client.get(
                "https://grapheneos.org/releases.json",
                headers={"User-Agent": "DroidifyBot/2.0"},
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                devices = [k for k in data.keys() if _re.match(r'^[a-z][a-z0-9_]+$', k)]
                if devices:
                    await cache_set(ck, devices, ttl=7200)
                    return devices
    except Exception:
        pass
    # Minimal fallback only if fetch fails completely
    return ["shiba", "felix", "husky", "akita", "caiman", "tokay", "komodo",
            "comet", "lynx", "cheetah", "panther", "bluejay", "oriole", "raven"]



async def get_all_roms(
    q: str | None = None,
    rom_type: str | None = None,
    android_base: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    ck = "all_roms_index"
    cached = await get(ck)

    if cached is None:
        async with get_client() as client:
            resp = await fetch(client, "https://download.lineageos.org/api/v1/devices")

        all_roms: list[dict] = []

        if resp and resp.status_code == 200:
            for branch, codenames in resp.json().items():
                android = LOS_BRANCH_TO_ANDROID.get(branch, "?")
                for codename in codenames:
                    all_roms.append({
                        "name":          "LineageOS",
                        "slug":          "lineageos",
                        "codename":      codename,
                        "android_base":  android,
                        "version_label": branch,
                        "is_official":   True,
                        "status":        "active",
                        "rom_type":      "custom",
                        # source_url = wiki/info, download_url = actual download page
                        "source_url":    f"https://wiki.lineageos.org/devices/{codename}/",
                        "download_url":  f"https://download.lineageos.org/devices/{codename}",
                        "source":        "lineageos_api",
                    })

        # GrapheneOS — factory image direct downloads (live device list)
        grapheneos_devices = await _fetch_grapheneos_devices()
        for codename in grapheneos_devices:
            all_roms.append({
                "name":          "GrapheneOS",
                "slug":          "grapheneos",
                "codename":      codename,
                "android_base":  "16",
                "version_label": "stable",
                "is_official":   True,
                "status":        "active",
                "rom_type":      "custom",
                "source_url":    f"https://grapheneos.org/releases#{codename}",
                "download_url":  GRAPHENEOS_FACTORY_URL.format(codename=codename),
                "source":        "grapheneos_official",
            })

        # Pixel Experience — 148 devices
        try:
            from app.scrapers.pixelexperience import get_pixelexperience_roms
            pe_roms = await get_pixelexperience_roms()
            all_roms.extend(pe_roms)
        except Exception:
            pass

        # Replicant — old Samsung Galaxy devices (fully free)
        try:
            from app.scrapers.replicant import get_replicant_roms
            rep_roms = await get_replicant_roms()
            all_roms.extend(rep_roms)
        except Exception:
            pass

        # LuneOS — webOS for Android hardware
        try:
            from app.scrapers.luneos import get_luneos_devices
            lune_roms = await get_luneos_devices()
            all_roms.extend(lune_roms)
        except Exception:
            pass

        # GSI ROMs — work on any Treble-compatible device (Android 8+)
        try:
            from app.scrapers.gsi import get_gsi_roms
            gsi_roms = await get_gsi_roms()
            all_roms.extend(gsi_roms)
        except Exception:
            pass

        # SourceForge ROM projects — one request per project, no per-device loops
        try:
            from app.scrapers.sourceforge_roms import get_sourceforge_roms
            sf_roms = await get_sourceforge_roms()
            all_roms.extend(sf_roms)
            _log.info("SF roms: %d", len(sf_roms))
        except Exception as e:
            _log.warning("SF roms failed: %s", e)

        # Unofficial TWRP — 6,204 posts via WordPress REST API
        try:
            from app.scrapers.unofficialtwrp import get_unofficialtwrp_devices
            utwrp = await get_unofficialtwrp_devices()
            all_roms.extend(utwrp)
            _log.info("uTWRP roms: %d", len(utwrp))
        except Exception as e:
            _log.warning("uTWRP roms failed: %s", e)

        # Community ROMs — Evolution X, DerpFest, Project Elixir, ArrowOS, etc.
        try:
            from app.scrapers.community_roms import get_all_community_roms
            community = await get_all_community_roms()
            all_roms.extend(community)
            _log.info("Community roms: %d", len(community))
        except Exception as e:
            _log.warning("Community roms failed: %s", e)

        await cache_set(ck, all_roms, ttl=600)
        cached = all_roms

    roms = list(cached or [])

    if q:
        ql = q.lower()
        qn = re.sub('[-_ ]', '', ql)

        def _rom_matches(r: dict) -> bool:
            name     = (r.get("name")         or "").lower()
            codename = (r.get("codename")      or "").lower()
            mfr      = (r.get("manufacturer")  or "").lower()
            desc     = (r.get("description")   or "").lower()
            return (
                ql in name or ql in codename or ql in mfr or ql in desc
                or qn in re.sub('[-_ ]', '', name)
                or qn in re.sub('[-_ ]', '', codename)
                or codename.startswith(ql)
            )

        roms = [r for r in roms if _rom_matches(r)]
    if rom_type:
        roms = [r for r in roms if r["rom_type"] == rom_type]
    if android_base:
        roms = [r for r in roms if r.get("android_base") == android_base]

    total = len(roms)
    return {"total": total, "offset": offset, "limit": limit,
            "roms": roms[offset: offset + limit]}


# ── New ROM sources ───────────────────────────────────────────────────────────

async def _check_ubports(codename: str) -> dict | None:
    from app.scrapers.ubports import check_ubports_device
    return await check_ubports_device(codename)


async def _check_nethunter(codename: str) -> dict | None:
    from app.scrapers.nethunter import check_nethunter_device
    return await check_nethunter_device(codename)


async def _check_postmarketos(codename: str) -> dict | None:
    from app.scrapers.postmarketos import check_postmarketos_device
    return await check_postmarketos_device(codename)


async def _check_pixelexperience(codename: str) -> dict | None:
    """Check if a device has Pixel Experience support."""
    try:
        from app.scrapers.pixelexperience import get_pixelexperience_roms
        roms = await get_pixelexperience_roms()
        for r in roms:
            if r.get("codename", "").lower() == codename.lower():
                return r
    except Exception:
        pass
    return None


async def get_roms_for_device(codename: str) -> list[dict]:
    """Fetch all available ROMs for a device — all sources merged."""
    import re as _re

    ck = f"roms:{codename}"
    cached = await get(ck)
    if cached is not None:
        return cached
    # Pre-check: if global indexes are not yet warmed, return empty list
    # rather than making 5+ slow HTTP requests that will time out
    sf_cached = await cache_get("roms:sourceforge")
    if sf_cached is None:
        # Indexes not warmed yet — return empty, client will retry
        return []

    cn_lower = codename.lower()
    cn_norm  = _re.sub(r'[-_ .]', '', cn_lower)

    # ── Per-device async checks ───────────────────────────────────────────────
    async with get_client() as client:
        results = await asyncio.gather(
            _check_grapheneos(client, codename),
            _check_crdroid(client, codename),
            _check_divestos(client, codename),
            _check_calyxos(client, codename),
            _check_eos(client, codename),
            return_exceptions=True,
        )
    roms = [r for r in results if r and not isinstance(r, Exception)]

    # ── Cached global indexes (no extra HTTP after first warm-up) ─────────────
    # SourceForge — 26 ROM projects, normalised codename match
    try:
        from app.scrapers.sourceforge_roms import get_sourceforge_roms
        seen = set()
        for r in await get_sourceforge_roms():
            r_cn   = (r.get("codename") or "").lower()
            r_norm = _re.sub(r'[-_ .]', '', r_cn)
            if r_cn == cn_lower or (cn_norm and r_norm == cn_norm):
                key = (r.get("name"), r_cn)
                if key not in seen:
                    seen.add(key)
                    roms.append(r)
    except Exception:
        pass

    # unofficialTWRP — WordPress API index
    try:
        from app.scrapers.unofficialtwrp import get_unofficialtwrp_devices
        for r in await get_unofficialtwrp_devices():
            r_cn   = (r.get("codename") or "").lower()
            r_norm = _re.sub(r'[-_ .]', '', r_cn)
            if r_cn == cn_lower or (cn_norm and r_norm == cn_norm):
                roms.append(r)
    except Exception:
        pass

    # Pixel Experience — GitHub JSON index
    try:
        from app.scrapers.pixelexperience import get_pixelexperience_roms
        for r in await get_pixelexperience_roms():
            r_cn   = (r.get("codename") or "").lower()
            r_norm = _re.sub(r'[-_ .]', '', r_cn)
            if r_cn == cn_lower or (cn_norm and r_norm == cn_norm):
                roms.append(r)
    except Exception:
        pass

    # Ubuntu Touch, NetHunter, postmarketOS
    try:
        extra = await asyncio.gather(
            _check_ubports(codename),
            _check_nethunter(codename),
            _check_postmarketos(codename),
            return_exceptions=True,
        )
        roms += [r for r in extra if r and not isinstance(r, Exception)]
    except Exception:
        pass

    # Community ROMs — Evolution X, DerpFest, Project Elixir, ArrowOS, PixelOS,
    # HavocOS, VoltageOS, AncientOS, AlphaDroid, StagOS, DotOS, LMODroid,
    # BlissROMs, CarbonROM, ProtonAOSP
    try:
        from app.scrapers.community_roms import get_all_community_roms
        community = await get_all_community_roms()
        for r in community:
            r_cn   = (r.get("codename") or "").lower()
            r_norm = _re.sub(r'[-_ .]', '', r_cn)
            if r_cn == cn_lower or (cn_norm and r_norm == cn_norm):
                roms.append(r)
    except Exception:
        pass

    await cache_set(ck, roms, ttl=1800)
    return roms
