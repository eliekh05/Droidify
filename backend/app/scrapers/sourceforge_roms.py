"""SourceForge ROM and recovery scraper — show_result=2000 returns all device folders."""
import asyncio
import re
import httpx
from bs4 import BeautifulSoup
from app.services.cache import get as cache_get, set as cache_set

_SF_FILES  = "https://sourceforge.net/projects/{project}/files/?start=0&show_result=2000"
_SF_SEARCH = "https://sourceforge.net/directory/os:android/?q={query}&_=json"

# (sf_slug, rom_name, description, android_version)
_ROM_PROJECTS: list[tuple[str, str, str, str]] = [
    ("crdroid",           "crDroid",           "Feature-rich AOSP with deep customization",    "14"),
    ("evolution-x",       "Evolution X",       "Pixel-style ROM with extra features",           "14"),
    ("havoc-os",          "HavocOS",           "AOSP ROM with extensive feature set",           "13"),
    ("derpfest",          "DerpFest",          "AOSP-based ROM with unique features",           "14"),
    ("superioros",        "SuperiorOS",        "Performance and battery optimized AOSP ROM",    "14"),
    ("xtended",           "XTended",           "AOSP ROM with Pixel-like experience",           "13"),
    ("voltage-os",        "VoltageOS",         "Stable AOSP ROM focused on performance",        "14"),
    ("cosmic-os",         "CosmicOS",          "Clean AOSP-based custom ROM",                  "13"),
    ("nusantaraproject",  "Nusantara Project", "Indonesian AOSP ROM project",                  "13"),
    ("coltos",            "ColtOS",            "AOSP-based ROM with useful features",           "13"),
    ("nameless-aosp",     "Nameless AOSP",     "Minimal, clean AOSP experience",               "14"),
    ("corvus-os",         "CorvusOS",          "Performance-focused AOSP ROM",                  "13"),
    ("liquid-remix",      "Liquid Remix",      "AOSP ROM with smooth animations",              "13"),
    ("blissroms",         "BlissROMs",         "AOSP ROM focused on stability",                "13"),
    ("arrow-os",          "ArrowOS",           "Simple, minimal AOSP-based ROM",               "13"),
    ("paranoid-android",  "Paranoid Android",  "Pioneer of unique Android experiences",         "14"),
    ("cipheros",          "CipherOS",          "Security-focused AOSP ROM",                    "14"),
    ("stellar-os",        "StellarOS",         "Stellar AOSP-based custom ROM",                "13"),
    ("project-blaze",     "ProjectBlaze",      "Fast and stable AOSP ROM",                     "14"),
    ("mokee",             "MoKee",             "Chinese AOSP ROM project",                     "11"),
    ("nitrogen-project",  "NitrogenOS",        "AOSP ROM with Nitrogen features",              "13"),
    ("spark-os",          "SparkOS",           "AOSP ROM with spark of customization",          "13"),
    ("cherish-os",        "CherishOS",         "Cherish your Android experience",              "13"),
    ("alphadroid-project", "AlphaDroid",        "crDroid-based ROM with new look",                "16"),
    ("risingos-revived",   "RisingOS",          "Feature-rich AOSP revival",                      "14"),
    ("axion-aosp",         "AxionAOSP",         "Minimal AOSP with AI features",                  "16"),
    ("project-elixir",     "Project Elixir",    "Minimal UI close to stock Android",              "14"),
    ("mist-os",            "MistOS",            "Clean minimal AOSP ROM",                         "16"),
    ("yaap-devices",       "YAAP",              "Yet Another AOSP Project",                       "14"),
    ("lmo-project",        "LMODroid",          "LineageMicrog-based ROM",                        "12"),
    ("pixel-extended",     "Pixel Extended",    "Stock Android with extra features",              "13"),
    ("waos-official",      "WaveOS",            "Smooth and stable AOSP ROM",                     "14"),
    ("awaken-project",     "AwakenOS",          "AOSP ROM focused on customization",              "14"),
]

_RECOVERY_PROJECTS: list[tuple[str, str, str]] = [
    ("recovery-for-xiaomi-devices", "TWRP for Xiaomi",     "Unofficial TWRP builds for Xiaomi/Redmi/POCO"),
    ("pbrp",                        "PitchBlack Recovery", "PitchBlack Recovery Project — TWRP fork"),
    ("shrp",                        "SkyHawk Recovery",    "SkyHawk Recovery Project — TWRP fork"),

]

_CODENAME_RE     = re.compile(r'^[a-z][a-z0-9_]{2,24}$')
_MODEL_RE        = re.compile(r'^[A-Z]{2,}[0-9A-Z_-]{1,20}$')
_SKIP_EXTENSIONS = re.compile(r'\.(zip|img|gz|xz|7z|tar|md5|sha256?|sha1|txt|xml|json|exe|bat|apk)$', re.I)
_SKIP_NAMES      = frozenset([
    'test','old','build','release','src','lib','doc','tmp','var','usr',
    'etc','opt','bin','sbin','sys','dev','run','stable','alpha','beta',
    'gsi','arm','arm64','x86','x86_64','tools','extras','common',
])

def _parse_devices(html: str) -> list[str]:
    soup  = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="files_list")
    if not table:
        return []
    devices: list[str] = []
    for row in table.find_all("tr"):
        link = row.find("a", href=True)
        if not link:
            continue
        name = link.get_text(strip=True)
        if not name or name in ("Parent folder", "..") or name.startswith("Totals"):
            continue
        if _SKIP_EXTENSIONS.search(name):
            continue
        if " " in name or not (2 < len(name) <= 25):
            continue
        if name.lower() in _SKIP_NAMES:
            continue
        if _CODENAME_RE.match(name) or _MODEL_RE.match(name):
            devices.append(name)
    return list(dict.fromkeys(devices))

async def _fetch_project(client: httpx.AsyncClient, sf_slug: str) -> list[str]:
    """Fetch device list from one SF project. Returns [] on any error."""
    try:
        resp = await client.get(_SF_FILES.replace("{project}", sf_slug))
        if resp.status_code == 200:
            return _parse_devices(resp.text)
    except Exception:
        return []
    return []

async def get_sourceforge_roms() -> list[dict]:
    """
    Fetch all ROM entries from all SF projects concurrently.
    Returns ~1,600 ROM + recovery entries combined.
    Cached 2 hours.
    """
    ck = "roms:sourceforge_all"
    if c := await cache_get(ck):
        return c

    results: list[dict] = []

    async with httpx.AsyncClient(
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"},
        follow_redirects=True,
    ) as client:

        rom_tasks = [_fetch_project(client, slug) for slug, *_ in _ROM_PROJECTS]
        rom_results = await asyncio.gather(*rom_tasks, return_exceptions=True)

        for (sf_slug, rom_name, description, android_ver), devices in zip(_ROM_PROJECTS, rom_results):
            if isinstance(devices, Exception) or not devices:
                continue
            is_active = android_ver in ("14", "15", "16")
            for codename in devices:
                results.append({
                    "name":         rom_name,
                    "codename":     codename,
                    "manufacturer": None,
                    "android_base": android_ver,
                    "rom_type":     "custom",
                    "status":       "active" if is_active else "discontinued",
                    "official":     True,
                    "maintainer":   f"{rom_name} Team",
                    "source_url":   f"https://sourceforge.net/projects/{sf_slug}/files/{codename}/",
                    "download_url": f"https://sourceforge.net/projects/{sf_slug}/files/{codename}/",
                    "data_source":  f"sf_{sf_slug.replace('-','_')}",
                    "rom_name":     rom_name,
                    "description":  description,
                })

        rec_tasks = [_fetch_project(client, slug) for slug, *_ in _RECOVERY_PROJECTS]
        rec_results = await asyncio.gather(*rec_tasks, return_exceptions=True)

        for (sf_slug, rec_name, description), devices in zip(_RECOVERY_PROJECTS, rec_results):
            if isinstance(devices, Exception) or not devices:
                continue
            for codename in devices:
                results.append({
                    "name":         rec_name,
                    "codename":     codename,
                    "manufacturer": None,
                    "android_base": None,
                    "rom_type":     "recovery",
                    "status":       "active",
                    "official":     True,
                    "maintainer":   f"{rec_name} Team",
                    "source_url":   f"https://sourceforge.net/projects/{sf_slug}/files/{codename}/",
                    "download_url": f"https://sourceforge.net/projects/{sf_slug}/files/{codename}/",
                    "data_source":  f"sf_{sf_slug.replace('-','_')}",
                    "rom_name":     rec_name,
                    "description":  description,
                })

    await cache_set(ck, results, ttl=7200)
    return results
