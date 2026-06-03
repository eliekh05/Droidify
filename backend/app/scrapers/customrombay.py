"""Scraper for customrombay.org — 811 devices with ROMs, recoveries, and Linux distributions."""
import asyncio
import re
from bs4 import BeautifulSoup
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import get_client, fetch

_BASE = "https://customrombay.org"
_INDEX = f"{_BASE}/index.json"
_CODENAME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{1,30}$')

async def _fetch_index(client) -> list[dict]:
    """Fetch the full device index from customrombay.org/index.json."""
    ck = "customrombay:index"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, _INDEX)
        if not r or r.status_code != 200: return []
        data = r.json()
        devices = []
        for entry in data:
            title = entry.get("title", "")
            permalink = entry.get("permalink", "")
            # Title format: "CustomRomBay.org - {codename}"
            m = re.match(r"^CustomRomBay\.org - (.+)$", title)
            if not m or not permalink or permalink in ("/", "/about/", "/contributing/", "/posts/"):
                continue
            codename = m.group(1)
            if _CODENAME_RE.match(codename):
                devices.append({
                    "codename": codename,
                    "url": f"{_BASE}{permalink}",
                    "model": entry.get("contents", ""),
                })
        await cache_set(ck, devices, ttl=43200)  # 12 hour cache
        return devices
    except Exception:
        return []

def _parse_device_page(html: str, codename: str) -> dict:
    """
    Parse a customrombay device page.
    Returns {"roms": [...], "recoveries": [...], "linux": [...]}
    """
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    if not main:
        return {"roms": [], "recoveries": [], "linux": []}

    result = {"roms": [], "recoveries": [], "linux": []}
    current_section = None

    section_map = {
        "custom roms": "roms",
        "custom recoveries": "recoveries",
        "linux distributions": "linux",
    }

    for tag in main.find_all(["h1", "h2", "h3", "table", "p"]):
        if tag.name in ("h1", "h2", "h3"):
            text = tag.get_text(strip=True).lower()
            for key in section_map:
                if key in text:
                    current_section = section_map[key]
                    break
            else:
                current_section = None
            continue

        if tag.name == "table" and current_section:
            for row in tag.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) < 1:
                    continue
                # First cell: ROM name + project link
                name_cell = cells[0]
                name_link = name_cell.find("a", href=True)
                if not name_link:
                    continue
                name = name_link.get_text(strip=True)
                project_url = name_link["href"]

                # Second cell: version/status + download link
                dl_url = project_url  # fallback
                status = "active"
                if len(cells) > 1:
                    dl_link = cells[1].find("a", href=True)
                    if dl_link:
                        dl_url = dl_link["href"]
                        status_text = dl_link.get_text(strip=True).lower()
                        if "discontinued" in status_text or "eol" in status_text:
                            status = "discontinued"
                        elif "non-booting" in status_text or "wip" in status_text:
                            status = "wip"

                if name and dl_url:
                    result[current_section].append({
                        "name": name,
                        "download_url": dl_url,
                        "project_url": project_url,
                        "status": status,
                        "codename": codename,
                        "source": "customrombay",
                    })

    return result

async def _fetch_device(client, codename: str, url: str) -> dict:
    """Fetch and parse a single device page."""
    ck = f"customrombay:device:{codename}"
    if c := await cache_get(ck): return c
    try:
        r = await fetch(client, url)
        if not r or r.status_code != 200:
            return {"roms": [], "recoveries": [], "linux": []}
        data = _parse_device_page(r.text, codename)
        await cache_set(ck, data, ttl=43200)
        return data
    except Exception:
        return {"roms": [], "recoveries": [], "linux": []}

async def get_customrombay_index() -> list[dict]:
    """Return the full device index (codename + URL)."""
    async with get_client() as client:
        return await _fetch_index(client)

async def get_roms_for_codenames(codenames: list[str]) -> list[dict]:
    """
    Fetch ROM/recovery data for a specific list of codenames.
    Only fetches pages for devices in the codename list.
    Returns flat list of ROM entries.
    """
    ck = f"customrombay:batch:{','.join(sorted(codenames[:10]))}"
    if c := await cache_get(ck): return c

    async with get_client() as client:
        index = await _fetch_index(client)
        codename_set = {c.lower() for c in codenames}

        # Find matching entries (case-insensitive codename match)
        matches = [
            entry for entry in index
            if entry["codename"].lower() in codename_set
        ]

        if not matches:
            return []

        pages = await asyncio.gather(
            *[_fetch_device(client, e["codename"], e["url"]) for e in matches],
            return_exceptions=True,
        )

    all_roms = []
    for entry, page in zip(matches, pages):
        if not isinstance(page, dict):
            continue
        for rom in page.get("roms", []):
            all_roms.append({
                "name": rom["name"],
                "codename": entry["codename"],
                "android_base": "unknown",
                "rom_type": "custom",
                "status": rom.get("status", "active"),
                "source": "customrombay",
                "description": f"{rom['name']} for {entry.get('model', entry['codename'])}",
                "download_url": rom["download_url"],
                "source_url": rom.get("project_url", rom["download_url"]),
                "official": False,
            })
        for rec in page.get("recoveries", []):
            all_roms.append({
                "name": rec["name"],
                "codename": entry["codename"],
                "android_base": "unknown",
                "rom_type": "recovery",
                "status": rec.get("status", "active"),
                "source": "customrombay",
                "description": f"{rec['name']} recovery for {entry.get('model', entry['codename'])}",
                "download_url": rec["download_url"],
                "source_url": rec.get("project_url", rec["download_url"]),
                "official": False,
            })
        for linux in page.get("linux", []):
            all_roms.append({
                "name": linux["name"],
                "codename": entry["codename"],
                "android_base": "linux",
                "rom_type": "linux",
                "status": linux.get("status", "active"),
                "source": "customrombay",
                "description": f"{linux['name']} Linux distribution for {entry.get('model', entry['codename'])}",
                "download_url": linux["download_url"],
                "source_url": linux.get("project_url", linux["download_url"]),
                "official": False,
            })

    await cache_set(ck, all_roms, ttl=43200)
    return all_roms

async def get_all_customrombay_roms() -> list[dict]:
    """
    Fetch ROM data for ALL 811 devices on customrombay.org.
    Runs concurrently with rate limiting to avoid overwhelming the server.
    Results cached for 12 hours.
    """
    ck = "customrombay:all_roms"
    if c := await cache_get(ck): return c

    async with get_client() as client:
        index = await _fetch_index(client)
        if not index:
            return []

        BATCH = 20
        all_roms = []

        for i in range(0, len(index), BATCH):
            batch = index[i:i + BATCH]
            pages = await asyncio.gather(
                *[_fetch_device(client, e["codename"], e["url"]) for e in batch],
                return_exceptions=True,
            )
            for entry, page in zip(batch, pages):
                if not isinstance(page, dict):
                    continue
                for section, rom_type in [("roms", "custom"), ("recoveries", "recovery"), ("linux", "linux")]:
                    for item in page.get(section, []):
                        all_roms.append({
                            "name": item["name"],
                            "codename": entry["codename"],
                            "android_base": "linux" if rom_type == "linux" else "unknown",
                            "rom_type": rom_type,
                            "status": item.get("status", "active"),
                            "source": "customrombay",
                            "description": f"{item['name']} for {entry.get('model', entry['codename'])}",
                            "download_url": item["download_url"],
                            "source_url": item.get("project_url", item["download_url"]),
                            "official": False,
                        })

    await cache_set(ck, all_roms, ttl=43200)
    return all_roms
