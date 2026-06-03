"""Android root, flashing, and recovery tools — fetched live from GitHub and project pages."""
import asyncio
import re

from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client, fetch

TOOL_REPOS: list[dict] = [
    # Root
    {"name": "Magisk",           "cat": "root",     "owner": "topjohnwu",       "repo": "Magisk",
     "known_version": "v28.1",   "url": "https://github.com/topjohnwu/Magisk",
     "desc": "Systemless root with Zygisk support. The community standard for Android rooting.",
     "platforms": ["android"],   "status": "active"},

    {"name": "KernelSU",         "cat": "root",     "owner": "tiann",           "repo": "KernelSU",
     "known_version": "v1.0.2",  "url": "https://github.com/tiann/KernelSU",
     "desc": "Kernel-based root for GKI kernels. Hides root at the kernel level.",
     "platforms": ["android"],   "status": "active"},

    {"name": "APatch",           "cat": "root",     "owner": "bmax121",         "repo": "APatch",
     "known_version": "10888",   "url": "https://github.com/bmax121/APatch",
     "desc": "Kernel patch-based root supporting GKI and non-GKI kernels.",
     "platforms": ["android"],   "status": "active"},

    {"name": "LSPosed",          "cat": "xposed",   "owner": "LSPosed",         "repo": "LSPosed",
     "known_version": "v1.9.2",  "url": "https://github.com/LSPosed/LSPosed",
     "desc": "Modern Xposed framework via Zygisk/Riru. Android 8.1+.",
     "platforms": ["android"],   "status": "active"},

    {"name": "Shamiko",          "cat": "xposed",   "owner": "LSPosed",         "repo": "Shamiko",
     "known_version": "v1.2.1",  "url": "https://github.com/LSPosed/LSPosed",
     "desc": "Zygisk module to hide Magisk and root from detection apps.",
     "platforms": ["android"],   "status": "active"},

    {"name": "Heimdall",         "cat": "flashing", "owner": "Benjamin-Dobell", "repo": "Heimdall",
     "known_version": "v1.4.2",  "url": "https://github.com/Benjamin-Dobell/Heimdall",
     "desc": "Open-source Samsung Download Mode flash tool. Replaces Odin on Linux/macOS.",
     "platforms": ["windows", "macos", "linux"], "status": "active"},

    {"name": "Fastboot Enhance",  "cat": "flashing", "owner": "libxzr",         "repo": "FastbootEnhance",
     "known_version": "v2.5",    "url": "https://github.com/libxzr/FastbootEnhance",
     "desc": "GUI wrapper for ADB/Fastboot with partition management and A/B slot switching.",
     "platforms": ["windows"],   "status": "active"},
]

async def _fetch_platform_tools(client) -> dict:
    """
    Google Platform Tools — permanent dl.google.com URLs always point to latest.
    Version from developer.android.com release notes page.
    """
    ck = "tools:platform_tools"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://developer.android.com/tools/releases/platform-tools",
                        headers={"User-Agent": "DroidifyBot/2.0"})
        version = None
        if r and r.status_code == 200:
            m = (re.search(r"Platform Tools ([\d.]+)", r.text) or
                 re.search(r"version ([\d.]+)", r.text[:5000], re.I))
            if m:
                version = f"v{m.group(1)}"
    except Exception:
        version = None

    result = {
        "windows": "https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
        "macos":   "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip",
        "linux":   "https://dl.google.com/android/repository/platform-tools-latest-linux.zip",
        "version": version,
    }
    await cache_set(ck, result, ttl=86400)
    return result

async def _fetch_odin(client) -> dict:
    """
    Odin — fetch latest version and download link from samsungodin.com/download/
    Page lists all versioned ZIP files; we take the latest by version number.
    """
    ck = "tools:odin"
    if c := await cache_get(ck): return c
    try:
        from bs4 import BeautifulSoup
        r = await fetch(client, "https://samsungodin.com/download/",
                        headers={"User-Agent": "Mozilla/5.0"})
        if not r or r.status_code != 200:
            raise Exception("unreachable")

        soup = BeautifulSoup(r.text, "html.parser")
        # Find all Odin ZIP download links e.g. Odin_v3.09.zip
        zip_links = [(a["href"], a.get_text(strip=True))
                     for a in soup.find_all("a", href=True)
                     if re.search(r'odin.*\.zip', a["href"], re.I)]

        if not zip_links:
            raise Exception("no zips found")

        def _ver_key(link_text):
            m = re.search(r'v?(\d+)[._](\d+)', link_text[0], re.I)
            return (int(m.group(1)), int(m.group(2))) if m else (0, 0)

        zip_links.sort(key=_ver_key, reverse=True)
        latest_url, _ = zip_links[0]
        ver_m = re.search(r'v?(\d+\.\d+(?:\.\d+)?)', latest_url, re.I)
        version = f"v{ver_m.group(1)}" if ver_m else None

        result = {"download_url": latest_url, "version": version,
                  "all_versions": [url for url, _ in zip_links[:5]]}
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return {"download_url": None, "version": None}

async def _fetch_sp_flash_tool(client) -> dict:
    """
    SP Flash Tool — scrape spflashtools.com/category/windows for latest article.
    Article page contains direct ZIP download link.
    """
    ck = "tools:sp_flash"
    if c := await cache_get(ck): return c
    try:
        from bs4 import BeautifulSoup
        r = await fetch(client, "https://spflashtools.com/category/windows",
                        headers={"User-Agent": "Mozilla/5.0"})
        if not r or r.status_code != 200:
            raise Exception("unreachable")

        soup = BeautifulSoup(r.text, "html.parser")
        # Find latest article link (sorted by date on their site)
        article_links = [a["href"] for a in soup.find_all("a", href=True)
                         if re.search(r'sp-flash-tool-v\d+', a["href"], re.I)]

        if not article_links:
            raise Exception("no articles")

        latest_article = article_links[0]
        ver_m = re.search(r'sp-flash-tool-v(\d+)-(\d+)', latest_article, re.I)
        version = f"v{ver_m.group(1)}.{ver_m.group(2)}" if ver_m else None

        r2 = await fetch(client, latest_article, headers={"User-Agent": "Mozilla/5.0"})
        dl_url = latest_article  # fallback
        if r2 and r2.status_code == 200:
            from bs4 import BeautifulSoup as _BS
            _soup2 = _BS(r2.text, "html.parser")
            for _a in _soup2.find_all("a", href=True):
                if _a["href"].endswith(".zip") and "upload" in _a["href"]:
                    dl_url = _a["href"]
                    break
            if dl_url == latest_article:
                zip_m = re.search(r'https://[^"\'<>\s]+\.zip', r2.text)
                if zip_m:
                    dl_url = zip_m.group(0)

        result = {"download_url": dl_url, "version": version, "article_url": latest_article}
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return {"download_url": None, "version": None}

async def _fetch_mi_flash(client) -> dict:
    """
    Mi Flash Tool — scrape xiaomiflashtool.com for latest version and download.
    """
    ck = "tools:mi_flash"
    if c := await cache_get(ck): return c
    try:
        from bs4 import BeautifulSoup
        r = await fetch(client, "https://xiaomiflashtool.com/",
                        headers={"User-Agent": "Mozilla/5.0"})
        if not r or r.status_code != 200:
            raise Exception("unreachable")

        # Look for download links and version
        zip_links = re.findall(r'https?://[^\s<>]*miflash[^\s<>]*[.]zip', r.text, re.I)
        # Date-based version (YYYYMMDD format used by Xiaomi)
        ver_m = (re.search(r'MiFlash[\s_]+(\d{8})', r.text, re.I) or
                 re.search(r'(\d{8})', r.text[:3000]))
        version = ver_m.group(1) if ver_m else None

        result = {
            "download_url": zip_links[0] if zip_links else None,
            "version": version,
        }
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return {"download_url": None, "version": None}

async def _fetch_qfil(client) -> dict:
    """
    QFIL — Qualcomm Flash Image Loader.
    Fetch version from qfiltool.com.
    """
    ck = "tools:qfil"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, "https://qfiltool.com/",
                        headers={"User-Agent": "Mozilla/5.0"})
        if not r or r.status_code != 200:
            raise Exception("unreachable")

        ver_m = re.search(r'QFIL[\s]+([0-9.]+)', r.text, re.I)
        dl_links = re.findall(r'https?://[^\s<>]+[.](?:zip|exe)', r.text, re.I)
        version = ver_m.group(1) if ver_m else None

        result = {
            "download_url": dl_links[0] if dl_links else None,
            "version": version,
        }
        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return {"download_url": None, "version": None}

async def _fetch_gh_release(client, tool: dict) -> dict | None:
    """Fetch latest release via redirect trick — no API, no rate limit."""
    url = tool.get("url", "")
    if not url or "github.com" not in url:
        return None
    m = re.search(r"github\.com/([^/]+)/([^/#?]+)", url)
    if not m:
        return None
    owner, repo = m.group(1), m.group(2).rstrip("/")
    try:
        r = await client.get(
            f"https://github.com/{owner}/{repo}/releases/latest",
            follow_redirects=False,
            headers={"User-Agent": "DroidifyBot/2.0"},
            timeout=8,
        )
        if r.status_code in (301, 302):
            location = r.headers.get("location", "")
            tag = location.rstrip("/").split("/")[-1]
            if tag and tag not in ("releases", "latest", repo, ""):
                return {
                    "version": tag,
                    "release_url": f"https://github.com/{owner}/{repo}/releases/tag/{tag}",
                    "download_urls": [f"https://github.com/{owner}/{repo}/releases/tag/{tag}"],
                }
    except Exception:
        return []
    return None

async def get_tools(category: str | None = None) -> list[dict]:
    """Return all tools with fully live data — versions, download links, metadata."""
    ck = f"all_tools:{category or 'all'}"
    if cached := await cache_get(ck):
        return cached

    async with get_client() as client:
        pt_data, odin_data, sp_data, mi_data, qfil_data, *gh_results = await asyncio.gather(
            _fetch_platform_tools(client),
            _fetch_odin(client),
            _fetch_sp_flash_tool(client),
            _fetch_mi_flash(client),
            _fetch_qfil(client),
            *[_fetch_gh_release(client, t) for t in TOOL_REPOS],
            return_exceptions=True,
        )

    tools: list[dict] = []

    for tool, release in zip(TOOL_REPOS, gh_results):
        if isinstance(release, Exception):
            release = None
        version = (release.get("version") if release
                   else tool.get("known_version"))
        tools.append({
            "name":           tool["name"],
            "category":       tool["cat"],
            "description":    tool["desc"],
            "platforms":      tool["platforms"],
            "status":         tool["status"],
            "official_url":   tool["url"],
            "download_urls":  release.get("download_urls", []) if release else [],
            "latest_version": version,
            "release_url":    release.get("release_url", tool["url"]) if release else tool["url"],
            "source":         "github_redirect" if release else "known_version_fallback",
            "live_data":      bool(release),
        })

    pt = pt_data if isinstance(pt_data, dict) else {}
    for platform, dl_url in [
        ("windows", pt.get("windows", "https://dl.google.com/android/repository/platform-tools-latest-windows.zip")),
        ("macos",   pt.get("macos",   "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip")),
        ("linux",   pt.get("linux",   "https://dl.google.com/android/repository/platform-tools-latest-linux.zip")),
    ]:
        tools.append({
            "name":           f"ADB / Fastboot ({platform.title()})",
            "category":       "flashing",
            "description":    f"Official Google platform tools for {platform} — adb, fastboot, systrace.",
            "platforms":      [platform],
            "status":         "active",
            "official_url":   "https://developer.android.com/tools/releases/platform-tools",
            "download_urls":  [dl_url],
            "latest_version": pt.get("version"),
            "release_url":    "https://developer.android.com/tools/releases/platform-tools",
            "source":         "google_official",
            "live_data":      bool(pt.get("version")),
        })

    odin = odin_data if isinstance(odin_data, dict) else {}
    tools.append({
        "name":           "Odin",
        "category":       "flashing",
        "description":    "Samsung proprietary Download Mode tool. Flashes AP/BL/CP/CSC partitions.",
        "platforms":      ["windows"],
        "status":         "active",
        "official_url":   "https://samsungodin.com/",
        "download_urls":  [odin.get("download_url")] if odin.get("download_url") else [],
        "latest_version": odin.get("version"),
        "release_url":    "https://samsungodin.com/download/",
        "source":         "samsungodin_scrape" if odin.get("version") else "static_url",
        "live_data":      bool(odin.get("version")),
    })

    sp = sp_data if isinstance(sp_data, dict) else {}
    tools.append({
        "name":           "SP Flash Tool",
        "category":       "flashing",
        "description":    "MediaTek (MTK) device flashing tool. Used for stock firmware, recovery, and unbrick.",
        "platforms":      ["windows", "linux"],
        "status":         "active",
        "official_url":   "https://spflashtools.com/",
        "download_urls":  [sp.get("download_url")] if sp.get("download_url") else [],
        "latest_version": sp.get("version"),
        "release_url":    sp.get("article_url", "https://spflashtools.com/category/windows"),
        "source":         "spflashtools_scrape" if sp.get("version") else "static_url",
        "live_data":      bool(sp.get("version")),
    })

    mi = mi_data if isinstance(mi_data, dict) else {}
    tools.append({
        "name":           "Mi Flash Tool",
        "category":       "flashing",
        "description":    "Xiaomi official fastboot ROM installer for MIUI/HyperOS ROMs on Snapdragon devices.",
        "platforms":      ["windows"],
        "status":         "active",
        "official_url":   "https://xiaomiflashtool.com/",
        "download_urls":  [mi.get("download_url")] if mi.get("download_url") else [],
        "latest_version": mi.get("version"),
        "release_url":    "https://xiaomiflashtool.com/",
        "source":         "xiaomiflashtool_scrape" if mi.get("version") else "static_url",
        "live_data":      bool(mi.get("version")),
    })

    qfil = qfil_data if isinstance(qfil_data, dict) else {}
    tools.append({
        "name":           "QFIL",
        "category":       "flashing",
        "description":    "Qualcomm Flash Image Loader. Emergency EDL/9008 mode flashing for Snapdragon devices.",
        "platforms":      ["windows"],
        "status":         "active",
        "official_url":   "https://qfiltool.com/",
        "download_urls":  [qfil.get("download_url")] if qfil.get("download_url") else [],
        "latest_version": qfil.get("version"),
        "release_url":    "https://qfiltool.com/",
        "source":         "qfiltool_scrape" if qfil.get("version") else "static_url",
        "live_data":      bool(qfil.get("version")),
    })

    REFERENCE_TOOLS = [
        {"name": "MSMDownloadTool", "cat": "flashing", "status": "active",
         "desc": "OnePlus/Qualcomm MSM unbrick tool. Restores fully bricked OnePlus via EDL.",
         "platforms": ["windows"],
         "url": "https://xdaforums.com/c/oneplus.1628/", "dl": None},
        {"name": "OrangeFox Recovery", "cat": "recovery", "status": "active",
         "desc": "TWRP fork with improved UI, built-in OTA support, and extended file manager.",
         "platforms": ["android"],
         "url": "https://orangefox.download/", "dl": None},
        {"name": "PitchBlack Recovery", "cat": "recovery", "status": "active",
         "desc": "TWRP fork with dark theme and enhanced Xiaomi/OnePlus support.",
         "platforms": ["android"],
         "url": "https://pitchblackrecovery.com/", "dl": None},
        {"name": "SkyHawk Recovery (SHRP)", "cat": "recovery", "status": "active",
         "desc": "TWRP fork with Addon Manager, terminal emulator, and Magisk patching.",
         "platforms": ["android"],
         "url": "https://skyhawkrecovery.github.io/", "dl": None},
        {"name": "SuperSU", "cat": "root", "status": "discontinued",
         "desc": "Historical system-level root by Chainfire. Dominant 2012-2017. Replaced by Magisk.",
         "platforms": ["android"], "url": "https://supersuroot.org/", "dl": None},
        {"name": "EdXposed", "cat": "xposed", "status": "discontinued",
         "desc": "Riru-based Xposed for Android 8.1-12. Predecessor to LSPosed.",
         "platforms": ["android"],
         "url": "https://github.com/ElderDrivers/EdXposed", "dl": None},
        {"name": "Xposed Framework", "cat": "xposed", "status": "discontinued",
         "desc": "Original Xposed by rovo89 for Android 4.x-6.x. Pioneered system-level hooking.",
         "platforms": ["android"],
         "url": "https://repo.xposed.info/module/de.robv.android.xposed.installer", "dl": None},
        {"name": "ClockworkMod Recovery", "cat": "recovery", "status": "discontinued",
         "desc": "Historical custom recovery by Koushik Dutta (CWM). Dominant 2010-2014.",
         "platforms": ["android"],
         "url": "https://www.clockworkmod.com/", "dl": None},
        {"name": "Zygisk", "cat": "xposed", "status": "active",
         "desc": "Magisk's built-in module framework. Powers LSPosed, Shamiko, and hundreds of modules.",
         "platforms": ["android"],
         "url": "https://github.com/topjohnwu/Magisk", "dl": None},
    ]

    for t in REFERENCE_TOOLS:
        tools.append({
            "name":           t["name"],
            "category":       t["cat"],
            "description":    t["desc"],
            "platforms":      t["platforms"],
            "status":         t["status"],
            "official_url":   t["url"],
            "download_urls":  [t["dl"]] if t.get("dl") else [],
            "latest_version": None,
            "release_url":    t["url"],
            "source":         "reference",
            "live_data":      False,
        })

    if category:
        tools = [t for t in tools if t["category"] == category]

    tools.sort(key=lambda t: (t["status"] != "active", t["category"], t["name"]))
    await cache_set(ck, tools, ttl=1800)
    return tools
