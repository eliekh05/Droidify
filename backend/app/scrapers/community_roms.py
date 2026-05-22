"""
community_roms.py
=================
Scrapers for 20+ community ROM projects via GitHub API and official APIs.
All data fetched live — zero hardcoded device lists.

Sources:
  Evolution X   — GitHub API: Evolution-X/OTA repo listing
  Project Elixir — SourceForge API
  DerpFest       — GitHub API: DerpFest-AOSP/OTA
  ArrowOS        — GitHub API: ArrowOS/android_vendor_arrow
  RisingOS       — GitHub API scrape
  BlissROMs      — SourceForge API
  DotOS          — GitHub API: DotOS/ota
  crDroid extra  — already in SF scraper
  AncientOS      — GitHub API
  SparkOS        — GitHub API
  VoltageOS      — GitHub API
  HavocOS        — havocos.com API
  CarbonROM      — SourceForge API
  PixelOS        — GitHub API
  ProtonAOSP     — GitHub API
  Afterlife       — SourceForge
  LMODroid       — GitHub API
  AlphaDroid     — GitHub API
  StagOS         — GitHub API
  PixelDust      — GitHub API
  PE Extended    — already in PE scraper
"""

import asyncio
import re
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client

_UA = "DroidifyBot/2.0 (+https://github.com/eliekh05/Droidify)"
_GH_API = "https://api.github.com"


async def _gh_contents(client, owner: str, repo: str, path: str = "") -> list:
    """List files in a GitHub repo directory via API."""
    url = f"{_GH_API}/repos/{owner}/{repo}/contents/{path}"
    try:
        r = await client.get(url, headers={"User-Agent": _UA, "Accept": "application/vnd.github+json"})
        if r.status_code == 200:
            return r.json() if isinstance(r.json(), list) else []
    except Exception:
        pass
    return []


async def _gh_json(client, owner: str, repo: str, branch: str, path: str) -> dict | list | None:
    """Fetch a JSON file from GitHub raw."""
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    try:
        r = await client.get(url, headers={"User-Agent": _UA})
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def _make_rom(codename: str, name: str, source: str, oem: str = "", download: str = "", version: str = "") -> dict:
    return {
        "codename": codename.lower().strip(),
        "name": name,
        "source": source,
        "oem": oem,
        "download": download,
        "version": version,
        "type": "rom",
    }


# ── Evolution X ────────────────────────────────────────────────────────────────
async def get_evolution_x_roms() -> list[dict]:
    ck = "roms:evolution_x"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            # List codenames from OTA repo — each JSON file = one device
            files = await _gh_contents(client, "Evolution-X", "OTA", "")
            for f in files:
                if not f.get("name", "").endswith(".json"):
                    continue
                codename = f["name"].replace(".json", "")
                if not re.match(r"^[a-zA-Z0-9_-]+$", codename):
                    continue
                data = await _gh_json(client, "Evolution-X", "OTA", "udc", f["name"])
                if not data:
                    data = await _gh_json(client, "Evolution-X", "OTA", "tiramisu", f["name"])
                if isinstance(data, dict) and "response" in data:
                    resp = data["response"]
                    entry = resp[0] if resp else {}
                    results.append(_make_rom(
                        codename=codename,
                        name=entry.get("device", codename),
                        source="evolution_x",
                        oem=entry.get("oem", ""),
                        download=entry.get("download", ""),
                        version=entry.get("version", ""),
                    ))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── DerpFest ───────────────────────────────────────────────────────────────────
async def get_derpfest_roms() -> list[dict]:
    ck = "roms:derpfest"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            # DerpFest OTA repo lists devices as JSON files
            for branch in ["11", "12", "13", "14", "15"]:
                files = await _gh_contents(client, "DerpFest-AOSP", "OTA", "")
                for f in (files or []):
                    name = f.get("name", "")
                    if not name.endswith(".json"): continue
                    codename = name.replace(".json", "")
                    if not re.match(r'^[a-zA-Z0-9_-]+$', codename): continue
                    results.append(_make_rom(codename, codename, "derpfest"))
                if results: break
    except Exception:
        pass
    seen = set()
    deduped = []
    for r in results:
        if r["codename"] not in seen:
            seen.add(r["codename"])
            deduped.append(r)
    await cache_set(ck, deduped, ttl=3600)
    return deduped


# ── Project Elixir ─────────────────────────────────────────────────────────────
async def get_project_elixir_roms() -> list[dict]:
    ck = "roms:project_elixir"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "ProjectElixir", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if not re.match(r'^[a-zA-Z0-9_-]+$', codename): continue
                data = await _gh_json(client, "ProjectElixir", "OTA", "main", name)
                entry = {}
                if isinstance(data, dict):
                    resp = data.get("response", [])
                    entry = resp[0] if resp else {}
                results.append(_make_rom(
                    codename=codename,
                    name=entry.get("device", codename),
                    source="project_elixir",
                    oem=entry.get("oem", ""),
                    download=entry.get("download", ""),
                ))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── ArrowOS ────────────────────────────────────────────────────────────────────
async def get_arrowos_roms() -> list[dict]:
    ck = "roms:arrowos"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            # ArrowOS keeps device list as a JSON index
            for url in [
                "https://raw.githubusercontent.com/ArrowOS/arrow_ota/arrow-14.0/devices.json",
                "https://raw.githubusercontent.com/ArrowOS/arrow_ota/arrow-13.0/devices.json",
            ]:
                try:
                    r = await client.get(url, headers={"User-Agent": _UA})
                    if r.status_code == 200:
                        data = r.json()
                        devices = data if isinstance(data, list) else data.get("devices", data.get("response", []))
                        for d in devices:
                            cn = d.get("codename") or d.get("device") or ""
                            if cn and re.match(r'^[a-zA-Z0-9_-]+$', cn):
                                results.append(_make_rom(
                                    codename=cn,
                                    name=d.get("device_name") or d.get("device") or cn,
                                    source="arrowos",
                                    oem=d.get("oem", ""),
                                    download=d.get("download", ""),
                                ))
                        if results: break
                except Exception:
                    continue
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── PixelOS ────────────────────────────────────────────────────────────────────
async def get_pixelos_roms() -> list[dict]:
    ck = "roms:pixelos"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            for branch in ["fourteen", "thirteen", "twelve"]:
                url = f"https://raw.githubusercontent.com/PixelOS-AOSP/official_devices/master/devices.json"
                try:
                    r = await client.get(url, headers={"User-Agent": _UA})
                    if r.status_code == 200:
                        data = r.json()
                        devices = data if isinstance(data, list) else []
                        for d in devices:
                            cn = d.get("codename", "")
                            if cn and re.match(r'^[a-zA-Z0-9_-]+$', cn):
                                results.append(_make_rom(
                                    codename=cn,
                                    name=d.get("device") or cn,
                                    source="pixelos",
                                    oem=d.get("oem", ""),
                                ))
                        if results: break
                except Exception:
                    pass
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── HavocOS ────────────────────────────────────────────────────────────────────
async def get_havocos_roms() -> list[dict]:
    ck = "roms:havocos"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            r = await client.get(
                "https://havocos.com/api/v1/devices",
                headers={"User-Agent": _UA},
                timeout=12,
            )
            if r.status_code == 200:
                data = r.json()
                devices = data if isinstance(data, list) else data.get("data", [])
                for d in devices:
                    cn = d.get("codename") or d.get("device_codename") or ""
                    if cn and re.match(r'^[a-zA-Z0-9_-]+$', cn):
                        results.append(_make_rom(
                            codename=cn,
                            name=d.get("device") or d.get("device_name") or cn,
                            source="havocos",
                            oem=d.get("oem") or d.get("brand") or "",
                        ))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── VoltageOS ──────────────────────────────────────────────────────────────────
async def get_voltage_roms() -> list[dict]:
    ck = "roms:voltageos"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "VoltageOS", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "voltageos"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── AncientOS ─────────────────────────────────────────────────────────────────
async def get_ancientos_roms() -> list[dict]:
    ck = "roms:ancientos"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "AncientOS", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "ancientos"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── AlphaDroid ────────────────────────────────────────────────────────────────
async def get_alphadroid_roms() -> list[dict]:
    ck = "roms:alphadroid"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "AlphaDroidOTA", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "alphadroid"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── StagOS ────────────────────────────────────────────────────────────────────
async def get_stagos_roms() -> list[dict]:
    ck = "roms:stagos"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "StagOS", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "stagos"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── DotOS ─────────────────────────────────────────────────────────────────────
async def get_dotos_roms() -> list[dict]:
    ck = "roms:dotos"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            url = "https://raw.githubusercontent.com/DotOS/ota/dot12/devices.json"
            r = await client.get(url, headers={"User-Agent": _UA})
            if r.status_code == 200:
                data = r.json()
                devices = data if isinstance(data, list) else data.get("devices", [])
                for d in devices:
                    cn = d.get("codename", "")
                    if cn and re.match(r'^[a-zA-Z0-9_-]+$', cn):
                        results.append(_make_rom(
                            codename=cn,
                            name=d.get("name") or cn,
                            source="dotos",
                            oem=d.get("brand", ""),
                        ))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── LMODroid ──────────────────────────────────────────────────────────────────
async def get_lmodroid_roms() -> list[dict]:
    ck = "roms:lmodroid"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "LMODroid", "lmodroid_ota", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "lmodroid"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── BlissROMs ─────────────────────────────────────────────────────────────────
async def get_blissroms_roms() -> list[dict]:
    ck = "roms:blissroms"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            r = await client.get(
                "https://sourceforge.net/projects/blissroms/files?limit=500",
                headers={"User-Agent": _UA, "Accept": "application/json"},
            )
            if r.status_code == 200:
                data = r.json()
                for f in data.get("files", {}).get("dirs", []):
                    codename = f.get("name", "")
                    if codename and re.match(r'^[a-zA-Z0-9_-]+$', codename):
                        results.append(_make_rom(codename, codename, "blissroms"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── CarbonROM ─────────────────────────────────────────────────────────────────
async def get_carbonrom_roms() -> list[dict]:
    ck = "roms:carbonrom"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "CarbonROM", "otaserver", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "carbonrom"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


# ── ProtonAOSP ────────────────────────────────────────────────────────────────
async def get_protonaosp_roms() -> list[dict]:
    ck = "roms:protonaosp"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            url = "https://raw.githubusercontent.com/ProtonAOSP/android_vendor_proton/master/device-info.json"
            r = await client.get(url, headers={"User-Agent": _UA})
            if r.status_code == 200:
                data = r.json()
                for cn, info in (data.items() if isinstance(data, dict) else []):
                    if re.match(r'^[a-zA-Z0-9_-]+$', cn):
                        results.append(_make_rom(
                            codename=cn,
                            name=info.get("name", cn) if isinstance(info, dict) else cn,
                            source="protonaosp",
                        ))
    except Exception:
        pass
    await cache_set(ck, results, ttl=7200)
    return results


# ── Master aggregator ─────────────────────────────────────────────────────────
async def get_all_community_roms() -> list[dict]:
    """Fetch all community ROMs concurrently."""
    ck = "roms:community_all"
    if c := await cache_get(ck): return c

    scrapers = [
        # Established sources
        get_evolution_x_roms(),
        get_derpfest_roms(),
        get_project_elixir_roms(),
        get_arrowos_roms(),
        get_pixelos_roms(),
        get_havocos_roms(),
        get_voltage_roms(),
        get_ancientos_roms(),
        get_alphadroid_roms(),
        get_stagos_roms(),
        get_dotos_roms(),
        get_lmodroid_roms(),
        get_blissroms_roms(),
        get_carbonrom_roms(),
        get_protonaosp_roms(),
        # New from Awesome-CustomROM list
        get_project_matrixx_roms(),
        get_axionos_roms(),
        get_infinity_x_roms(),
        get_risingos_roms(),
        get_paranoid_android_roms(),
        get_nusantara_roms(),
        get_cherish_roms(),
        get_cipheros_roms(),
        get_aosp_extended_roms(),
        get_droidx_ui_roms(),
        get_euclidos_roms(),
    ]

    results_nested = await asyncio.gather(*scrapers, return_exceptions=True)
    all_roms = []
    for r in results_nested:
        if isinstance(r, list):
            all_roms.extend(r)

    await cache_set(ck, all_roms, ttl=1800)
    return all_roms


# ── NEW SCRAPERS FROM Awesome-CustomROM ──────────────────────────────────────

async def get_project_matrixx_roms() -> list[dict]:
    ck = "roms:project_matrixx"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "ProjectMatrixx", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "project_matrixx"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


async def get_axionos_roms() -> list[dict]:
    ck = "roms:axionos"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "AxionAOSP", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "axionos", download=f"https://sourceforge.net/projects/axionaosp/files/{codename}/"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


async def get_infinity_x_roms() -> list[dict]:
    ck = "roms:infinity_x"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "ProjectInfinity-X", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "infinity_x", download=f"https://sourceforge.net/projects/infinity-x/files/{codename}/"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


async def get_risingos_roms() -> list[dict]:
    ck = "roms:risingos"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            for org in ["RisingOS-Revived", "RisingTechOSS"]:
                files = await _gh_contents(client, org, "OTA", "")
                for f in (files or []):
                    name = f.get("name", "")
                    if not name.endswith(".json"): continue
                    codename = name.replace(".json", "")
                    if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                        results.append(_make_rom(codename, codename, "risingos"))
                if results:
                    break
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


async def get_paranoid_android_roms() -> list[dict]:
    ck = "roms:paranoid_android"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "AOSPA", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "paranoid_android"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


async def get_nusantara_roms() -> list[dict]:
    ck = "roms:nusantara"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            r = await client.get("https://nusantararom.org/wp-json/wp/v2/posts?per_page=100&categories=3",
                                 headers={"User-Agent": _UA}, timeout=10)
            if r.status_code == 200:
                for post in r.json():
                    title = post.get("title", {}).get("rendered", "")
                    slug  = post.get("slug", "")
                    if slug and re.match(r'^[a-zA-Z0-9_-]+$', slug):
                        results.append(_make_rom(slug, title or slug, "nusantara",
                                                 download=f"https://nusantararom.org/device/{slug}/"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


async def get_cherish_roms() -> list[dict]:
    ck = "roms:cherishos"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "CherishOS", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "cherishos"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


async def get_cipheros_roms() -> list[dict]:
    ck = "roms:cipheros"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            r = await client.get("https://sourceforge.net/projects/cipheros/files?limit=200",
                                 headers={"User-Agent": _UA, "Accept": "application/json"}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                for d in data.get("files", {}).get("dirs", []):
                    codename = d.get("name", "")
                    if codename and re.match(r'^[a-zA-Z0-9_-]+$', codename):
                        results.append(_make_rom(codename, codename, "cipheros",
                                                 download=f"https://sourceforge.net/projects/cipheros/files/{codename}/"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


async def get_aosp_extended_roms() -> list[dict]:
    ck = "roms:aospextended"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "AospExtended", "OTA_AB", "")
            if not files:
                files = await _gh_contents(client, "AospExtended", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "aospextended",
                                             download=f"https://sourceforge.net/projects/aospextended-rom/files/{codename}/"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


async def get_droidx_ui_roms() -> list[dict]:
    ck = "roms:droidx_ui"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "DroidX-UI", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "droidx_ui"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results


async def get_euclidos_roms() -> list[dict]:
    ck = "roms:euclidos"
    if c := await cache_get(ck): return c
    results = []
    try:
        async with get_client() as client:
            files = await _gh_contents(client, "euclidTeam", "OTA", "")
            for f in (files or []):
                name = f.get("name", "")
                if not name.endswith(".json"): continue
                codename = name.replace(".json", "")
                if re.match(r'^[a-zA-Z0-9_-]+$', codename):
                    results.append(_make_rom(codename, codename, "euclidos"))
    except Exception:
        pass
    await cache_set(ck, results, ttl=3600)
    return results
