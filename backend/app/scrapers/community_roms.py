"""
community_roms.py — 30+ community ROM projects via GitHub OTA APIs.

Every ROM project listed here uses a standard GitHub OTA pattern:
  github.com/{org}/official_devices or {org}/OTA
  → list files → extract codenames from JSON filenames

All fetched concurrently. Zero hardcoded device lists.
"""
import asyncio
import re
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client

_GH = "https://api.github.com"
_UA = "DroidifyBot/2.0 (+https://github.com/eliekh05/Droidify)"
_HDR = {"User-Agent": _UA, "Accept": "application/vnd.github+json"}

# (rom_name, gh_owner, ota_repo, branch, android_version, rom_type, description)
_GH_OTA_REPOS = [
    # ── Active 2025 ROMs ────────────────────────────────────────────────────
    ("crDroid",           "crdroidandroid",     "android_vendor_crDroidOTA", "14.0", "14", "custom",
     "Feature-rich LineageOS-based ROM with deep customization"),
    ("Evolution X",       "Evolution-X-Devices","official_devices",          "tiramisu","14", "custom",
     "Pixel-style AOSP ROM with extra features"),
    ("PixelExperience",   "PixelExperience",    "official_devices",          "thirteen","13","custom",
     "AOSP with all Pixel goodies — discontinued April 2024"),
    ("LineageOS",         "LineageOS",          "hudson",                    "master",  "14","custom",
     "The most popular open-source Android ROM"),
    ("ArrowOS",           "ArrowOS-Devices",    "official_devices",          "arrow-13.1","13","custom",
     "Simple, minimal AOSP-based ROM"),
    ("DotOS",             "DotOS-Devices",      "official_devices",          "dot12",   "12","custom",
     "Pixel-like AOSP ROM with dot features"),
    ("PixelPlusUI",       "PixelPlusUI-Devices","official_devices",          "tiramisu","13","custom",
     "Minimal UI close to stock with extra features"),
    ("AlphaDroid",        "AlphaDroid-devices", "OTA",                       "alpha-16.2","16","custom",
     "crDroid-based ROM with new look and optimizations"),
    ("AxionAOSP",         "AxionAOSP",          "official_devices",          "main",    "16","custom",
     "Minimal AOSP with AI-powered features"),
    ("RisingOS",          "RisingOS-Revived",   "official_devices",          "udc",     "14","custom",
     "Feature-rich AOSP revival project"),
    ("LMODroid",          "LMODroid-Devices",   "official_devices",          "lmo-12",  "12","custom",
     "LineageMicrog-based stable ROM"),
    ("Project Elixir",    "ProjectElixir-Devices","official_devices",        "fourteen","14","custom",
     "Minimal UI enhancement close to stock Android"),
    ("Paranoid Android",  "AOSPA",              "vendor_aospa",              "uvite",   "14","custom",
     "Pioneer of unique Android experiences"),
    ("StagOS",            "StagOS-Devices",     "official_devices",          "tiramisu","13","custom",
     "Clean AOSP-based ROM"),
    ("PixelOS",           "PixelOS-AOSP",       "official_devices",          "thirteen","13","custom",
     "The Pixel Project — stock Android with Pixel goodies"),
    ("AncientOS",         "Ancient-Project",    "official_devices",          "ancient-v6","13","custom",
     "AOSP-based ROM with unique ancient theme"),
    ("SparkOS",           "Spark-OS-Devices",   "official_devices",          "12.1",    "12","custom",
     "AOSP ROM with spark of customization"),
    ("VoltageOS",         "VoltageOS-Devices",  "official_devices",          "14",      "14","custom",
     "Stable AOSP ROM focused on performance"),
    ("ProtonAOSP",        "ProtonAOSP",         "official_devices",          "12.1",    "12","custom",
     "Performance-focused minimal AOSP ROM"),
    ("AfterlifeOS",       "Afterlife-Project",  "official_devices",          "thirteen","13","custom",
     "AOSP-based ROM with unique features"),
    ("CarbonROM",         "CarbonROM",          "carbonOTA",                 "cm-14.1", "7", "custom",
     "Based on AOSP with Carbon features"),
    ("WaveOS",            "Wave-OS-Devices",    "official_devices",          "thirteen","13","custom",
     "Smooth and stable AOSP ROM"),
    ("AwakenOS",          "Project-Awaken",     "OTA",                       "fourteen","14","custom",
     "AOSP-based ROM focused on customization"),
    ("IndusOS",           "DroidX-UI",          "DroidX-UI",                 "twelve",  "12","custom",
     "Feature-rich AOSP-based ROM"),
    ("Project 404",       "P-404",              "official_devices",          "main",    "14","custom",
     "AOSP-based ROM with unique features"),
    ("Derp Project",      "DerpFest-AOSP",      "official_devices",          "thirteen","13","custom",
     "AOSP-based ROM with unique Derp features"),
    ("SuperiorOS",        "SuperiorOS-Devices", "official_devices",          "twelve",  "12","custom",
     "Performance and battery optimized AOSP ROM"),
    ("PixelDust",         "pixeldust-devices",  "official_devices",          "twelve",  "12","custom",
     "Pixel-like ROM with dust of extras"),
    ("Pixel Extended",    "PixelExtended",      "official_devices",          "thirteen","13","custom",
     "Stock-like ROM with extra features"),
    ("YAAP",              "yaap",               "devices",                   "main",    "13","custom",
     "Yet Another AOSP Project — minimal and clean"),
]


async def _fetch_gh_ota(client, rom_name: str, owner: str, repo: str,
                        branch: str, android_ver: str, rom_type: str, description: str) -> list[dict]:
    """Fetch device list from a GitHub OTA repo."""
    ck = f"roms:gh_{owner}_{repo}"
    if c := await cache_get(ck): return c

    # Try to list files in the repo root or common subdirs
    devices: set[str] = set()

    for path in ["", "builds", "OTA", "ota", "devices"]:
        url = f"{_GH}/repos/{owner}/{repo}/contents/{path}"
        try:
            r = await client.get(url, headers=_HDR)
            if r.status_code != 200:
                continue
            items = r.json()
            if not isinstance(items, list):
                continue
            for item in items:
                name = item.get("name", "")
                # Extract codename from JSON filename: e.g. beryllium.json → beryllium
                if name.endswith(".json") and not name.startswith("_"):
                    codename = name[:-5].lower()
                    if re.match(r'^[a-z][a-z0-9_]{2,24}$', codename):
                        devices.add(codename)
                # Also check directory names
                elif item.get("type") == "dir":
                    dirname = name.lower()
                    if re.match(r'^[a-z][a-z0-9_]{2,24}$', dirname) and dirname not in (
                        "builds","ota","devices","src","docs","scripts","tools"
                    ):
                        devices.add(dirname)
        except Exception:
            continue
        if devices:
            break

    result = [
        {
            "name":         rom_name,
            "codename":     d,
            "android_base": android_ver,
            "rom_type":     rom_type,
            "status":       "active",
            "source":       owner.lower(),
            "description":  description,
            "download_url": f"https://github.com/{owner}/{repo}",
        }
        for d in devices
    ]
    await cache_set(ck, result, ttl=7200)
    return result


async def get_all_community_roms() -> list[dict]:
    """Fetch all community ROM devices concurrently. Returns merged list."""
    ck = "roms:community_all"
    if c := await cache_get(ck): return c

    async with get_client() as client:
        tasks = [
            _fetch_gh_ota(client, name, owner, repo, branch, ver, rtype, desc)
            for name, owner, repo, branch, ver, rtype, desc in _GH_OTA_REPOS
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    all_roms: list[dict] = []
    for result in results:
        if isinstance(result, list):
            all_roms.extend(result)

    await cache_set(ck, all_roms, ttl=7200)
    return all_roms
