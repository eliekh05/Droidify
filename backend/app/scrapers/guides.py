"""Guides scraper — fetches flashing, rooting, recovery, backup and unbrick
guides from free public sources.

Sources (all free, no auth):
  LineageOS Wiki      → install / upgrade / build guides per device (structured HTML)
  Magisk Docs         → root guide (topjohnwu.github.io/Magisk/install.html)
  KernelSU Docs       → root guide (kernelsu.org/guide/installation.html)
  APatch Docs         → root guide (GitHub wiki)
  GrapheneOS          → install guide per Pixel device
  Android Docs        → ADB/Fastboot reference (developer.android.com/tools/adb)

Guide types returned:
  install             → how to flash a custom ROM
  upgrade             → how to update LineageOS OTA
  root                → Magisk / KernelSU / APatch rooting
  backup              → TWRP backup / ADB backup steps
  bootloader-unlock   → OEM unlock / fastboot unlock steps
  unbrick             → EDL / Odin / SP Flash recovery steps
  recovery            → how to install TWRP / OrangeFox

Each guide has:
  type        string
  title       string
  source      string  (who wrote it)
  source_url  string  (link to full guide)
  steps       list[str]  (extracted steps — best effort, may be empty)
  notes       string  (warnings, prerequisites)
"""
import asyncio
import re

from bs4 import BeautifulSoup

from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

# ── URL patterns ──────────────────────────────────────────────────────────────
LOS_INSTALL_URL  = "https://wiki.lineageos.org/devices/{codename}/install/"
LOS_UPGRADE_URL  = "https://wiki.lineageos.org/devices/{codename}/upgrade/"
GOS_INSTALL_URL  = "https://grapheneos.org/install/cli"
MAGISK_GUIDE_URL = "https://topjohnwu.github.io/Magisk/install.html"
KSU_GUIDE_URL    = "https://kernelsu.org/guide/installation.html"
ADB_GUIDE_URL    = "https://developer.android.com/tools/adb"

# GrapheneOS supported Pixels
_GOS_PIXELS = {
    "tokay","caiman","komodo","comet","shiba","husky",
    "felix","tangorpro","lynx","cheetah","panther",
    "bluejay","oriole","raven",
}


def _clean(text: str) -> str:
    return re.sub(r"\s{2,}", " ", text).strip()


def _parse_los_guide(html: str, guide_type: str, codename: str) -> dict | None:
    """Parse a LineageOS wiki guide page into structured steps."""
    soup = BeautifulSoup(html, "lxml")

    # Check we got a real guide page not a redirect to wiki home
    h1 = soup.find("h1")
    if not h1 or codename.lower() not in html.lower():
        return None

    sections: list[dict] = []
    current_section: dict | None = None

    for tag in soup.find_all(["h2", "h3", "li", "p"]):
        if tag.name in ["h2", "h3"]:
            title = _clean(tag.get_text())
            if title and "What next" not in title and "Get assistance" not in title:
                current_section = {"title": title, "steps": []}
                sections.append(current_section)
        elif tag.name == "li" and current_section:
            text = _clean(tag.get_text())
            if text and len(text) > 5:
                # Remove navigation noise
                if not any(kw in text for kw in ["lineageos.org", "Contribute", "Glossary"]):
                    current_section["steps"].append(text[:250])
        elif tag.name == "p" and current_section:
            text = _clean(tag.get_text())
            if text and len(text) > 30:
                if "warning" in tag.get("class", []) or "note" in " ".join(tag.get("class", [])):
                    current_section["steps"].append(f"⚠ {text[:200]}")

    if not sections:
        return None

    # Flatten steps for summary
    all_steps = []
    for s in sections:
        if s["steps"]:
            all_steps.append(f"── {s['title']} ──")
            all_steps.extend(s["steps"][:6])

    type_titles = {
        "install": f"How to install LineageOS on {codename}",
        "upgrade": f"How to upgrade LineageOS on {codename}",
        "build":   f"How to build LineageOS for {codename}",
    }

    return {
        "type":       guide_type,
        "title":      type_titles.get(guide_type, f"LineageOS {guide_type} guide — {codename}"),
        "source":     "LineageOS Wiki",
        "source_url": LOS_INSTALL_URL.format(codename=codename)
                      if guide_type == "install"
                      else LOS_UPGRADE_URL.format(codename=codename),
        "sections":   sections[:10],
        "steps":      all_steps[:30],
        "notes":      (
            "⚠ Unlocking the bootloader WILL erase all data on your device. "
            "Back up everything first. Read through the full guide before starting."
        ),
        "data_source": "lineageos_wiki",
    }


async def _los_guide(client, codename: str, guide_type: str) -> dict | None:
    """Fetch and parse a LineageOS wiki guide."""
    url = (LOS_INSTALL_URL if guide_type == "install" else LOS_UPGRADE_URL).format(
        codename=codename
    )
    resp = await fetch(client, url)
    if not resp or resp.status_code != 200:
        return None
    return _parse_los_guide(resp.text, guide_type, codename)


async def _magisk_guide(client) -> dict:
    """Fetch and parse the Magisk root guide."""
    ck = "guide:magisk"
    cached = await cache_get(ck)
    if cached:
        return cached

    resp = await fetch(client, MAGISK_GUIDE_URL)
    steps: list[str] = []
    if resp and resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "lxml")
        for li in soup.find_all("li"):
            text = _clean(li.get_text())
            if text and len(text) > 15:
                steps.append(text[:200])

    result = {
        "type":       "root",
        "title":      "Root with Magisk",
        "source":     "Magisk Documentation",
        "source_url": MAGISK_GUIDE_URL,
        "sections": [
            {
                "title": "Requirements",
                "steps": [
                    "Unlocked bootloader",
                    "Latest Magisk APK downloaded from GitHub",
                    "ADB and Fastboot installed on your PC",
                    "A copy of your device's stock boot.img (from firmware zip)",
                ]
            },
            {
                "title": "Steps",
                "steps": [
                    "Install the Magisk app on your device",
                    "Copy your stock boot.img to your device storage",
                    "Open Magisk → Install → Select and Patch a File → choose boot.img",
                    "Wait for patching to complete",
                    "Copy the patched image back: adb pull /sdcard/Download/magisk_patched*.img",
                    "Boot into fastboot: adb reboot bootloader",
                    "Flash patched image: fastboot flash boot magisk_patched*.img",
                    "Reboot: fastboot reboot",
                    "Open Magisk app to confirm root is active",
                ]
            },
        ],
        "steps": steps[:25] or [
            "Download Magisk APK from github.com/topjohnwu/Magisk/releases",
            "Install Magisk app on device",
            "Extract boot.img from your stock firmware",
            "Copy boot.img to device storage",
            "Magisk app → Install → Select and Patch a File → boot.img",
            "ADB pull the patched image from /sdcard/Download/",
            "Boot into fastboot mode",
            "fastboot flash boot magisk_patched_*.img",
            "fastboot reboot",
            "Open Magisk app to verify root",
        ],
        "notes": (
            "⚠ Never flash a patched boot.img shared by someone else. "
            "Always patch your own copy from official firmware. "
            "Requires unlocked bootloader."
        ),
        "data_source": "magisk_docs",
    }
    await cache_set(ck, result, ttl=3600)
    return result


async def _kernelsu_guide(client) -> dict:
    """KernelSU root guide."""
    ck = "guide:kernelsu"
    cached = await cache_get(ck)
    if cached:
        return cached

    result = {
        "type":       "root",
        "title":      "Root with KernelSU",
        "source":     "KernelSU Documentation",
        "source_url": "https://kernelsu.org/guide/installation.html",
        "sections": [
            {
                "title": "Requirements",
                "steps": [
                    "GKI (Generic Kernel Image) kernel — Android 12+ on most Snapdragon/MediaTek devices",
                    "Unlocked bootloader",
                    "ADB and Fastboot installed",
                ]
            },
            {
                "title": "Steps",
                "steps": [
                    "Download KernelSU Manager APK from github.com/tiann/KernelSU/releases",
                    "Install KernelSU Manager app on device",
                    "Check your device's GKI version in the Manager app",
                    "Download the matching KernelSU kernel image",
                    "Boot into fastboot mode: adb reboot bootloader",
                    "Flash kernel: fastboot flash boot kernelsu_*.img",
                    "Reboot: fastboot reboot",
                    "Open KernelSU Manager to confirm",
                ]
            },
        ],
        "steps": [
            "Download KernelSU Manager APK from github.com/tiann/KernelSU/releases",
            "Install KernelSU Manager on device",
            "Check GKI version compatibility in Manager app",
            "Download matching boot image from KernelSU releases",
            "adb reboot bootloader",
            "fastboot flash boot kernelsu_boot.img",
            "fastboot reboot",
            "Open KernelSU Manager to verify",
        ],
        "notes": (
            "KernelSU requires a GKI kernel. Not compatible with all devices. "
            "Check kernelsu.org for device compatibility before proceeding."
        ),
        "data_source": "kernelsu_docs",
    }
    await cache_set(ck, result, ttl=3600)
    return result


def _bootloader_unlock_guide(codename: str, manufacturer: str) -> dict:
    """
    Generate bootloader unlock steps based on manufacturer.
    Different OEMs have very different unlock procedures:
      Google Pixel   → fastboot flashing unlock (simplest)
      Xiaomi/POCO    → Mi Unlock Tool required (1-7 day wait)
      OnePlus        → fastboot oem unlock or Settings toggle
      Samsung        → OEM Unlock toggle only (no fastboot BL unlock on most models)
      Motorola       → fastboot oem unlock
      Sony           → Sony unlock server (newflasher)
      Fairphone      → fastboot flashing unlock
    """
    mfr = (manufacturer or "").lower()

    if "google" in mfr or codename in {
        "tokay","caiman","komodo","comet","shiba","husky",
        "felix","tangorpro","lynx","cheetah","panther",
        "bluejay","oriole","raven","bonito","crosshatch",
        "taimen","walleye","marlin","sailfish","angler","bullhead",
    }:
        steps = [
            "Enable Developer Options: Settings → About Phone → tap Build Number 7 times",
            "Enable OEM Unlocking: Settings → Developer Options → OEM Unlocking",
            "Connect device to PC via USB",
            "Boot into fastboot: adb reboot bootloader",
            "Unlock bootloader: fastboot flashing unlock",
            "Confirm on device screen using volume keys + power",
            "Device will factory reset and reboot",
            "Re-enable Developer Options and OEM Unlocking after reboot",
        ]
        notes = "⚠ Will factory reset your device. Back up all data first."
        tool = "fastboot"

    elif "xiaomi" in mfr or "poco" in mfr or "redmi" in mfr:
        steps = [
            "Create a Xiaomi account and log in on your device",
            "Enable Developer Options: Settings → About Phone → MIUI Version (tap 7 times)",
            "Enable OEM Unlocking and Mi Unlock Status",
            "Apply for unlock at account.xiaomi.com/pass/v3/unlock (may require waiting 1-7 days)",
            "Download Mi Unlock Tool from miui.com/unlock",
            "Boot into fastboot: adb reboot bootloader",
            "Open Mi Unlock Tool on PC → sign in → click Unlock",
            "Device will factory reset and unlock",
        ]
        notes = (
            "⚠ Xiaomi requires account binding and a mandatory waiting period (1–7 days) "
            "before unlock is approved. Will factory reset your device."
        )
        tool = "mi_unlock_tool"

    elif "samsung" in mfr:
        steps = [
            "Enable Developer Options: Settings → About Phone → Software Information → Build Number (tap 7 times)",
            "Enable OEM Unlocking: Settings → Developer Options → OEM Unlocking",
            "Note: Most Samsung devices do NOT support fastboot bootloader unlock",
            "Samsung uses Download Mode (Odin/Heimdall) for firmware flashing instead",
            "To flash custom recovery: boot into Download Mode (Vol Down + Home + Power)",
            "Use Odin (Windows) or Heimdall (Linux/macOS) to flash recovery image",
            "Then boot into recovery and flash custom ROM via ADB sideload",
        ]
        notes = (
            "⚠ Samsung devices generally cannot unlock the bootloader via fastboot. "
            "OEM Unlock toggle enables flashing via Download Mode only. "
            "Some carrier-locked Samsung devices cannot be unlocked at all."
        )
        tool = "odin_heimdall"

    elif "oneplus" in mfr:
        steps = [
            "Enable Developer Options: Settings → About Phone → Build Number (tap 7 times)",
            "Enable OEM Unlocking: Settings → Developer Options → OEM Unlocking",
            "Connect device to PC via USB",
            "Boot into fastboot: adb reboot bootloader",
            "Unlock: fastboot oem unlock  (older models) OR fastboot flashing unlock (newer)",
            "Confirm on device screen",
            "Device will factory reset and reboot",
        ]
        notes = "⚠ Will factory reset your device. OnePlus 6 and older use 'fastboot oem unlock'."
        tool = "fastboot"

    elif "motorola" in mfr or "moto" in mfr:
        steps = [
            "Visit motorola.com/unlockbootloader to request unlock key",
            "Enable Developer Options: Settings → About Phone → Build Number (tap 7 times)",
            "Enable OEM Unlocking in Developer Options",
            "Connect device to PC via USB",
            "Boot into fastboot: adb reboot bootloader",
            "Run: fastboot oem get_unlock_data",
            "Copy the unlock data to the Motorola website form to get your unlock key",
            "Run: fastboot oem unlock YOUR_UNLOCK_KEY",
            "Device will factory reset",
        ]
        notes = "⚠ Requires a device-specific unlock key from Motorola's website. Will factory reset."
        tool = "fastboot"

    elif "sony" in mfr:
        steps = [
            "Check if your device is eligible at developer.sony.com/develop/open-devices/get-started/unlock-bootloader",
            "Get your unlock key from Sony's website using your device's IMEI",
            "Enable Developer Options and OEM Unlocking",
            "Boot into fastboot: adb reboot bootloader",
            "Run: fastboot oem unlock 0x<YOUR_KEY>",
            "Device will factory reset",
        ]
        notes = "⚠ Sony devices require an OEM-specific unlock code. Some models are not unlockable."
        tool = "fastboot"

    elif "fairphone" in mfr:
        steps = [
            "Enable Developer Options: Settings → About Phone → Build Number (tap 7 times)",
            "Enable OEM Unlocking: Settings → Developer Options → OEM Unlocking",
            "Boot into fastboot: adb reboot bootloader",
            "Unlock: fastboot flashing unlock",
            "Confirm on device",
            "Device factory resets and reboots",
        ]
        notes = "⚠ Fairphone supports bootloader unlocking officially. Will factory reset."
        tool = "fastboot"

    else:
        # Generic Qualcomm/fastboot guide
        steps = [
            "Enable Developer Options: Settings → About Phone → Build Number (tap 7 times)",
            "Enable OEM Unlocking: Settings → Developer Options → OEM Unlocking (if present)",
            "Connect device to PC via USB",
            "Boot into fastboot: adb reboot bootloader",
            "Try: fastboot flashing unlock  (Android 8+)",
            "Or try: fastboot oem unlock  (older devices)",
            "Confirm on device screen if prompted",
            "Device will factory reset",
        ]
        notes = (
            "⚠ Unlock method varies by manufacturer. "
            "Search XDA forums for your specific device for confirmed steps. "
            "Will factory reset your device."
        )
        tool = "fastboot"

    return {
        "type":       "bootloader-unlock",
        "title":      f"Bootloader Unlock — {manufacturer or codename}",
        "source":     "Droidify (compiled from OEM documentation)",
        "source_url": "https://source.android.com/docs/core/architecture/bootloader/locking",
        "sections":   [{"title": "Steps", "steps": steps}],
        "steps":      steps,
        "tool":       tool,
        "notes":      notes,
        "data_source": "compiled_oem_docs",
    }


def _backup_guide() -> dict:
    """Universal TWRP + ADB backup guide."""
    return {
        "type":       "backup",
        "title":      "How to Back Up Your Android Device",
        "source":     "TWRP + Android ADB documentation",
        "source_url": "https://twrp.me/",
        "sections": [
            {
                "title": "Method 1 — TWRP Full Backup (recommended, requires TWRP installed)",
                "steps": [
                    "Boot into TWRP recovery (Vol Up + Power, or adb reboot recovery)",
                    "Tap Backup",
                    "Select: Boot, System, Data (and Vendor if shown)",
                    "Swipe to back up",
                    "Wait for completion — backup saved to /sdcard/TWRP/BACKUPS/",
                    "Copy the backup folder to your PC: adb pull /sdcard/TWRP/BACKUPS/ ./",
                ]
            },
            {
                "title": "Method 2 — ADB Backup (no root needed, limited)",
                "steps": [
                    "Enable USB Debugging: Settings → Developer Options → USB Debugging",
                    "Connect device to PC via USB",
                    "Run: adb backup -apk -shared -all -f backup.ab",
                    "Unlock your phone and tap 'Back up my data'",
                    "Enter encryption password if desired",
                    "Wait for completion",
                    "Restore later with: adb restore backup.ab",
                ]
            },
            {
                "title": "Method 3 — Google Backup (before flashing)",
                "steps": [
                    "Settings → System → Backup → Back up now",
                    "Ensure Google Photos backup is complete for photos",
                    "Note your app list — some apps cannot be restored to custom ROMs",
                ]
            },
        ],
        "steps": [
            "Boot into TWRP recovery",
            "Tap Backup → select Boot, System, Data",
            "Swipe to back up",
            "Copy backup to PC: adb pull /sdcard/TWRP/BACKUPS/ ./",
        ],
        "notes": (
            "⚠ Always back up BEFORE flashing anything. "
            "TWRP backup is the most complete — backs up everything including app data. "
            "ADB backup does not include all app data and is not available on all devices."
        ),
        "data_source": "twrp_adb_docs",
    }


def _unbrick_guide(manufacturer: str, codename: str) -> dict:
    """Generate unbrick steps based on manufacturer/chipset family."""
    mfr = (manufacturer or "").lower()

    if "samsung" in mfr:
        steps = [
            "Download the stock firmware for your exact model from samfw.com or SamMobile",
            "Install Odin on Windows (or Heimdall on Linux/macOS)",
            "Boot device into Download Mode: hold Vol Down + Home + Power (or Vol Down + Bixby + Power)",
            "Connect device to PC via USB",
            "Open Odin → load AP/BL/CP/CSC files from the firmware zip",
            "Click Start in Odin",
            "Wait for PASS message — device will reboot",
            "If Download Mode is not accessible, try: hold Vol Down + Vol Up + Power (Emergency Download)",
        ]
        tool = "odin"
        dl_url = "https://odindownload.com/"

    elif any(x in mfr for x in ["xiaomi", "poco", "redmi"]) or codename in {
        "alioth","haydn","lmi","pipa","psyche","spes","marble",
    }:
        steps = [
            "Download MIUI fastboot ROM for your device from xiaomi.com/global/miui",
            "Install Mi Flash Tool (Windows only) from miui.com/unlock",
            "Boot device into EDL/9008 mode: hold Vol Down + Power, or use EDL cable",
            "Open Mi Flash Tool → select extracted ROM folder → Flash",
            "Alternative if EDL unavailable: boot into fastboot and use fastboot flash commands",
            "If using Mi Flash, select 'Flash All' to fully restore",
        ]
        tool = "mi_flash_tool"
        dl_url = "https://xdaforums.com/t/guide-miflash-tool-flash-miui-rom.3289528/"

    elif "qualcomm" in mfr or any(x in codename for x in ["sm8", "sm7", "sdm"]):
        steps = [
            "Download QFIL (Qualcomm Flash Image Loader)",
            "Get the stock firmware/firehose programmer for your device from XDA",
            "Boot device into EDL mode (9008): hold Vol Up + Vol Down + plug USB, or use test point",
            "Open QFIL → select Flat Build → load programmer (.mbn/.elf file)",
            "Load the rawprogram XML and patch XML files",
            "Click Download — wait for completion",
            "Device should reboot into stock firmware",
        ]
        tool = "qfil"
        dl_url = "https://qfiltool.com/"

    elif "mediatek" in mfr or "mtk" in mfr:
        steps = [
            "Download SP Flash Tool from spflashtools.com",
            "Get the stock scatter/firmware for your device from XDA or manufacturer",
            "Install MTK USB drivers on your PC",
            "Open SP Flash Tool → Load the scatter file from firmware folder",
            "Select Download Only (not Format All) to preserve data, or Format All to fully restore",
            "Power OFF device completely",
            "Click Download in SP Flash Tool → plug in USB cable",
            "Wait for progress bar to complete — green ring = success",
        ]
        tool = "sp_flash_tool"
        dl_url = "https://spflashtools.com/"

    elif "google" in mfr or codename in {
        "panther","bluejay","oriole","raven","cheetah","lynx",
        "felix","tangorpro","husky","shiba","tokay","caiman","komodo","comet",
    }:
        steps = [
            "Download the factory image for your device from developers.google.com/android/images",
            "Extract the factory image zip",
            "Boot into fastboot: adb reboot bootloader",
            "Run the flash-all script: ./flash-all.sh (macOS/Linux) or flash-all.bat (Windows)",
            "This restores the complete stock firmware including bootloader",
            "Device will reboot into stock Android",
        ]
        tool = "fastboot"
        dl_url = "https://developers.google.com/android/images"

    else:
        steps = [
            "Identify your device chipset (Qualcomm/MediaTek/Samsung/other)",
            "For Qualcomm: use QFIL with EDL mode (9008)",
            "For MediaTek: use SP Flash Tool with scatter file",
            "For Samsung: use Odin or Heimdall with stock firmware",
            "Search XDA forums for '[your device] unbrick guide' for device-specific steps",
            f"XDA search: xdaforums.com/search/?q={codename}+unbrick",
        ]
        tool = "varies"
        dl_url = f"https://xdaforums.com/search/?q={codename}+unbrick"

    return {
        "type":       "unbrick",
        "title":      f"Unbrick / Restore Stock — {manufacturer or codename}",
        "source":     "Compiled from manufacturer and XDA documentation",
        "source_url": dl_url,
        "sections":   [{"title": "Recovery Steps", "steps": steps}],
        "steps":      steps,
        "tool":       tool,
        "notes":      (
            "⚠ Unbricking usually requires a PC, a USB cable, and the correct stock firmware "
            "for your EXACT model number. Using the wrong firmware can make things worse. "
            "Always verify the firmware matches your model before flashing."
        ),
        "data_source": "compiled_xda_oem_docs",
    }


def _recovery_install_guide(codename: str, manufacturer: str) -> dict:
    """Guide for installing TWRP or OrangeFox custom recovery."""
    mfr = (manufacturer or "").lower()

    if "samsung" in mfr:
        steps = [
            "Download TWRP or OrangeFox .tar image for your device",
            "Enable OEM Unlock in Developer Options",
            "Boot into Download Mode: Vol Down + Home + Power",
            "Connect device to PC",
            "Open Odin (Windows) or Heimdall (Linux/macOS)",
            "In Odin: load .tar file into AP slot → click Start",
            "In Heimdall: heimdall flash --RECOVERY twrp.img",
            "Immediately boot into recovery: Vol Up + Home + Power",
            "Do NOT let device boot to system first (Samsung re-locks recovery)",
        ]
    else:
        steps = [
            "Download TWRP or OrangeFox .img file for your device",
            "Boot into fastboot mode: adb reboot bootloader",
            "Flash recovery: fastboot flash recovery twrp.img",
            "Some devices: fastboot boot twrp.img (temporary boot, then install from within TWRP)",
            "Reboot into recovery: fastboot reboot recovery",
            "In TWRP: swipe to allow modifications if prompted",
            "Flash any ROM or module via Install → ADB Sideload or select zip",
        ]

    return {
        "type":       "recovery",
        "title":      f"Install Custom Recovery — {manufacturer or codename}",
        "source":     "TWRP / OrangeFox documentation",
        "source_url": f"https://twrp.me/Devices/",
        "sections":   [{"title": "Steps", "steps": steps}],
        "steps":      steps,
        "notes":      (
            "⚠ Custom recovery replaces your stock recovery. "
            "Some devices re-flash stock recovery on every boot — "
            "disable this by flashing ROM immediately after flashing recovery."
        ),
        "data_source": "twrp_orangefox_docs",
    }


# ── Main public function ──────────────────────────────────────────────────────
async def get_guides_for_device(
    codename: str,
    manufacturer: str | None = None,
) -> list[dict]:
    """
    Return all available guides for a device.
    Fetches live guides from LineageOS Wiki + static structured guides
    compiled from manufacturer/XDA/tool documentation.
    """
    ck = f"guides:{codename}"
    cached = await cache_get(ck)
    if cached is not None:
        return cached

    guides: list[dict] = []
    mfr = manufacturer or ""

    async with get_client() as client:
        los_install, los_upgrade, magisk_guide, ksu_guide = await asyncio.gather(
            _los_guide(client, codename, "install"),
            _los_guide(client, codename, "upgrade"),
            _magisk_guide(client),
            _kernelsu_guide(client),
        )

    # LineageOS guides (live from wiki)
    if los_install:
        guides.append(los_install)
    if los_upgrade:
        guides.append(los_upgrade)

    # GrapheneOS install guide for supported Pixels
    if codename in _GOS_PIXELS:
        guides.append({
            "type":       "install",
            "title":      f"Install GrapheneOS on {codename}",
            "source":     "GrapheneOS Documentation",
            "source_url": GOS_INSTALL_URL,
            "sections":   [{
                "title": "Steps",
                "steps": [
                    "Use the official GrapheneOS web installer at grapheneos.org/install/web (Chrome/Edge required)",
                    "Or follow the CLI guide at grapheneos.org/install/cli",
                    "Unlock bootloader: fastboot flashing unlock",
                    "Flash GrapheneOS: use the web installer or fastboot commands from the CLI guide",
                    "Re-lock bootloader after install: fastboot flashing lock",
                    "Re-locking is strongly recommended for security",
                ]
            }],
            "steps": [
                "Visit grapheneos.org/install/web in Chrome or Edge",
                "Connect device and follow the web installer",
                "Or: download factory image and run fastboot commands from CLI guide",
                "Re-lock bootloader after installation",
            ],
            "notes": "GrapheneOS re-locking the bootloader after install is recommended and supported.",
            "data_source": "grapheneos_docs",
        })

    # Root guides
    guides.append(magisk_guide)
    guides.append(ksu_guide)

    # Bootloader unlock
    guides.append(_bootloader_unlock_guide(codename, mfr))

    # Custom recovery install
    guides.append(_recovery_install_guide(codename, mfr))

    # Backup guide (universal)
    guides.append(_backup_guide())

    # Unbrick guide
    guides.append(_unbrick_guide(mfr, codename))

    # Add resell/trade-in guides
    try:
        from app.scrapers.resell_guides import get_resell_guides
        resell = await get_resell_guides()
        guides.extend(resell)
    except Exception:
        pass

    await cache_set(ck, guides, ttl=3600)
    return guides


async def get_all_guides() -> list[dict]:
    """Return universal guides not tied to a specific device."""
    ck = "guides:universal"
    cached = await cache_get(ck)
    if cached:
        return cached

    async with get_client() as client:
        magisk_guide, ksu_guide = await asyncio.gather(
            _magisk_guide(client),
            _kernelsu_guide(client),
        )

    guides = [
        magisk_guide,
        ksu_guide,
        _backup_guide(),
        {
            "type":       "bootloader-unlock",
            "title":      "Bootloader Unlock — General Guide",
            "source":     "Android Open Source Project",
            "source_url": "https://source.android.com/docs/core/architecture/bootloader/locking",
            "sections": [
                {
                    "title": "Steps",
                    "steps": [
                        "Enable Developer Options: go to Settings → About Phone → tap Build Number 7 times",
                        "Enable OEM Unlocking in Settings → Developer Options",
                        "Boot into fastboot mode: adb reboot bootloader",
                        "Run: fastboot flashing unlock  (Android 8+) or fastboot oem unlock  (older devices)",
                        "Confirm the unlock on your device screen",
                        "Device will factory reset and reboot",
                    ],
                }
            ],
            "notes": "⚠ Steps vary by manufacturer. Search for your device codename above for exact instructions.",
            "data_source": "aosp_docs",
        },
        {
            "type":       "recovery",
            "title":      "Install Custom Recovery — General Guide",
            "source":     "TWRP Documentation",
            "source_url": "https://twrp.me/faq/howtoinstalltwrp.html",
            "sections": [
                {
                    "title": "Steps",
                    "steps": [
                        "Unlock bootloader first (see Bootloader Unlock guide)",
                        "Download TWRP or OrangeFox image for your device from the Recoveries page",
                        "Boot into fastboot mode: adb reboot bootloader",
                        "Flash the recovery: fastboot flash recovery recovery.img",
                        "Boot directly into recovery: fastboot boot recovery.img",
                        "Once in recovery, install the recovery permanently via the recovery UI",
                    ],
                }
            ],
            "notes": "⚠ Always verify the recovery image matches your exact device model and Android version.",
            "data_source": "twrp_docs",
        },
        {
            "type":       "unbrick",
            "title":      "Unbrick / Restore Stock — General Guide",
            "source":     "Android Community",
            "source_url": "https://source.android.com/docs/core/architecture/bootloader",
            "sections": [
                {
                    "title": "Soft Brick (boots to fastboot/recovery)",
                    "steps": [
                        "Boot into fastboot mode",
                        "Flash stock firmware using fastboot flash commands",
                        "Or restore via recovery: adb sideload stock_rom.zip",
                        "Reboot: fastboot reboot",
                    ],
                },
                {
                    "title": "Hard Brick (no signs of life)",
                    "steps": [
                        "Qualcomm devices: use QFIL / EDL mode (hold Vol Down + USB at boot)",
                        "MediaTek devices: use SP Flash Tool with scatter file",
                        "Samsung devices: use Odin with stock firmware (KDZ or TAR file)",
                        "Google Pixel: use Android Flash Tool at flash.android.com",
                    ],
                },
            ],
            "notes": "⚠ Use device-specific guides above for exact firmware files and steps.",
            "data_source": "community",
        },
        {
            "type":       "install",
            "title":      "Flash a Custom ROM — General Guide",
            "source":     "LineageOS Wiki",
            "source_url": "https://wiki.lineageos.org/faq",
            "sections": [
                {
                    "title": "Requirements",
                    "steps": [
                        "Unlocked bootloader",
                        "Custom recovery installed (TWRP or OrangeFox)",
                        "ADB and fastboot installed on your computer",
                        "ROM zip file downloaded and verified",
                    ],
                },
                {
                    "title": "Steps",
                    "steps": [
                        "Boot into recovery",
                        "Wipe: Factory Reset (or Dalvik/Cache/System/Data depending on ROM instructions)",
                        "Install the ROM zip via recovery",
                        "Optionally install GApps package if ROM does not include Google apps",
                        "Reboot system — first boot takes 3–10 minutes",
                    ],
                },
            ],
            "notes": "⚠ Always read the ROM-specific instructions. Steps vary between ROMs.",
            "data_source": "lineageos_wiki",
        },
    ]
    # Add resell/trade-in guides
    try:
        from app.scrapers.resell_guides import get_resell_guides
        resell = await get_resell_guides()
        guides.extend(resell)
    except Exception:
        pass

    await cache_set(ck, guides, ttl=3600)
    return guides
