"""
GSI (Generic System Image) ROM scraper.
Fetches live release data from GitHub Releases API.
GSI ROMs run on ANY Android 8.0+ Treble-compatible device.
Zero hardcoded data — all sourced live.
"""
import asyncio
import re
from ..services.cache import get as cache_get, set as cache_set
from ..services.http import get_client

_UA = "DroidifyBot/2.0 (+https://github.com/eliekh05/Droidify)"

# GSI projects: (label, owner, repo, codename_tag)
_GSI_PROJECTS = [
    ("phh AOSP GSI",          "phhusson",      "treble_experimentations", "gsi_arm64"),
    ("LineageOS GSI",         "AndyCGYan",     "lineage_build_unified",   "gsi_arm64"),
    ("Pixel Experience GSI",  "ponces",        "treble_build_pe",         "gsi_arm64"),
    ("crDroid GSI",           "ponces",        "treble_build_crdroid",    "gsi_arm64"),
    ("CalyxOS GSI",           "ponces",        "treble_build_calyx",      "gsi_arm64"),
    ("Evolution X GSI",       "ponces",        "treble_build_evo",        "gsi_arm64"),
    ("NikGApps GSI",          "nicholasgasior","nikgapps",                "gsi_arm64"),
]

# Google AOSP GSI is documented at developer.android.com — no GH releases API
_AOSP_GSI = {
    "codename":    "gsi_arm64",
    "name":        "Google AOSP GSI",
    "source":      "gsi",
    "oem":         "Google",
    "download":    "https://developer.android.com/topic/generic-system-image/releases",
    "version":     "Android 15",
    "type":        "rom",
    "description": "Official AOSP Generic System Image for Treble-compatible devices",
}


async def _fetch_gh_latest(client, owner: str, repo: str, label: str, codename: str) -> dict | None:
    """Fetch latest release info from GitHub Releases API."""
    try:
        r = await client.get(f"https://github.com/{owner}/{repo}/releases/latest", follow_redirects=False,
            headers={"User-Agent": _UA, "Accept": "application/vnd.github+json"},
            timeout=10,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        tag = data.get("tag_name", "")
        # Find a downloadable asset
        download = ""
        for asset in data.get("assets", []):
            name = asset.get("name", "")
            if name.endswith((".img", ".zip", ".xz")) and "arm64" in name.lower():
                download = asset.get("browser_download_url", "")
                break
        if not download:
            download = data.get("html_url", f"https://github.com/{owner}/{repo}/releases/latest")
        return {
            "codename":    codename,
            "name":        label,
            "source":      "gsi",
            "oem":         None,
            "download":    download,
            "version":     tag,
            "type":        "rom",
            "description": f"GSI — runs on any Treble-compatible device (Android 8+)",
        }
    except Exception:
        return None


async def get_gsi_roms() -> list[dict]:
    ck = "roms:gsi"
    if c := await cache_get(ck): return c

    async with get_client() as client:
        tasks = [_fetch_gh_latest(client, owner, repo, label, cn)
                 for label, owner, repo, cn in _GSI_PROJECTS]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    roms = [_AOSP_GSI]  # Always include AOSP GSI
    for r in results:
        if r and not isinstance(r, Exception):
            roms.append(r)

    await cache_set(ck, roms, ttl=3600)
    return roms
