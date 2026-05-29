"""PostmarketOS scraper.

Source: https://postmarketos.org/
Free, no auth. Lightweight Alpine Linux-based mobile OS.
Device list scraped from their wiki devices page.
"""
import re
from bs4 import BeautifulSoup
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

PMOS_WIKI_URL = "https://wiki.postmarketos.org/wiki/Devices"
PMOS_DL_URL   = "https://postmarketos.org/download/"


async def get_postmarketos_devices() -> list[dict]:
    ck = "pmos_devices"
    cached = await cache_get(ck)
    if cached:
        return cached

    async with get_client() as client:
        resp = await fetch(client, PMOS_WIKI_URL)

    if not resp or resp.status_code != 200:
        return []

    soup  = BeautifulSoup(resp.text, "html.parser")
    # pmOS wiki embeds device data as JSON in a <div data-devices> or in tables
    # Try finding device links in the wiki content
    devices: list[dict] = []

    # Look for links matching /wiki/Device:Manufacturer_Model pattern
    device_links = soup.find_all("a", href=re.compile(r"/wiki/[A-Za-z]+:[A-Za-z]"))
    seen: set[str] = set()

    for link in device_links:
        href  = link.get("href", "")
        title = link.get("title", link.get_text(strip=True))
        if ":" not in title:
            continue
        # Title format: "Manufacturer Model (codename)" or "Manufacturer_Model"
        # href format: /wiki/Samsung_Galaxy_S7_Edge_(hero2lte)
        codename_m = re.search(r"\(([a-z0-9_]+)\)", href)
        codename   = codename_m.group(1) if codename_m else ""

        if not codename or codename in seen:
            continue
        seen.add(codename)

        # Extract manufacturer and model from title
        name = title.replace("_", " ").strip()
        mfr  = _infer_manufacturer(name)

        devices.append({
            "codename":     codename,
            "model_name":   name,
            "manufacturer": mfr,
            "source_url":   f"https://wiki.postmarketos.org{href}",
            "download_url": PMOS_DL_URL,
            "source":       "postmarketos",
        })

    await cache_set(ck, devices, ttl=3600)
    return devices


async def check_postmarketos_device(codename: str) -> dict | None:
    """Return PostmarketOS ROM entry if supported."""
    ck = f"pmos:{codename}"
    cached = await cache_get(ck)
    if cached is not None:
        return cached if cached else None

    # pmOS wiki search per device
    async with get_client() as client:
        search_url = (
            f"https://wiki.postmarketos.org/index.php"
            f"?title=Special:Search&search={codename}&ns0=1"
        )
        resp = await fetch(client, search_url)

    if not resp or resp.status_code != 200:
        await cache_set(ck, {}, ttl=3600)
        return None

    # Check if codename appears in search results as a device page
    if codename.lower() not in resp.text.lower():
        await cache_set(ck, {}, ttl=3600)
        return None

    # Find the direct device wiki page link
    soup   = BeautifulSoup(resp.text, "html.parser")
    result = None

    for link in soup.find_all("a", href=re.compile(rf"{codename}", re.I)):
        href = link.get("href", "")
        if "/wiki/" in href and codename.lower() in href.lower():
            result = {
                "name":          "postmarketOS",
                "slug":          "postmarketos",
                "android_base":  None,
                "version_label": "Edge / Stable",
                "maintainer":    "postmarketOS community",
                "is_official":   True,
                "status":        "active",
                "rom_type":      "linux",
                "source_url":    f"https://wiki.postmarketos.org{href}",
                "download_urls": [PMOS_DL_URL],
                "source":        "postmarketos",
                "description":   (
                    "Alpine Linux-based mobile OS. "
                    "Supports mainline Linux kernel on many devices. "
                    "Interfaces: Phosh, Plasma Mobile, GNOME, XFCE."
                ),
            }
            break

    await cache_set(ck, result or {}, ttl=3600)
    return result


def _infer_manufacturer(name: str) -> str:
    n = name.lower()
    for mfr, kws in {
        "Google":   ["nexus", "pixel"],
        "Samsung":  ["galaxy", "samsung"],
        "OnePlus":  ["oneplus"],
        "Xiaomi":   ["xiaomi", "poco", "redmi"],
        "Fairphone": ["fairphone"],
        "Pine64":   ["pinephone", "pinetab"],
        "Motorola": ["moto"],
        "Sony":     ["xperia"],
        "LG":       ["lg "],
        "Lenovo":   ["lenovo"],
    }.items():
        if any(k in n for k in kws):
            return mfr
    return name.split()[0] if name else "Unknown"
