"""/e/OS unofficial builds from sourceforge.net/projects/eosbuildsronnz98."""
import asyncio
import re
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client, fetch

_BASE = "https://sourceforge.net/projects/eosbuildsronnz98/files"

# /e/OS branch letter → Android version (same as AOSP codename letters)
_LETTER_TO_ANDROID: dict[str, str] = {
    "n": "7",  "o": "8",  "p": "9",  "q": "10",
    "r": "11", "s": "12", "t": "13", "u": "14",
    "v": "15", "w": "16",
}

_CATEGORIES = [
    "SamsungSmartphones", "SamsungTabs", "XiaomiSmartphones",
    "OtherSmartphones", "LG", "Motorola", "Realme",
    "OnePlus", "Fairphone", "OtherCustomROMS",
]

_CODENAME_RE = re.compile(r'^[a-z][a-z0-9_]{2,30}$')

# Filename pattern: e-2.3-r-20260517-UNOFFICIAL-j1xlte.zip
_FILENAME_RE = re.compile(
    r'e-([\d.]+)-([a-z])-(\d{8})-UNOFFICIAL-([a-z][a-z0-9_]{2,24})\.zip'
)

async def _fetch_category(client, category: str) -> list[dict]:
    ck = f"roms:eosbuilds:{category}"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, f"{_BASE}/{category}/",
                        headers={"User-Agent": "Mozilla/5.0"})
        if not r or r.status_code != 200:
            return []

        # Parse all zip filenames — take the newest build per codename
        latest: dict[str, dict] = {}
        for m in _FILENAME_RE.finditer(r.text):
            eos_ver, letter, date, codename = m.group(1), m.group(2), m.group(3), m.group(4)
            if not _CODENAME_RE.match(codename):
                continue
            existing = latest.get(codename)
            if existing is None or date > existing["date"]:
                latest[codename] = {
                    "date":     date,
                    "eos_ver":  eos_ver,
                    "letter":   letter,
                    "android":  _LETTER_TO_ANDROID.get(letter, "unknown"),
                    "filename": m.group(0),
                    "category": category,
                }

        result = []
        for codename, info in latest.items():
            filename = info["filename"]
            dl_url = f"{_BASE}/{info['category']}/{filename}/download"
            result.append({
                "name":         "/e/OS (Community Build)",
                "codename":     codename,
                "android_base": info["android"],
                "version":      info["eos_ver"],
                "build_date":   info["date"],
                "rom_type":     "privacy",
                "status":       "active",
                "source":       "eosbuilds_community",
                "description":  f"Unofficial /e/OS {info['eos_ver']} (Android {info['android']}) — community build",
                "download_url": dl_url,
                "source_url":   f"{_BASE}/{info['category']}/",
                "official":     False,
            })

        await cache_set(ck, result, ttl=43200)
        return result
    except Exception:
        return []

async def get_eosbuilds_roms() -> list[dict]:
    """Fetch all community /e/OS builds across all device categories."""
    ck = "roms:eosbuilds_all"
    if c := await cache_get(ck): return c

    async with get_client() as client:
        results = await asyncio.gather(
            *[_fetch_category(client, cat) for cat in _CATEGORIES],
            return_exceptions=True,
        )

    seen: set[str] = set()
    all_roms: list[dict] = []
    for r in results:
        if not isinstance(r, list):
            continue
        for rom in r:
            cn = rom["codename"]
            if cn not in seen:
                seen.add(cn)
                all_roms.append(rom)

    await cache_set(ck, all_roms, ttl=43200)
    return all_roms
