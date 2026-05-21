"""
GSI (Generic System Image) ROM scraper.
GSI ROMs run on ANY Android 8.0+ device with Project Treble support.
This covers virtually all devices released since 2018.

Sources:
- phh-treble GSI (most popular independent GSI)
- Google AOSP GSI
- Known major GSI-compatible ROM projects
"""
from ..services.cache import get as cache_get, set as cache_set

# Major GSI ROM projects with verified download links
GSI_ROMS = [
    {
        "name":         "phh AOSP GSI",
        "codename":     "gsi_arm64",
        "manufacturer": None,
        "android_base": "15",
        "rom_type":     "gsi",
        "status":       "active",
        "official":     True,
        "maintainer":   "phhusson",
        "source_url":   "https://github.com/phhusson/treble_experimentations/releases",
        "download_url": "https://github.com/phhusson/treble_experimentations/releases/latest",
        "data_source":  "gsi",
        "rom_name":     "phh AOSP GSI",
        "description":  "Works on any Treble-compatible device (Android 8+)",
        "gsi_arch":     ["arm64", "arm"],
    },
    {
        "name":         "Google AOSP GSI",
        "codename":     "gsi_arm64",
        "manufacturer": "Google",
        "android_base": "15",
        "rom_type":     "gsi",
        "status":       "active",
        "official":     True,
        "maintainer":   "Google",
        "source_url":   "https://developer.android.com/topic/generic-system-image",
        "download_url": "https://developer.android.com/topic/generic-system-image/releases",
        "data_source":  "gsi",
        "rom_name":     "AOSP GSI",
        "description":  "Official Google AOSP Generic System Image for Treble-compatible devices",
    },
    {
        "name":         "LineageOS GSI",
        "codename":     "gsi_arm64",
        "manufacturer": None,
        "android_base": "15",
        "rom_type":     "gsi",
        "status":       "active",
        "official":     True,
        "maintainer":   "AndyYan",
        "source_url":   "https://github.com/AndyCGYan/lineage_build_unified",
        "download_url": "https://sourceforge.net/projects/andyyan-gsi/files/",
        "data_source":  "gsi",
        "rom_name":     "LineageOS GSI",
        "description":  "LineageOS as a GSI — runs on any Treble device",
    },
    {
        "name":         "Pixel Experience GSI",
        "codename":     "gsi_arm64",
        "manufacturer": None,
        "android_base": "14",
        "rom_type":     "gsi",
        "status":       "active",
        "official":     False,
        "maintainer":   "Community",
        "source_url":   "https://github.com/ponces/treble_build_pe",
        "download_url": "https://github.com/ponces/treble_build_pe/releases",
        "data_source":  "gsi",
        "rom_name":     "Pixel Experience GSI",
        "description":  "Pixel Experience as a GSI for Treble-compatible devices",
    },
    {
        "name":         "crDroid GSI",
        "codename":     "gsi_arm64",
        "manufacturer": None,
        "android_base": "14",
        "rom_type":     "gsi",
        "status":       "active",
        "official":     False,
        "maintainer":   "Community",
        "source_url":   "https://github.com/ponces/treble_build_crdroid",
        "download_url": "https://github.com/ponces/treble_build_crdroid/releases",
        "data_source":  "gsi",
        "rom_name":     "crDroid GSI",
        "description":  "crDroid as a GSI for Treble-compatible devices",
    },
    {
        "name":         "CalyxOS GSI",
        "codename":     "gsi_arm64",
        "manufacturer": None,
        "android_base": "14",
        "rom_type":     "gsi",
        "status":       "active",
        "official":     False,
        "maintainer":   "Community",
        "source_url":   "https://github.com/ponces/treble_build_calyx",
        "download_url": "https://github.com/ponces/treble_build_calyx/releases",
        "data_source":  "gsi",
        "rom_name":     "CalyxOS GSI",
        "description":  "CalyxOS as a GSI for Treble-compatible devices",
    },
]


async def get_gsi_roms() -> list[dict]:
    ck = "roms:gsi"
    if c := await cache_get(ck): return c
    await cache_set(ck, GSI_ROMS, ttl=86400)
    return GSI_ROMS
