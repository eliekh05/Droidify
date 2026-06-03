"""Buying and selling guides for used Android devices."""
_BUY_GENERAL = {
    "guide_type":  "buy",
    "title":       "What to check before buying a used device for custom ROMs",
    "source":      "Droidify",
    "source_url":  None,
    "codename":    "universal",
    "steps": [
        "Confirm the exact model number — not just the marketing name. "
        "Galaxy S8 has two variants: SM-G950F (Exynos, most markets) and "
        "SM-G950U (Snapdragon, US carriers). ROM support differs between them.",

        "Check if the bootloader is unlockable. Some carrier-locked US variants "
        "(Verizon, AT&T, Sprint) permanently disable OEM unlocking in software. "
        "Look up the exact SM-XXXXX model on XDA before buying.",

        "Ask if the bootloader has already been unlocked. An unlocked bootloader "
        "means someone has already flashed custom software — the device was wiped "
        "at least once. Not necessarily a problem, but worth knowing.",

        "Check the IMEI against a blacklist database (IMEI.info or Swappa) before "
        "paying. A blacklisted device cannot make calls on any carrier.",

        "Boot the device and check Settings → About Phone → Build Number. "
        "Verify the Android version matches what the seller claims.",

        "Test the basics: touchscreen, cameras, speakers, microphone, "
        "fingerprint sensor, charging, WiFi, Bluetooth, SIM slot. "
        "Custom ROM issues are much harder to diagnose if hardware is already broken.",

        "For Samsung devices: check Settings → About Phone → Software Information "
        "→ Knox Warranty Void. If it shows 0x1, the bootloader was unlocked at "
        "some point and Knox is permanently tripped. This affects Samsung Pay, "
        "Secure Folder, and some banking apps.",

        "Check battery health if possible. Older flagships with degraded batteries "
        "make poor custom ROM candidates — battery drain is worse after flashing.",
    ],
    "notes": (
        "The most important check is the exact model number. "
        "Marketing names are meaningless for ROM compatibility. "
        "Always look up the SM-XXXXX or equivalent model string."
    ),
}

_BUY_SAMSUNG = {
    "guide_type":  "buy",
    "title":       "Buying a used Samsung for custom ROMs — what to check",
    "source":      "Droidify",
    "source_url":  None,
    "codename":    "universal",
    "manufacturer": "Samsung",
    "steps": [
        "Find the exact model number in Settings → About Phone → Model Number. "
        "Not the marketing name — the SM-XXXXX string. "
        "For example: SM-G998B is Galaxy S21 Ultra Exynos (unlockable), "
        "SM-G998U is Galaxy S21 Ultra Snapdragon (often carrier-locked).",

        "Check Knox status: Settings → About Phone → Software Information → "
        "Knox Warranty Void. 0x0 means factory state. 0x1 means bootloader "
        "was unlocked at some point. Knox is one-way — once tripped, stays tripped.",

        "Verify OEM unlocking is available in Developer Options. On US carrier "
        "variants (Verizon in particular) this option is greyed out and cannot "
        "be enabled. There is no software workaround.",

        "Check for Samsung FRP (Factory Reset Protection) lock. Ask the seller "
        "to factory reset in front of you, or verify the previous Google account "
        "is removed before completing the purchase.",

        "Exynos vs Snapdragon matters for ROM support. Most global ROMs target "
        "Exynos variants. US Snapdragon variants have less community support "
        "and the bootloader situation is worse.",

        "Older Samsung (pre-2019) use Download Mode + Odin for flashing instead "
        "of standard fastboot. This requires a Windows PC with Odin installed. "
        "Newer Samsung (2019+) support standard fastboot.",
    ],
    "notes": (
        "Samsung Knox is the biggest gotcha. Once 0x1, banking apps, "
        "Samsung Pay, and Secure Folder stop working permanently — even if you "
        "flash back to stock. For custom ROM use this usually doesn't matter, "
        "but know what you're buying."
    ),
}

_BUY_XIAOMI = {
    "guide_type":  "buy",
    "title":       "Buying a used Xiaomi/Redmi/POCO for custom ROMs — what to check",
    "source":      "Droidify",
    "source_url":  None,
    "codename":    "universal",
    "manufacturer": "Xiaomi",
    "steps": [
        "Find the codename in Settings → About Phone → All Specs. "
        "The codename (e.g. 'beryllium', 'mido') determines ROM compatibility, "
        "not the marketing name.",

        "Check MIUI version. Xiaomi changed bootloader unlock policy in 2022 — "
        "newer MIUI/HyperOS requires a waiting period (168 hours minimum) "
        "after linking a Xiaomi account before unlock is permitted.",

        "Ask if the 168-hour wait has already been completed and if the bootloader "
        "is unlocked. This saves you a week if it's already done.",

        "Check if it's a China ROM variant. China MIUI has Google services issues. "
        "Global variant is better for custom ROM use, but both can be flashed.",

        "Verify the device has a proper fastboot mode — power + volume down. "
        "Xiaomi uses standard fastboot which makes flashing straightforward "
        "compared to Samsung's Odin-based flow.",

        "For POCO devices: confirm it's not a locked variant sold by a carrier. "
        "POCO phones are generally more unlock-friendly than Redmi budget devices.",
    ],
    "notes": (
        "Xiaomi's unlock waiting period is the main friction point. "
        "If you're buying used and the seller already completed the wait and "
        "unlocked the bootloader, that's a meaningful time saver."
    ),
}

_BUY_GOOGLE = {
    "guide_type":  "buy",
    "title":       "Buying a used Google Pixel for custom ROMs — what to check",
    "source":      "Droidify",
    "source_url":  None,
    "codename":    "universal",
    "manufacturer": "Google",
    "steps": [
        "Google Pixels are the easiest Android devices to unlock and flash. "
        "No OEM-specific restrictions, standard fastboot, and excellent ROM support.",

        "Check the codename in Settings → About Phone → Model. "
        "Pixel 9 = tokay, Pixel 9 Pro = caiman, Pixel 8 = shiba, etc. "
        "This confirms GrapheneOS and other ROM compatibility.",

        "Verify no carrier lock. Unlocked Pixel = full bootloader control. "
        "Carrier-locked Pixels can still be unlocked but may need to be "
        "used on that carrier first before the device is eligible.",

        "Check if the device is listed on grapheneos.org/install if you intend "
        "to run GrapheneOS — only specific Pixel models are supported.",

        "Pixel phones older than 5 years are past Google's security update window. "
        "They work fine with GrapheneOS or LineageOS but you lose upstream security patches "
        "from Google. Factor this into your decision.",

        "Android version: check Settings → About Phone. Pixels receive fast updates "
        "and can usually be flashed to the latest stock Android before you flash a custom ROM.",
    ],
    "notes": (
        "Pixels are the best choice for custom ROM use. "
        "Unlocking is two commands, flashing is clean, "
        "and the community support is excellent."
    ),
}

_SELL_GENERAL = {
    "guide_type":  "sell",
    "title":       "What to do before selling a device with a custom ROM",
    "source":      "Droidify",
    "source_url":  None,
    "codename":    "universal",
    "steps": [
        "Remove your Google account first — Settings → Accounts → Google → Remove. "
        "Failing to do this before factory reset triggers FRP (Factory Reset Protection). "
        "The buyer will be locked out until your credentials are entered.",

        "Remove all other accounts: email, Microsoft, Samsung, Xiaomi, etc. "
        "Any account left active can trigger lock screens after reset.",

        "If the device has a custom ROM, decide whether to flash back to stock. "
        "Most buyers expect stock Android. Selling with a custom ROM is fine if "
        "you disclose it clearly and the buyer knows what they're getting.",

        "If flashing back to stock: follow the device-specific instructions on "
        "the LineageOS wiki or your ROM's documentation. For Samsung, use Odin "
        "with an official stock firmware package from SamFW.",

        "After flashing stock (or if staying on custom ROM): "
        "Settings → System → Reset → Factory Data Reset. "
        "This wipes apps, data, and accounts.",

        "If the device supports encryption (Android 6+, which is all modern devices): "
        "the factory reset already makes your data unrecoverable in practice "
        "since the encryption keys are wiped. No need to overwrite storage manually.",

        "Re-lock the bootloader if you flashed back to stock. "
        "fastboot flashing lock (or fastboot oem lock for older devices). "
        "This returns the device to a factory-locked state.",

        "Boot the device after reset and stop at the setup wizard. "
        "Hand it to the buyer here — do not proceed through setup yourself.",
    ],
    "notes": (
        "The two critical steps are: remove Google account BEFORE factory reset, "
        "and re-lock the bootloader if you're selling to someone who doesn't want "
        "to flash custom software."
    ),
}

_SELL_WITH_CUSTOM_ROM = {
    "guide_type":  "sell",
    "title":       "Selling a device with a custom ROM installed",
    "source":      "Droidify",
    "source_url":  None,
    "codename":    "universal",
    "steps": [
        "Remove all personal accounts from the custom ROM's settings. "
        "Even on a custom ROM, Google FRP can trigger if accounts aren't removed before reset.",

        "Remove any Magisk modules that contain personal data or keys. "
        "Modules like banking app patches, certificate installers, or "
        "work profile configurations should be removed.",

        "Factory reset from within the custom ROM — Settings → System → Reset. "
        "Or use the recovery's wipe function: Wipe → Format Data.",

        "Disclose the custom ROM clearly in your listing. "
        "State the ROM name, Android version, and whether the bootloader is unlocked. "
        "A buyer who doesn't know what they're getting will leave negative feedback.",

        "Include basic instructions or a link to the ROM's XDA thread. "
        "A buyer who's new to custom ROMs will appreciate knowing where to get support.",
    ],
    "notes": (
        "Selling with a custom ROM is fine for the right buyer. "
        "Be upfront about it — 'custom ROM installed, bootloader unlocked' "
        "in the listing title saves everyone time."
    ),
}

_ALL_GUIDES = [
    _BUY_GENERAL,
    _BUY_SAMSUNG,
    _BUY_XIAOMI,
    _BUY_GOOGLE,
    _SELL_GENERAL,
    _SELL_WITH_CUSTOM_ROM,
]

def get_resell_guides(
    guide_type: str | None = None,
    manufacturer: str | None = None,
) -> list[dict]:
    """Return buying and selling guides, optionally filtered by guide_type or manufacturer."""
    result = list(_ALL_GUIDES)

    if guide_type:
        result = [g for g in result if g["guide_type"] == guide_type]

    if manufacturer:
        mfr_lower = manufacturer.lower()
        result = [
            g for g in result
            if g.get("manufacturer", "").lower() == mfr_lower or
               g.get("manufacturer") is None
        ]

    return result
