"""
guides.py — Flashing, rooting and modding guides.

Sources (free, no auth):
  LineageOS Wiki  — install + upgrade guides per device (structured HTML)
  GrapheneOS      — install guide for supported Pixels
  Magisk Docs     — universal root guide
  KernelSU Docs   — kernel-based root guide
  APatch Docs     — alternative root guide
"""
import asyncio
import re
from bs4 import BeautifulSoup
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

LOS_INSTALL = "https://wiki.lineageos.org/devices/{codename}/install/"
LOS_UPGRADE = "https://wiki.lineageos.org/devices/{codename}/upgrade/"
GOS_INSTALL = "https://grapheneos.org/install/web"
MAGISK_URL  = "https://topjohnwu.github.io/Magisk/install.html"
KSU_URL     = "https://kernelsu.org/guide/installation.html"
APATCH_URL  = "https://apatch.dev"

_GOS_DEVICES = frozenset([
    "tokay","caiman","komodo","comet","shiba","husky",
    "felix","tangorpro","lynx","cheetah","panther",
    "bluejay","oriole","raven",
])


def _extract_steps(soup: BeautifulSoup) -> list[str]:
    """Extract ordered steps from wiki HTML."""
    steps = []
    for ol in soup.find_all("ol"):
        for li in ol.find_all("li", recursive=False):
            text = li.get_text(" ", strip=True)
            text = re.sub(r"\s{2,}", " ", text)
            if len(text) > 10:
                steps.append(text[:300])
    return steps[:20]  # cap at 20 steps


def _extract_notes(soup: BeautifulSoup) -> str:
    """Extract warnings/prerequisites from wiki HTML."""
    notes = []
    for el in soup.select(".note, .warning, blockquote, .bs-callout"):
        text = el.get_text(" ", strip=True)
        if text:
            notes.append(text[:200])
    return " ".join(notes[:3])


async def _fetch_los_guide(client, codename: str, guide_type: str) -> dict | None:
    """Fetch and parse a LineageOS wiki guide page."""
    url = LOS_INSTALL.format(codename=codename) if guide_type == "install" \
          else LOS_UPGRADE.format(codename=codename)
    try:
        resp = await fetch(client, url)
        if not resp or resp.status_code != 200:
            return None
        soup  = BeautifulSoup(resp.text, "html.parser")
        title = soup.find("h1") or soup.find("title")
        steps = _extract_steps(soup)
        notes = _extract_notes(soup)
        if not steps:
            return None
        return {
            "guide_type": guide_type,
            "title":      title.get_text(strip=True) if title else f"LineageOS {guide_type.title()} Guide",
            "source":     "LineageOS Wiki",
            "source_url": url,
            "steps":      steps,
            "notes":      notes,
            "codename":   codename,
        }
    except Exception:
        return None


async def get_guides_for_device(
    codename: str,
    manufacturer: str = "",
    guide_type: str | None = None,
) -> list[dict]:
    ck = f"guides:{codename}"
    if c := await cache_get(ck): return c

    guides: list[dict] = []
    cn = codename.lower()

    async with get_client() as client:
        tasks = [
            _fetch_los_guide(client, cn, "install"),
            _fetch_los_guide(client, cn, "upgrade"),
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, dict):
                guides.append(r)

    # GrapheneOS install guide for supported Pixels
    if cn in _GOS_DEVICES:
        guides.append({
            "guide_type": "install",
            "title":      "GrapheneOS Web Installer",
            "source":     "GrapheneOS",
            "source_url": GOS_INSTALL,
            "steps":      [
                "Open https://grapheneos.org/install/web in Chrome/Edge",
                "Connect device in fastboot mode (hold Volume Down + Power)",
                "Follow the web installer — it handles everything automatically",
                "Reboot and complete initial setup",
            ],
            "notes":      "Requires Chrome or Edge browser. WebUSB must be enabled.",
            "codename":   cn,
        })

    # Universal root guides (always include)
    guides.extend([
        {
            "guide_type": "root",
            "title":      "Root with Magisk",
            "source":     "Magisk Docs",
            "source_url": MAGISK_URL,
            "steps":      [
                "Unlock bootloader via fastboot",
                "Download your device's stock boot.img",
                "Patch boot.img with Magisk app",
                "Flash patched boot.img: fastboot flash boot patched_boot.img",
                "Reboot and verify root in Magisk app",
            ],
            "notes": "Requires unlocked bootloader. Back up data first.",
            "codename": cn,
        },
        {
            "guide_type": "root",
            "title":      "Root with KernelSU",
            "source":     "KernelSU",
            "source_url": KSU_URL,
            "steps":      [
                "Requires a KernelSU-supported kernel for your device",
                "Flash KernelSU kernel via recovery or fastboot",
                "Install KernelSU Manager app",
                "Grant root access to apps from Manager",
            ],
            "notes": "Only works if a supported kernel exists for your device.",
            "codename": cn,
        },
        {
            "guide_type": "bootloader-unlock",
            "title":      "Unlock Bootloader",
            "source":     "General Guide",
            "source_url": "https://source.android.com/docs/core/architecture/bootloader/locking_unlocking",
            "steps":      [
                "Enable Developer Options: Settings → About Phone → tap Build Number 7 times",
                "Enable OEM unlocking in Developer Options",
                "Boot to fastboot: adb reboot bootloader",
                "Unlock: fastboot flashing unlock (or fastboot oem unlock for older devices)",
                "Confirm on device screen — this wipes all data",
            ],
            "notes": "This will factory reset your device. Back up everything first.",
            "codename": cn,
        },
    ])

    if guide_type:
        guides = [g for g in guides if g.get("guide_type") == guide_type]

    await cache_set(ck, guides, ttl=3600)
    return guides


async def get_all_guides(limit: int = 50, offset: int = 0) -> dict:
    """Return a list of generic guides not tied to a specific device."""
    guides = [
        {
            "guide_type": "root",
            "title":      "Root with Magisk",
            "source":     "Magisk Docs",
            "source_url": MAGISK_URL,
            "codename":   "universal",
            "steps":      [
                "Unlock bootloader via fastboot",
                "Download your device stock boot.img",
                "Patch boot.img with Magisk app",
                "Flash patched boot: fastboot flash boot patched_boot.img",
                "Reboot and verify in Magisk Manager",
            ],
            "notes": "Requires unlocked bootloader. Wipes data.",
        },
        {
            "guide_type": "root",
            "title":      "Root with KernelSU",
            "source":     "KernelSU",
            "source_url": KSU_URL,
            "codename":   "universal",
            "steps":      [
                "Find a KernelSU-supported kernel for your device",
                "Flash the kernel via recovery or fastboot",
                "Install KernelSU Manager app",
                "Grant root access from the Manager",
            ],
            "notes": "Only works with a supported kernel.",
        },
        {
            "guide_type": "bootloader-unlock",
            "title":      "Unlock Bootloader",
            "source":     "General Guide",
            "source_url": "https://source.android.com/docs/core/architecture/bootloader/locking_unlocking",
            "codename":   "universal",
            "steps":      [
                "Enable Developer Options: Settings → About Phone → tap Build Number 7 times",
                "Enable OEM unlocking in Developer Options",
                "Boot to fastboot: adb reboot bootloader",
                "Run: fastboot flashing unlock",
                "Confirm on device — this wipes all data",
            ],
            "notes": "Wipes all data. Back up everything first.",
        },
        {
            "guide_type": "install",
            "title":      "Flash Custom ROM (General)",
            "source":     "General Guide",
            "source_url": "https://wiki.lineageos.org",
            "codename":   "universal",
            "steps":      [
                "Unlock bootloader",
                "Install a custom recovery (TWRP or OrangeFox)",
                "Boot into recovery",
                "Wipe data, cache, and dalvik",
                "Flash the ROM zip",
                "Flash GApps if needed",
                "Reboot system",
            ],
            "notes": "Always read the device-specific guide on LineageOS wiki.",
        },
    ]
    total = len(guides)
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "guides": guides[offset: offset + limit],
    }
