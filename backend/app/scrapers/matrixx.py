"""MatrixxOS ROM scraper — uses GitHub OTA repo."""
import asyncio
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client

MATRIXX_API  = "https://api.github.com/repos/Matrixx-Devices/android_vendor_MatrixxOTA/contents?ref=16.0"
MATRIXX_RAW  = "https://raw.githubusercontent.com/Matrixx-Devices/android_vendor_MatrixxOTA/16.0/{codename}.json"
SKIP         = {"README.md", "Pong.json", "Tetris.json"}
CACHE_KEY    = "matrixx_roms_v1"
TTL          = 7200  # 2 hours

async def get_matrixx_roms() -> list[dict]:
    cached = await cache_get(CACHE_KEY)
    if cached:
        return cached

    roms: list[dict] = []
    async with get_client() as client:
        try:
            r = await client.get(MATRIXX_API, timeout=15)
            r.raise_for_status()
            files = [
                item["name"].replace(".json", "")
                for item in r.json()
                if item.get("type") == "file"
                and item.get("name", "").endswith(".json")
                and item.get("name") not in SKIP
            ]
        except Exception:
            return []

        async def _fetch(codename: str) -> None:
            try:
                url = MATRIXX_RAW.format(codename=codename)
                resp = await client.get(url, timeout=10)
                if resp.status_code != 200:
                    return
                data = resp.json()
                for entry in data.get("response", []):
                    roms.append({
                        "codename":   codename,
                        "rom_name":   f"MatrixxOS {entry.get('version', '')}",
                        "source":     "MatrixxOS",
                        "android":    entry.get("android_version", ""),
                        "type":       entry.get("build_type", "Official"),
                        "url":        entry.get("download", ""),
                        "filename":   entry.get("filename", ""),
                        "size":       entry.get("size", 0),
                        "date":       entry.get("timestamp", 0),
                        "maintainer": entry.get("maintainer", ""),
                        "device":     entry.get("device_name", ""),
                        "oem":        entry.get("oem", ""),
                    })
            except Exception:
                pass

        await asyncio.gather(*[_fetch(cn) for cn in files])

    await cache_set(CACHE_KEY, roms, ttl=TTL)
    return roms


async def get_matrixx_roms_for_device(codename: str) -> list[dict]:
    all_roms = await get_matrixx_roms()
    return [r for r in all_roms if r["codename"].lower() == codename.lower()]
