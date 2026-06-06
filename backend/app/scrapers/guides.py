"""
Guides scraper — device-specific and universal Android modding guides.
Order: Unlock Bootloader → Install Recovery → Install ROM → Root → Restore → Buy/Sell
"""
import asyncio
import re
from bs4 import BeautifulSoup
from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

LOS_INSTALL = "https://wiki.lineageos.org/devices/{codename}/install/"
LOS_UPGRADE  = "https://wiki.lineageos.org/devices/{codename}/upgrade/"

_GOS_DEVICES = frozenset([
    "tokay","caiman","komodo","comet","shiba","husky",
    "felix","tangorpro","lynx","cheetah","panther",
    "bluejay","oriole","raven",
])

_ORDER = {
    "bootloader-unlock": 0,
    "install-recovery":  1,
    "install-rom":       2,
    "root":              3,
    "restore":           4,
    "sell-buy":          5,
}

def _sort(guides):
    return sorted(guides, key=lambda g: _ORDER.get(g.get("guide_type"), 99))

def _extract_steps(soup):
    steps = []
    for ol in soup.find_all("ol"):
        for li in ol.find_all("li", recursive=False):
            text = re.sub(r"\s{2,}", " ", li.get_text(" ", strip=True))
            if len(text) > 10:
                steps.append(text[:300])
    return steps[:20]

def _extract_notes(soup):
    parts = []
    for el in soup.select(".note, .warning, blockquote, .bs-callout"):
        t = el.get_text(" ", strip=True)
        if t: parts.append(t[:200])
    return " ".join(parts[:2])

async def _fetch_los(client, codename, gtype):
    url = LOS_INSTALL.replace("{codename}", codename) if gtype == "install-rom" \
          else LOS_UPGRADE.replace("{codename}", codename)
    try:
        r = await fetch(client, url)
        if not r or r.status_code != 200: return None
        soup  = BeautifulSoup(r.text, "html.parser")
        title = soup.find("h1") or soup.find("title")
        steps = _extract_steps(soup)
        if not steps: return None
        return {
            "guide_type": gtype,
            "title":      title.get_text(strip=True) if title else "LineageOS Guide",
            "source":     "LineageOS Wiki",
            "steps":      steps,
            "notes":      _extract_notes(soup),
            "codename":   codename,
        }
    except Exception:
        return None


def _g_bootloader(cn):
    return {
        "guide_type": "bootloader-unlock",
        "title":      "Unlock Bootloader",
        "source":     "Universal",
        "codename":   cn,
        "steps": [
            "Back up all data — unlocking factory resets your device",
            "Enable Developer Options: Settings → About Phone → tap Build Number 7 times",
            "Enable OEM Unlocking in Developer Options",
            "Enable USB Debugging in Developer Options",
            "Connect to PC: adb reboot bootloader",
            "Unlock: fastboot flashing unlock  (older: fastboot oem unlock)",
            "Confirm on device screen — wipe happens immediately",
            "Device reboots to stock setup wizard",
        ],
        "notes": "Wipes everything. Samsung Knox trips permanently on unlock — no way back.",
    }

def _g_twrp(cn):
    return {
        "guide_type": "install-recovery",
        "title":      "Install TWRP Recovery",
        "source":     "Universal",
        "codename":   cn,
        "steps": [
            "Download TWRP .img for your exact device variant from twrp.me",
            "Boot to fastboot: adb reboot bootloader",
            "Flash: fastboot flash recovery twrp.img",
            "Boot into recovery immediately: fastboot boot twrp.img",
            "In TWRP swipe to allow modifications",
        ],
        "notes": "Use the exact TWRP build for your device model number. Wrong builds can brick.",
    }

def _g_orangefox(cn):
    return {
        "guide_type": "install-recovery",
        "title":      "Install OrangeFox Recovery",
        "source":     "Universal",
        "codename":   cn,
        "steps": [
            "Download OrangeFox .img for your device from orangefox.tech",
            "Boot to fastboot: adb reboot bootloader",
            "Flash: fastboot flash recovery orangefox.img",
            "Boot into recovery: fastboot boot orangefox.img",
        ],
        "notes": "OrangeFox is only available for select devices.",
    }

def _g_flash_rom(cn):
    return {
        "guide_type": "install-rom",
        "title":      "Flash Custom ROM",
        "source":     "Universal",
        "codename":   cn,
        "steps": [
            "Unlock bootloader and install custom recovery first",
            "Download ROM zip and GApps zip (if needed) to your device",
            "Boot into recovery (TWRP or OrangeFox)",
            "Wipe: Factory Reset → Data, Cache, Dalvik/ART cache",
            "Flash ROM zip: Install → select zip → Swipe to Flash",
            "Flash GApps zip in the same session before rebooting",
            "Reboot System — first boot takes 3-10 minutes",
        ],
        "notes": "Never mix incompatible GApps versions. Read the ROM thread for device-specific notes.",
    }

def _g_magisk(cn):
    return {
        "guide_type": "root",
        "title":      "Root with Magisk",
        "source":     "Universal",
        "codename":   cn,
        "steps": [
            "Unlock bootloader first",
            "Download stock boot.img for your exact firmware build",
            "Install Magisk app on device",
            "In Magisk: Install → Select and Patch a File → pick boot.img",
            "Copy patched_boot.img to PC",
            "Flash: fastboot flash boot patched_boot.img",
            "Reboot and open Magisk to verify root",
        ],
        "notes": "Keep a backup of the original boot.img. Magisk is systemless — safer for updates.",
    }

def _g_kernelsu(cn):
    return {
        "guide_type": "root",
        "title":      "Root with KernelSU",
        "source":     "Universal",
        "codename":   cn,
        "steps": [
            "Check kernelsu.org for a supported kernel for your device",
            "Download the KernelSU kernel .img",
            "Flash: fastboot flash boot kernelsu_boot.img",
            "Install KernelSU Manager from GitHub releases",
            "Grant root from the Manager",
        ],
        "notes": "Requires kernel-level support. Not all devices are supported.",
    }

def _g_apatch(cn):
    return {
        "guide_type": "root",
        "title":      "Root with APatch",
        "source":     "Universal",
        "codename":   cn,
        "steps": [
            "Download APatch from github.com/bmax121/APatch",
            "Extract boot.img from your stock firmware",
            "In APatch app: patch boot.img",
            "Flash patched boot: fastboot flash boot patched_boot.img",
            "Reboot and verify in APatch Manager",
        ],
        "notes": "Alternative to Magisk with kernel patch support.",
    }

def _g_restore(cn):
    return {
        "guide_type": "restore",
        "title":      "Restore Stock / Unbrick",
        "source":     "Universal",
        "codename":   cn,
        "steps": [
            "Download official stock firmware for your exact model and region",
            "Samsung: use Odin — flash AP/BL/CP/CSC files",
            "Xiaomi/Poco: use MiFlash in EDL/fastboot mode",
            "Google Pixel: use Android Flash Tool at flash.android.com",
            "OnePlus: use MSM Download Tool for hard bricks",
            "Other devices: check XDA for your specific model",
            "After flash: device reboots to stock",
        ],
        "notes": "Always use firmware matching your exact region and model number.",
    }

def _g_sellbuy(cn):
    return {
        "guide_type": "sell-buy",
        "title":      "Buying & Selling Modified Devices",
        "source":     "Universal",
        "codename":   cn,
        "steps": [
            "BEFORE SELLING: Factory reset and remove Google account (FRP)",
            "BEFORE SELLING: Restore stock ROM and re-lock bootloader if possible",
            "BEFORE SELLING: Disclose Knox trip status to Samsung buyers — it shows in settings",
            "BEFORE BUYING: Ask if bootloader is unlocked",
            "BEFORE BUYING: Check IMEI on imei.info — confirm not blacklisted",
            "BEFORE BUYING: Test camera, speakers, fingerprint, charging",
            "BEFORE BUYING: Verify model number matches your region",
        ],
        "notes": "Unlocked bootloader = lower resale value. FRP locks are illegal to bypass on a device you don't own.",
    }


async def get_guides_for_device(codename: str, manufacturer: str = "", guide_type: str | None = None) -> list[dict]:
    ck = f"guides_v3:{codename}"
    if c := await cache_get(ck): return c

    cn = codename.lower()
    guides = []

    # 1. Bootloader
    guides.append(_g_bootloader(cn))
    # 2. Recovery
    guides.append(_g_twrp(cn))
    guides.append(_g_orangefox(cn))
    # 3. ROM — try LineageOS wiki first
    async with get_client() as client:
        los = await _fetch_los(client, cn, "install-rom")
    if los:
        guides.append(los)
    else:
        guides.append(_g_flash_rom(cn))
    # GrapheneOS for supported Pixels
    if cn in _GOS_DEVICES:
        guides.append({
            "guide_type": "install-rom",
            "title":      "Install GrapheneOS",
            "source":     "GrapheneOS",
            "codename":   cn,
            "steps": [
                "Open grapheneos.org/install/web in Chrome or Edge",
                "Connect device in fastboot mode",
                "Follow the web installer — fully automated",
                "Reboot and complete setup",
            ],
            "notes": "WebUSB required. Chrome or Edge only.",
        })
    # 4. Root
    guides.extend([_g_magisk(cn), _g_kernelsu(cn), _g_apatch(cn)])
    # 5. Restore
    guides.append(_g_restore(cn))
    # 6. Sell/Buy
    guides.append(_g_sellbuy(cn))

    guides = _sort(guides)
    if guide_type:
        guides = [g for g in guides if g.get("guide_type") == guide_type]

    await cache_set(ck, guides, ttl=3600)
    return guides


async def get_all_guides(limit: int = 50, offset: int = 0) -> dict:
    guides = _sort([
        _g_bootloader("universal"),
        _g_twrp("universal"),
        _g_orangefox("universal"),
        _g_flash_rom("universal"),
        _g_magisk("universal"),
        _g_kernelsu("universal"),
        _g_apatch("universal"),
        _g_restore("universal"),
        _g_sellbuy("universal"),
    ])
    return {"total": len(guides), "offset": offset, "limit": limit, "guides": guides[offset:offset+limit]}
