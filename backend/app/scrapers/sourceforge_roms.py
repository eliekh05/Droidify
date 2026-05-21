"""
SourceForge ROM + Recovery scraper.

Discovery method: ?show_result=2000 on the files listing page returns
ALL device folders in a single HTML request — no pagination, no per-device
requests, no redirect chains, no bot detection triggers.

SF REST API docs: https://sourceforge.net/api-docs
Key endpoint: /projects/{project}/files/?start=0&show_result=2000

Verified projects (researched 2026-05-19):

ROMs (23 projects, 1276 device entries):
  crDroid       307  crdroid
  HavocOS       190  havoc-os
  DerpFest      166  derpfest
  SuperiorOS     88  superioros
  XTended        71  xtended
  VoltageOS      57  voltage-os
  CosmicOS       52  cosmic-os
  Nusantara      50  nusantaraproject
  ColtOS         46  coltos
  Nameless AOSP  37  nameless-aosp
  CorvusOS       33  corvus-os
  Evolution X   106  evolution-x
  Liquid Remix   16  liquid-remix
  BlissROMs      10  blissroms
  ArrowOS        10  arrow-os
  Paranoid And.   7  paranoid-android
  CipherOS        7  cipheros
  StellarOS       6  stellar-os
  ProjectBlaze    6  project-blaze
  MoKee           4  mokee
  NitrogenOS      3  nitrogen-project
  SparkOS         2  spark-os
  CherishOS       2  cherish-os

Recoveries (3 projects, 388 device entries):
  TWRP-Xiaomi  184  recovery-for-xiaomi-devices
  PitchBlack   119  pbrp
  SkyHawk/SHRP  85  shrp
"""
import re
import httpx
from bs4 import BeautifulSoup
from ..services.cache import get as cache_get, set as cache_set

_SF_FILES = "https://sourceforge.net/projects/{project}/files/?start=0&show_result=2000"

# (sf_slug, rom_name, description, android_version, rom_type)
_ROM_PROJECTS: list[tuple[str, str, str, str, str]] = [
    ("crdroid",       "crDroid",          "Feature-rich AOSP with deep customization",          "14", "custom"),
    ("evolution-x",   "Evolution X",      "Pixel-style ROM with extra features",                 "14", "custom"),
    ("havoc-os",      "HavocOS",          "AOSP ROM with extensive feature set",                 "13", "custom"),
    ("derpfest",      "DerpFest",         "AOSP-based ROM with unique features",                 "13", "custom"),
    ("superioros",    "SuperiorOS",       "Performance and battery optimized AOSP ROM",          "14", "custom"),
    ("xtended",       "XTended",          "AOSP ROM with Pixel-like experience",                 "13", "custom"),
    ("voltage-os",    "VoltageOS",        "Stable AOSP ROM focused on performance",              "14", "custom"),
    ("cosmic-os",     "CosmicOS",         "Clean AOSP-based custom ROM",                        "13", "custom"),
    ("nusantaraproject","Nusantara Project","Indonesian AOSP ROM project",                        "13", "custom"),
    ("coltos",        "ColtOS",           "AOSP-based ROM with useful features",                 "13", "custom"),
    ("nameless-aosp", "Nameless AOSP",    "Minimal, clean AOSP experience",                     "14", "custom"),
    ("corvus-os",     "CorvusOS",         "Performance-focused AOSP ROM",                       "13", "custom"),
    ("liquid-remix",  "Liquid Remix",     "AOSP ROM with smooth animations",                    "13", "custom"),
    ("blissroms",     "BlissROMs",        "AOSP ROM focused on stability and bliss",             "13", "custom"),
    ("arrow-os",      "ArrowOS",          "Simple, minimal AOSP-based ROM",                     "13", "custom"),
    ("paranoid-android","Paranoid Android","Pioneer of unique Android experiences",               "14", "custom"),
    ("cipheros",      "CipherOS",         "Security-focused AOSP ROM",                          "14", "custom"),
    ("stellar-os",    "StellarOS",        "Stellar AOSP-based custom ROM",                      "13", "custom"),
    ("project-blaze", "ProjectBlaze",     "Fast and stable AOSP ROM",                           "14", "custom"),
    ("mokee",         "MoKee",            "Chinese AOSP ROM project (discontinued)",             "11", "custom"),
    ("nitrogen-project","NitrogenOS",     "AOSP ROM with Nitrogen features",                    "13", "custom"),
    ("spark-os",      "SparkOS",          "AOSP ROM with spark of customization",               "13", "custom"),
    ("cherish-os",    "CherishOS",        "Cherish your Android experience",                    "13", "custom"),
]

_RECOVERY_PROJECTS: list[tuple[str, str, str]] = [
    ("recovery-for-xiaomi-devices", "TWRP for Xiaomi",     "Unofficial TWRP builds for Xiaomi/Redmi/POCO devices"),
    ("pbrp",                        "PitchBlack Recovery", "PitchBlack Recovery Project — feature-rich TWRP fork"),
    ("shrp",                        "SkyHawk Recovery",    "SkyHawk Recovery Project — TWRP fork with extra features"),
]

_CODENAME_RE = re.compile(r'^[a-z][a-z0-9_]{2,24}$')           # lowercase codename
_MODEL_RE    = re.compile(r'^[A-Z]{2,}[0-9A-Z_-]{1,20}$')       # model number e.g. SM-G998

_SKIP = frozenset([
    'test', 'old', 'build', 'release', 'src', 'lib', 'doc', 'tmp',
    'var', 'usr', 'etc', 'opt', 'bin', 'sbin', 'sys', 'dev', 'run',
    'stable', 'alpha', 'beta', 'gsi', 'arm', 'arm64', 'x86', 'x86_64',
])

_SKIP_PATTERNS = re.compile(
    r'\.(zip|img|gz|xz|7z|tar|md5|sha256?|sha1|txt|xml|json|exe|bat|apk)$',
    re.IGNORECASE,
)


def _parse_devices(html: str) -> list[str]:
    """Parse device folder names from SF files listing HTML."""
    soup = BeautifulSoup(html, "lxml")
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
        if _SKIP_PATTERNS.search(name):
            continue
        if " " in name or not (2 < len(name) <= 25):
            continue
        if name.lower() in _SKIP:
            continue
        if _CODENAME_RE.match(name) or _MODEL_RE.match(name):
            devices.append(name)

    return list(dict.fromkeys(devices))  # deduplicate preserving order


async def get_sourceforge_roms() -> list[dict]:
    """
    Fetch all ROM entries from SF — one request per project, ~11 requests total.
    Returns ~1,276 ROM entries + ~388 recovery entries.
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

        # ROMs
        for sf_slug, rom_name, description, android_ver, rom_type in _ROM_PROJECTS:
            try:
                resp = await client.get(_SF_FILES.format(project=sf_slug))
                if resp.status_code != 200:
                    continue
                devices = _parse_devices(resp.text)
                is_active = android_ver in ("14", "15")

                for codename in devices:
                    results.append({
                        "name":         rom_name,
                        "codename":     codename,
                        "manufacturer": None,
                        "android_base": android_ver,
                        "rom_type":     rom_type,
                        "status":       "active" if is_active else "discontinued",
                        "official":     True,
                        "maintainer":   f"{rom_name} Team",
                        "source_url":   f"https://sourceforge.net/projects/{sf_slug}/files/{codename}/",
                        "download_url": f"https://sourceforge.net/projects/{sf_slug}/files/{codename}/",
                        "data_source":  f"sf_{sf_slug.replace('-', '_')}",
                        "rom_name":     rom_name,
                        "description":  description,
                    })
            except Exception:
                continue

        # Recoveries
        for sf_slug, rec_name, description in _RECOVERY_PROJECTS:
            try:
                resp = await client.get(_SF_FILES.format(project=sf_slug))
                if resp.status_code != 200:
                    continue
                devices = _parse_devices(resp.text)

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
                        "data_source":  f"sf_{sf_slug.replace('-', '_')}",
                        "rom_name":     rec_name,
                        "description":  description,
                    })
            except Exception:
                continue

    await cache_set(ck, results, ttl=7200)
    return results
