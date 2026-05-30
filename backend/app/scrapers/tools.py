"""Root tools, recoveries, and flashing tools — fetched live.

GitHub API unauthenticated limit: 60 requests/hour per IP.
Some repos may return 403 depending on server-side rate limiting.
All tools include a fallback known_version used when GitHub is unreachable.
"""
import asyncio
import re

from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client

GITHUB_HEADERS  = {
    "Accept":       "application/vnd.github.v3+json",
    "User-Agent":   "DroidifyBot/2.0 (+https://droidify.app; open-source indexer)",
    "X-GitHub-Api-Version": "2022-11-28",
}

# ── Tool registry ─────────────────────────────────────────────────────────────
# known_version = last verified version, used as fallback when GitHub is unreachable
TOOL_REPOS: list[dict] = [
    # Root
    {"name":"Magisk",          "cat":"root",     "owner":"topjohnwu",        "repo":"Magisk",
     "known_version":"v28.1", "url":"https://github.com/topjohnwu/Magisk",
     "desc":"Systemless root with Zygisk support. The community standard for Android rooting.",
     "platforms":["android"], "status":"active"},
    {"name":"KernelSU",        "cat":"root",     "owner":"tiann",            "repo":"KernelSU",
     "known_version":"v1.0.2","url":"https://kernelsu.org/",
     "desc":"Kernel-based root for GKI kernels. Hides root at the kernel level.",
     "platforms":["android"], "status":"active"},
    {"name":"APatch",          "cat":"root",     "owner":"bmax121",          "repo":"APatch",
     "known_version":"10888", "url":"https://github.com/bmax121/APatch",
     "desc":"Kernel patch-based root supporting GKI and non-GKI kernels. Alternative to KernelSU.",
     "platforms":["android"], "status":"active"},
    # Xposed
    {"name":"LSPosed",         "cat":"xposed",   "owner":"LSPosed",          "repo":"LSPosed",
     "known_version":"v1.9.2","url":"https://github.com/LSPosed/LSPosed",
     "desc":"Modern Xposed framework via Zygisk/Riru. Android 8.1+. Massive module ecosystem.",
     "platforms":["android"], "status":"active"},
    {"name":"Shamiko",         "cat":"xposed",   "owner":"LSPosed",          "repo":"Shamiko",
     "known_version":"v1.2.1","url":"https://github.com/LSPosed/LSPosed",
     "desc":"Zygisk module to hide Magisk and root from detection apps.",
     "platforms":["android"], "status":"active"},
    # Flashing
    {"name":"Heimdall",        "cat":"flashing", "owner":"Benjamin-Dobell",  "repo":"Heimdall",
     "known_version":"v1.4.2","url":"https://github.com/Benjamin-Dobell/Heimdall",
     "desc":"Open-source cross-platform Samsung Download Mode flash tool. Replaces Odin on Linux/macOS.",
     "platforms":["windows","macos","linux"], "status":"active"},
    {"name":"Fastboot Enhance", "cat":"flashing","owner":"libxzr",           "repo":"FastbootEnhance",
     "known_version":"v2.5", "url":"https://github.com/libxzr/FastbootEnhance",
     "desc":"GUI wrapper for ADB/Fastboot with partition management and A/B slot switching.",
     "platforms":["windows"], "status":"active"},
]

# Tools without GitHub repos — metadata only, no live version fetching
TOOL_STATIC: list[dict] = [
    {"name":"ADB / Fastboot",      "cat":"flashing",  "status":"active",
     "desc":"Official Google platform tools: sideloading, partition flashing, bootloader unlock. Essential for any Android modding.",
     "platforms":["windows","macos","linux"],
     "url":"https://developer.android.com/tools/releases/platform-tools",
     "dl":"https://developer.android.com/tools/releases/platform-tools"},

    {"name":"Odin",                "cat":"flashing",  "status":"active",
     "desc":"Samsung proprietary Download Mode tool. Flashes AP/BL/CP/CSC partitions on Samsung devices.",
     "platforms":["windows"],
     "url":"https://odindownload.com/",     "dl":"https://odindownload.com/download/"},

    {"name":"SP Flash Tool",       "cat":"flashing",  "status":"active",
     "desc":"MediaTek (MTK) device flashing tool. Used for stock firmware, recovery, and unbrick via BROM/Preloader.",
     "platforms":["windows","linux"],
     "url":"https://spflashtools.com/",    "dl":"https://spflashtools.com/category/windows"},

    {"name":"Mi Flash Tool",       "cat":"flashing",  "status":"active",
     "desc":"Xiaomi official fastboot ROM installer. Required for flashing MIUI global/China ROMs on SD-based Xiaomi/POCO/Redmi.",
     "platforms":["windows"],
     "url":"https://xiaomiflash.com/",     "dl":"https://xiaomiflash.com/"},

    {"name":"QFIL",                "cat":"flashing",  "status":"active",
     "desc":"Qualcomm Flash Image Loader. Emergency EDL/9008 mode flashing for Snapdragon devices. Unbricks hard-bricked phones.",
     "platforms":["windows"],
     "url":"https://qfiltool.com/",        "dl":"https://qfiltool.com/"},

    {"name":"MSMDownloadTool",     "cat":"flashing",  "status":"active",
     "desc":"OnePlus/Qualcomm MSM unbrick tool. Restores fully bricked OnePlus devices to factory firmware via EDL.",
     "platforms":["windows"],
     "url":"https://xdaforums.com/c/oneplus.1628/",   "dl":None},

    {"name":"OrangeFox Recovery",  "cat":"recovery",  "status":"active",
     "desc":"TWRP fork with improved UI, built-in OTA update support, and extended file manager. 159 devices.",
     "platforms":["android"],
     "url":"https://orangefox.download/",  "dl":"https://orangefox.download/en/devices"},

    {"name":"PitchBlack Recovery", "cat":"recovery",  "status":"active",
     "desc":"TWRP fork with dark theme and enhanced Xiaomi/OnePlus support.",
     "platforms":["android"],
     "url":"https://pitchblackrecovery.com/",  "dl":"https://pitchblackrecovery.com/"},

    {"name":"SkyHawk Recovery (SHRP)","cat":"recovery","status":"active",
     "desc":"TWRP fork with built-in Addon Manager, terminal emulator, and Magisk patching support.",
     "platforms":["android"],
     "url":"https://skyhawkrecovery.github.io/",  "dl":"https://skyhawkrecovery.github.io/"},

    # Historical / discontinued
    {"name":"SuperSU",             "cat":"root",      "status":"discontinued",
     "desc":"Historical system-level root manager by Chainfire. Dominant 2012–2017. Replaced by Magisk after going closed-source.",
     "platforms":["android"],
     "url":"https://supersuroot.org/",     "dl":None},

    {"name":"EdXposed",            "cat":"xposed",    "status":"discontinued",
     "desc":"Riru-based Xposed framework for Android 8.1–12. Predecessor to LSPosed. No longer maintained.",
     "platforms":["android"],
     "url":"https://github.com/ElderDrivers/EdXposed",  "dl":None},

    {"name":"Xposed Framework",    "cat":"xposed",    "status":"discontinued",
     "desc":"Original Xposed by rovo89 for Android 4.x–6.x. Pioneered system-level module hooking without ROM modification.",
     "platforms":["android"],
     "url":"https://repo.xposed.info/module/de.robv.android.xposed.installer",  "dl":None},

    {"name":"ClockworkMod Recovery","cat":"recovery", "status":"discontinued",
     "desc":"Historical custom recovery by Koushik Dutta (CWM). Dominant 2010–2014, replaced by TWRP.",
     "platforms":["android"],
     "url":"https://www.clockworkmod.com/",  "dl":None},

    {"name":"Zygisk",              "cat":"xposed",    "status":"active",
     "desc":"Magisk's built-in module framework running in Zygote process space. Powers LSPosed, Shamiko, and hundreds of modules.",
     "platforms":["android"],
     "url":"https://github.com/topjohnwu/Magisk",  "dl":None},
]


async def _fetch_gh_release(client, tool: dict) -> dict:
    """Fetch tool release info using GitHub releases redirect — no API rate limit."""
    tool = dict(tool)
    url = tool.get("url", "")
    if not url or "github.com" not in url:
        return tool
    # Extract owner/repo from URL
    m = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if not m:
        return tool
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
            if tag and tag not in ("releases", "latest", repo):
                tool["version"] = tag
                tool["download_url"] = f"https://github.com/{owner}/{repo}/releases/tag/{tag}"
    except Exception:
        pass
    return tool


async def get_tools(category: str | None = None) -> list[dict]:
    """Return all tools with live GitHub version data where available."""
    ck = f"all_tools:{category or 'all'}"
    cached = await cache_get(ck)
    if cached:
        return cached

    async with get_client() as client:
        gh_results = await asyncio.gather(
            *[_fetch_gh_release(client, t) for t in TOOL_REPOS]
        )

    tools: list[dict] = []

    # GitHub-backed tools
    for t, release in zip(TOOL_REPOS, gh_results):
        version = (
            release.get("latest_version") if release
            else t.get("known_version", "").lstrip("v")
        )
        tools.append({
            "name":           t["name"],
            "category":       t["cat"],
            "description":    t["desc"],
            "platforms":      t["platforms"],
            "status":         t["status"],
            "official_url":   t["url"],
            "download_urls":  release.get("download_urls", []) if release else [],
            "latest_version": version,
            "release_date":   release.get("release_date") if release else None,
            "release_url":    release.get("release_url", t["url"]) if release else t["url"],
            "source":         "github_api" if release else "known_version_fallback",
            "source_url":     f"https://github.com/{t['owner']}/{t['repo']}",
            "live_data":      bool(release),
        })

    # Static tools
    for t in TOOL_STATIC:
        tools.append({
            "name":           t["name"],
            "category":       t["cat"],
            "description":    t["desc"],
            "platforms":      t["platforms"],
            "status":         t["status"],
            "official_url":   t["url"],
            "download_urls":  [t["dl"]] if t.get("dl") else [],
            "latest_version": None,
            "release_date":   None,
            "release_url":    t["url"],
            "source":         "official_page",
            "source_url":     t["url"],
            "live_data":      False,
        })

    if category:
        tools = [t for t in tools if t["category"] == category]

    # Sort: active → discontinued, then alphabetically within category
    tools.sort(key=lambda t: (t["status"] != "active", t["category"], t["name"]))

    await cache_set(ck, tools, ttl=1800)
    return tools
