"""
tools.py — Android modding tools fetched live from GitHub and official sources.
No hardcoded versions. Live GitHub redirect trick for latest release tags.
"""
import asyncio
import re
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client, fetch

# Tool definitions — config only (owner/repo/category), no version data
_GH_TOOLS = [
    {"name": "Magisk",          "cat": "root",     "owner": "topjohnwu", "repo": "Magisk",
     "desc": "Systemless root with Zygisk support. The community standard for Android rooting.",
     "platforms": ["android"]},
    {"name": "KernelSU",        "cat": "root",     "owner": "tiann",     "repo": "KernelSU",
     "desc": "Kernel-based root for GKI kernels. Hides root at the kernel level.",
     "platforms": ["android"]},
    {"name": "APatch",          "cat": "root",     "owner": "bmax121",   "repo": "APatch",
     "desc": "Kernel patch root supporting GKI and non-GKI kernels.",
     "platforms": ["android"]},
    {"name": "LSPosed",         "cat": "xposed",   "owner": "LSPosed",   "repo": "LSPosed",
     "desc": "Modern Xposed framework via Zygisk. Android 8.1+.",
     "platforms": ["android"]},
    {"name": "Shamiko",         "cat": "xposed",   "owner": "LSPosed",   "repo": "Shamiko",
     "desc": "Zygisk module to hide Magisk and root from detection apps.",
     "platforms": ["android"]},
    {"name": "Heimdall",        "cat": "flashing", "owner": "Benjamin-Dobell", "repo": "Heimdall",
     "desc": "Open-source Samsung Download Mode flash tool. Replaces Odin on Linux/macOS.",
     "platforms": ["windows", "macos", "linux"]},
    {"name": "Fastboot Enhance", "cat": "flashing", "owner": "libxzr",   "repo": "FastbootEnhance",
     "desc": "GUI wrapper for ADB/Fastboot with partition management and A/B slot switching.",
     "platforms": ["windows"]},
    {"name": "Universal Android Debloater", "cat": "utility", "owner": "Universal-Debloater-Alliance",
     "repo": "universal-android-debloater-next-generation",
     "desc": "Remove bloatware from Android devices over ADB — no root required.",
     "platforms": ["windows", "macos", "linux"]},
    {"name": "scrcpy",          "cat": "utility",  "owner": "Genymobile", "repo": "scrcpy",
     "desc": "Mirror and control Android devices from your PC over ADB. No root needed.",
     "platforms": ["windows", "macos", "linux"]},
    {"name": "Zygisk Next",     "cat": "xposed",   "owner": "Dr-TSNG",   "repo": "ZygiskNext",
     "desc": "Standalone Zygisk implementation for KernelSU and APatch.",
     "platforms": ["android"]},
]

_REFERENCE_TOOLS = [
    {"name": "OrangeFox Recovery", "cat": "recovery", "status": "active",
     "desc": "TWRP fork with improved UI, OTA support, and extended file manager.",
     "platforms": ["android"], "url": "https://orangefox.download/"},
    {"name": "PitchBlack Recovery", "cat": "recovery", "status": "active",
     "desc": "TWRP fork with dark theme and enhanced Xiaomi/OnePlus support.",
     "platforms": ["android"], "url": "https://pitchblackrecovery.com/"},
    {"name": "SHRP (SkyHawk Recovery)", "cat": "recovery", "status": "active",
     "desc": "TWRP fork with Addon Manager, terminal emulator, and Magisk patching.",
     "platforms": ["android"], "url": "https://skyhawkrecovery.github.io/"},
    {"name": "MSMDownloadTool", "cat": "flashing", "status": "active",
     "desc": "OnePlus/Qualcomm MSM unbrick tool. Restores fully bricked OnePlus via EDL.",
     "platforms": ["windows"], "url": "https://xdaforums.com/c/oneplus.1628/"},
    {"name": "SuperSU", "cat": "root", "status": "discontinued",
     "desc": "Historical system-level root by Chainfire. Dominant 2012-2017. Replaced by Magisk.",
     "platforms": ["android"], "url": "https://supersuroot.org/"},
    {"name": "Xposed Framework", "cat": "xposed", "status": "discontinued",
     "desc": "Original Xposed by rovo89 for Android 4.x-6.x. Pioneered system-level hooking.",
     "platforms": ["android"], "url": "https://repo.xposed.info/module/de.robv.android.xposed.installer"},
    {"name": "ClockworkMod Recovery", "cat": "recovery", "status": "discontinued",
     "desc": "Historical custom recovery by Koushik Dutta (CWM). Dominant 2010-2014.",
     "platforms": ["android"], "url": "https://www.clockworkmod.com/"},
]


async def _gh_latest(client, owner: str, repo: str) -> dict | None:
    """Get latest release tag via redirect — no API key, no rate limit."""
    try:
        r = await client.get(
            f"https://github.com/{owner}/{repo}/releases/latest",
            follow_redirects=False,
            headers={"User-Agent": "DroidifyBot/2.0"},
            timeout=8,
        )
        if r.status_code in (301, 302):
            tag = r.headers.get("location", "").rstrip("/").split("/")[-1]
            if tag and tag not in ("releases", "latest", repo, ""):
                return {
                    "version":     tag,
                    "release_url": f"https://github.com/{owner}/{repo}/releases/tag/{tag}",
                }
    except Exception:
        pass
    return None


async def _fetch_platform_tools(client) -> dict:
    """Google Platform Tools — permanent dl.google.com URLs always point to latest."""
    ck = "tools:platform_tools_v2"
    if c := await cache_get(ck): return c
    version = None
    try:
        r = await fetch(client, "https://developer.android.com/tools/releases/platform-tools",
                        headers={"User-Agent": "DroidifyBot/2.0"})
        if r and r.status_code == 200:
            m = re.search(r"Platform Tools ([\d.]+)", r.text)
            if m: version = f"v{m.group(1)}"
    except Exception:
        pass
    result = {
        "windows": "https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
        "macos":   "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip",
        "linux":   "https://dl.google.com/android/repository/platform-tools-latest-linux.zip",
        "version": version,
    }
    await cache_set(ck, result, ttl=86400)
    return result


async def _fetch_odin(client) -> dict:
    """Odin — scrape SamMobile for latest version."""
    ck = "tools:odin_sammobile"
    if c := await cache_get(ck): return c
    try:
        from bs4 import BeautifulSoup
        r = await fetch(client, "https://www.sammobile.com/odin/",
                        headers={"User-Agent": "Mozilla/5.0"})
        if not r or r.status_code != 200: raise Exception
        soup    = BeautifulSoup(r.text, "html.parser")
        ver_m   = re.search(r"Odin\s*([\d.]+)", soup.get_text(), re.I)
        version = f"v{ver_m.group(1)}" if ver_m else None
        dl_links = [a["href"] for a in soup.find_all("a", href=True)
                    if "download" in a.get_text(strip=True).lower()
                    and "sammobile" in a["href"]]
        dl_url = dl_links[0] if dl_links else "https://www.sammobile.com/odin/"
        result = {"version": version, "download_url": dl_url}
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return {"version": None, "download_url": "https://www.sammobile.com/odin/"}


async def _fetch_sp_flash(client) -> dict:
    """SP Flash Tool — scrape spflashtools.com for latest."""
    ck = "tools:sp_flash_v2"
    if c := await cache_get(ck): return c
    try:
        from bs4 import BeautifulSoup
        r = await fetch(client, "https://spflashtools.com/category/windows",
                        headers={"User-Agent": "Mozilla/5.0"})
        if not r or r.status_code != 200: raise Exception
        soup  = BeautifulSoup(r.text, "html.parser")
        links = [a["href"] for a in soup.find_all("a", href=True)
                 if re.search(r"sp-flash-tool-v\d+", a["href"], re.I)]
        if not links: raise Exception
        latest = links[0]
        ver_m  = re.search(r"v(\d+)-(\d+)", latest, re.I)
        version = f"v{ver_m.group(1)}.{ver_m.group(2)}" if ver_m else None
        result = {"version": version, "download_url": latest}
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return {"version": None, "download_url": "https://spflashtools.com/category/windows"}


async def _fetch_mi_flash(client) -> dict:
    """Mi Flash Tool — scrape xiaomiflashtool.com."""
    ck = "tools:mi_flash_v2"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://xiaomiflashtool.com/",
                        headers={"User-Agent": "Mozilla/5.0"})
        if not r or r.status_code != 200: raise Exception
        zip_links = re.findall(r"https?://[^\s<>]*miflash[^\s<>]*\.zip", r.text, re.I)
        ver_m = re.search(r"MiFlash[\s_]+([\d.]+)", r.text, re.I) or                 re.search(r"(\d{8})", r.text[:3000])
        version = ver_m.group(1) if ver_m else None
        result = {"version": version, "download_url": zip_links[0] if zip_links else "https://xiaomiflashtool.com/"}
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return {"version": None, "download_url": "https://xiaomiflashtool.com/"}


async def _fetch_qfil(client) -> dict:
    """QFIL — Qualcomm Flash Image Loader from qfiltool.com."""
    ck = "tools:qfil_v2"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://qfiltool.com/",
                        headers={"User-Agent": "Mozilla/5.0"})
        if not r or r.status_code != 200: raise Exception
        ver_m  = re.search(r"QFIL[\s]+([\d.]+)", r.text, re.I)
        links  = re.findall(r"https?://[^\s<>]+\.(?:zip|exe)", r.text, re.I)
        version = ver_m.group(1) if ver_m else None
        result = {"version": version, "download_url": links[0] if links else "https://qfiltool.com/"}
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return {"version": None, "download_url": "https://qfiltool.com/"}


def _platform_label(p: str) -> str:
    return "macOS" if p == "macos" else p.title()


async def get_tools(category: str | None = None) -> list[dict]:
    """Return all tools with fully live versions and download links."""
    ck = f"all_tools_v2:{category or 'all'}"
    if cached := await cache_get(ck): return cached

    async with get_client() as client:
        results = await asyncio.gather(
            _fetch_platform_tools(client),
            _fetch_odin(client),
            _fetch_sp_flash(client),
            _fetch_mi_flash(client),
            _fetch_qfil(client),
            *[_gh_latest(client, t["owner"], t["repo"]) for t in _GH_TOOLS],
            return_exceptions=True,
        )

    pt_data   = results[0] if isinstance(results[0], dict) else {}
    odin_data = results[1] if isinstance(results[1], dict) else {}
    sp_data   = results[2] if isinstance(results[2], dict) else {}
    mi_data   = results[3] if isinstance(results[3], dict) else {}
    qfil_data = results[4] if isinstance(results[4], dict) else {}
    gh_results = results[5:]

    tools: list[dict] = []

    # GitHub tools
    for tool, rel in zip(_GH_TOOLS, gh_results):
        rel = rel if isinstance(rel, dict) else None
        gh_url = f"https://github.com/{tool['owner']}/{tool['repo']}"
        tools.append({
            "name":           tool["name"],
            "category":       tool["cat"],
            "description":    tool["desc"],
            "platforms":      tool["platforms"],
            "status":         "active",
            "official_url":   gh_url,
            "release_url":    rel["release_url"] if rel else gh_url + "/releases",
            "download_urls":  [rel["release_url"]] if rel else [gh_url + "/releases"],
            "latest_version": rel["version"] if rel else None,
            "live_data":      bool(rel),
        })

    # ADB/Fastboot — three platform entries
    for platform in ("windows", "macos", "linux"):
        dl = pt_data.get(platform, f"https://dl.google.com/android/repository/platform-tools-latest-{'darwin' if platform == 'macos' else platform}.zip")
        tools.append({
            "name":           f"ADB / Fastboot ({_platform_label(platform)})",
            "category":       "flashing",
            "description":    f"Official Google platform tools for {_platform_label(platform)} — adb, fastboot, systrace.",
            "platforms":      [platform],
            "status":         "active",
            "official_url":   "https://developer.android.com/tools/releases/platform-tools",
            "release_url":    "https://developer.android.com/tools/releases/platform-tools",
            "download_urls":  [dl],
            "latest_version": pt_data.get("version"),
            "live_data":      bool(pt_data.get("version")),
        })

    # Odin
    tools.append({
        "name":           "Odin",
        "category":       "flashing",
        "description":    "Samsung proprietary Download Mode tool. Flashes AP/BL/CP/CSC partitions. Windows only.",
        "platforms":      ["windows"],
        "status":         "active",
        "official_url":   "https://www.sammobile.com/odin/",
        "release_url":    "https://www.sammobile.com/odin/",
        "download_urls":  [odin_data.get("download_url", "https://www.sammobile.com/odin/")],
        "latest_version": odin_data.get("version"),
        "live_data":      bool(odin_data.get("version")),
    })

    # SP Flash Tool
    tools.append({
        "name":           "SP Flash Tool",
        "category":       "flashing",
        "description":    "MediaTek (MTK) device flashing tool. Used for stock firmware, recovery, and unbrick.",
        "platforms":      ["windows", "linux"],
        "status":         "active",
        "official_url":   "https://spflashtools.com/",
        "release_url":    sp_data.get("download_url", "https://spflashtools.com/category/windows"),
        "download_urls":  [sp_data.get("download_url", "https://spflashtools.com/category/windows")],
        "latest_version": sp_data.get("version"),
        "live_data":      bool(sp_data.get("version")),
    })

    # Mi Flash Tool
    tools.append({
        "name":           "Mi Flash Tool",
        "category":       "flashing",
        "description":    "Xiaomi official fastboot ROM installer for MIUI/HyperOS ROMs on Snapdragon devices.",
        "platforms":      ["windows"],
        "status":         "active",
        "official_url":   "https://xiaomiflashtool.com/",
        "release_url":    mi_data.get("download_url", "https://xiaomiflashtool.com/"),
        "download_urls":  [mi_data.get("download_url", "https://xiaomiflashtool.com/")],
        "latest_version": mi_data.get("version"),
        "live_data":      bool(mi_data.get("version")),
    })

    # QFIL
    tools.append({
        "name":           "QFIL",
        "category":       "flashing",
        "description":    "Qualcomm Flash Image Loader. Emergency EDL/9008 mode flashing for Snapdragon devices.",
        "platforms":      ["windows"],
        "status":         "active",
        "official_url":   "https://qfiltool.com/",
        "release_url":    qfil_data.get("download_url", "https://qfiltool.com/"),
        "download_urls":  [qfil_data.get("download_url", "https://qfiltool.com/")],
        "latest_version": qfil_data.get("version"),
        "live_data":      bool(qfil_data.get("version")),
    })

    # Reference tools (no direct download — link to official site)
    for t in _REFERENCE_TOOLS:
        tools.append({
            "name":           t["name"],
            "category":       t["cat"],
            "description":    t["desc"],
            "platforms":      t["platforms"],
            "status":         t.get("status", "active"),
            "official_url":   t["url"],
            "release_url":    t["url"],
            "download_urls":  [],
            "latest_version": None,
            "live_data":      False,
        })

    tools.sort(key=lambda t: (t["status"] != "active", t["category"], t["name"]))
    if category:
        tools = [t for t in tools if t["category"] == category]

    await cache_set(ck, tools, ttl=1800)
    return tools
