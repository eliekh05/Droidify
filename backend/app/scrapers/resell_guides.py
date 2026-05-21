"""
Resell / trade-in preparation guides
Covers: factory reset, account removal, data wipe verification,
        IMEI check, bootloader relock, stock ROM restore.
"""

RESELL_GUIDES = [
    {
        "type":       "resell",
        "title":      "Prepare Your Phone for Resale or Trade-In",
        "source":     "Google Android Help",
        "source_url": "https://support.google.com/android/answer/6088915",
        "sections": [
            {
                "title": "Before you wipe — back up everything",
                "steps": [
                    "Back up photos and videos to Google Photos or copy to your computer",
                    "Export contacts: Settings → Google → Backup → Back up now",
                    "Note down your app list — Google Play shows your purchase history",
                    "Save any 2FA backup codes stored on the device",
                    "Remove your SIM card and any SD card",
                ],
            },
            {
                "title": "Remove accounts",
                "steps": [
                    "Go to Settings → Accounts → Google → Remove account",
                    "Remove all other accounts (Samsung, Microsoft, etc.)",
                    "On Samsung: Settings → Accounts and backup → Manage accounts",
                    "Disabling Find My Device / Samsung Find My Mobile before wiping avoids activation lock",
                ],
            },
            {
                "title": "Factory reset",
                "steps": [
                    "Settings → General Management → Reset → Factory data reset",
                    "On Pixel: Settings → System → Reset options → Erase all data",
                    "Confirm and enter your PIN when prompted",
                    "Do not restore during setup — let it complete to the welcome screen",
                    "This wipes all data, apps, accounts, and settings",
                ],
            },
            {
                "title": "Verify the wipe",
                "steps": [
                    "Go through the setup wizard — you should see a fresh 'Welcome' screen",
                    "Check Settings → About Phone — it should not show your name/account",
                    "Verify Find My Device is off: accounts.google.com/find-my-device",
                    "Check no accounts remain: Settings → Accounts should be empty",
                ],
            },
        ],
        "data_source": "google_support",
    },
    {
        "type":       "resell",
        "title":      "Relock Bootloader Before Resale",
        "source":     "Android Open Source Project",
        "source_url": "https://source.android.com/docs/core/architecture/bootloader/locking",
        "sections": [
            {
                "title": "Why relock",
                "steps": [
                    "An unlocked bootloader shows a warning on every boot — buyers may reject it",
                    "Relocking restores the stock security posture",
                    "Required for some trade-in programs (Samsung, Google)",
                    "Note: relocking on a modified device may cause a bootloop — restore stock ROM first",
                ],
            },
            {
                "title": "Steps (Fastboot devices)",
                "steps": [
                    "Flash stock firmware completely (see Unbrick guide)",
                    "Boot into fastboot: adb reboot bootloader",
                    "Relock: fastboot flashing lock",
                    "Confirm on device screen",
                    "Device will factory reset again — this is normal",
                ],
            },
            {
                "title": "Samsung (Odin/Knox)",
                "steps": [
                    "Samsung Knox counter cannot be reset — it permanently records unlocks",
                    "You can still factory reset and remove your account",
                    "Disclose the Knox trip status (Knox Warranty Void: 0x1) to buyers",
                ],
            },
        ],
        "data_source": "aosp_docs",
    },
    {
        "type":       "resell",
        "title":      "Check IMEI and Carrier Lock Before Selling",
        "source":     "Android Community",
        "source_url": "https://www.imei.info",
        "sections": [
            {
                "title": "Find your IMEI",
                "steps": [
                    "Dial *#06# — IMEI appears on screen immediately",
                    "Or: Settings → About Phone → IMEI",
                    "Dual-SIM phones have two IMEIs — check both",
                    "Note the IMEI — buyers will want it for blacklist checks",
                ],
            },
            {
                "title": "Check blacklist status",
                "steps": [
                    "Visit imei.info or swappa.com/check to verify the device is clean",
                    "A blacklisted IMEI means the device was reported stolen — you cannot sell it",
                    "Contact your carrier if the device was incorrectly blacklisted",
                ],
            },
            {
                "title": "Check carrier lock",
                "steps": [
                    "Insert a SIM from a different carrier — if it fails, the phone is locked",
                    "Request an unlock from your carrier (usually free after contract period)",
                    "Or use Settings → Connections → More connection settings → Network unlock (Samsung)",
                    "Unlocked phones sell for significantly more than locked ones",
                ],
            },
        ],
        "data_source": "community",
    },
]


async def get_resell_guides() -> list[dict]:
    """Return resell/trade-in preparation guides."""
    return RESELL_GUIDES
