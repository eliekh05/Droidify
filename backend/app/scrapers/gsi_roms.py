"""GSI ROM scraper — Generic System Images for all Project Treble devices (Android 8+)."""
import asyncio
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client

_UA     = "DroidifyBot/2.0 (+https://github.com/eliekh05/Droidify)"

# (name, gh_owner, gh_repo, android_base, description)
_GSI_SOURCES = [
    ("AxionAOSP",          "Doze-off",   "axion_aosp",          "16",
     "AI-powered minimal AOSP GSI — Android 16, all Treble devices"),
    ("LunarisOS",          "Doze-off",   "Lunaris-AOSP_gsi",    "16",
     "Clean AOSP-based GSI — Android 16, all Treble devices"),
    ("Project Infinity-X", "Doze-off",   "ProjectInfinity-X_gsi","16",
     "Minimal stock-like GSI — Android 16, all Treble devices"),
    ("WitAqua",            "Doze-off",   "WitAqua_treble",      "16",
     "Stable AOSP GSI — Android 16, all Treble devices"),
    ("Evolution X",        "Doze-off",   "EvoX_treble",         "16",
     "Pixel-style Evolution X as GSI — Android 16, all Treble devices"),
    ("DerpFest",           "Doze-off",   "Derpfest_treble",     "16",
     "DerpFest AOSP as GSI — Android 16, all Treble devices"),
    ("The Clover Project", "Doze-off",   "Clover_treble",       "16",
     "Clover Project GSI — Android 16, all Treble devices"),
    ("LineageOS",          "MisterZtr",  "LineageOS_gsi",       "15",
     "Unofficial LineageOS GSI with extra patches — Android 15, all Treble devices"),
    ("AOSP",               "ponces",     "treble_aosp",         "15",
     "Pure AOSP GSI — Android 15, all Project Treble devices"),
]

async def _fetch_latest_release(client, owner: str, repo: str) -> dict | None:
    """Fetch latest release tag from GitHub releases page (no API needed)."""
    try:
        # Use the releases/latest redirect — no API rate limit
        r = await client.get(
            f"https://github.com/{owner}/{repo}/releases/latest",
            follow_redirects=False,
            headers={"User-Agent": "DroidifyBot/2.0"},
        )
        if r.status_code in (301, 302):
            location = r.headers.get("location", "")
            tag = location.rstrip("/").split("/")[-1]
            if tag and tag != "releases":
                return {"tag_name": tag, "assets": []}
    except Exception:
        return []
    return None

async def get_gsi_roms() -> list[dict]:
    """
    Fetch all GSI ROM entries.
    Each entry has codename='gsi' — they work on all Treble devices.
    Returns list with latest release info per ROM.
    """
    ck = "roms:gsi_all"
    if c := await cache_get(ck): return c

    async with get_client() as client:
        tasks = [_fetch_latest_release(client, owner, repo)
                 for _, owner, repo, _, _ in _GSI_SOURCES]
        releases = await asyncio.gather(*tasks, return_exceptions=True)

    results: list[dict] = []

    for (name, owner, repo, android_base, description), release in zip(_GSI_SOURCES, releases):
        # Always add the entry even if release fetch failed — link to releases page
        download_url = f"https://github.com/{owner}/{repo}/releases"
        version_label = None

        if isinstance(release, dict) and release.get("tag_name"):
            version_label = release["tag_name"]
            # Get the first .img or .zip asset download URL
            for asset in release.get("assets", []):
                name_lower = asset.get("name", "").lower()
                if name_lower.endswith((".img", ".xz", ".zip", ".7z")):
                    download_url = asset.get("browser_download_url", download_url)
                    break

        results.append({
            "name":          name,
            "codename":      "gsi",
            "model_name":    f"All Project Treble devices — {name} for Android {android_base}+",
            "android_base":  android_base,
            "rom_type":      "gsi",
            "status":        "active",
            "source":        f"github_{owner.lower()}",
            "description":   description,
            "version_label": version_label,
            "download_url":  download_url,
            "source_url":    f"https://github.com/{owner}/{repo}",
            "official":      True,
            "maintainer":    f"{name} Team",
        })

    await cache_set(ck, results, ttl=3600)
    return results
