"""Samsung stock firmware links via samfw.com — no auth required."""
from app.services.cache import get as cache_get, set as cache_set

# Known Samsung codename → model number mappings
# Sourced from LineageOS wiki and Samsung's public device pages
SAMSUNG_MODELS: dict[str, list[str]] = {
    # Galaxy S series
    "beyond0lte":  ["SM-G970F", "SM-G970U"],
    "beyond1lte":  ["SM-G973F", "SM-G973U"],
    "beyond2lte":  ["SM-G975F", "SM-G975U"],
    "beyondxlte":  ["SM-G977B", "SM-G977U"],
    "r0q":         ["SM-G991B", "SM-G991U"],   # S21
    "o1q":         ["SM-G996B", "SM-G996U"],   # S21+
    "p3q":         ["SM-G998B", "SM-G998U"],   # S21 Ultra
    "r8q":         ["SM-G780F", "SM-G780G"],   # S20 FE
    "a52sxq":      ["SM-A528B"],               # A52s
    "a53x":        ["SM-A536B", "SM-A536U"],   # A53
    "a72q":        ["SM-A725F"],               # A72
    "a73xq":       ["SM-A736B"],               # A73
    "c1s":         ["SM-G991B"],               # S21 alt
    "c2q":         ["SM-G996B"],               # S21+ alt
    # Galaxy A series
    "a3y17lte":    ["SM-A320F"],
    "a5y17lte":    ["SM-A520F"],
    "a7y17lte":    ["SM-A720F"],
    "a50":         ["SM-A505F", "SM-A505G"],
    "a51":         ["SM-A515F"],
    "a70q":        ["SM-A705F"],
    "a71":         ["SM-A715F"],
    "a10":         ["SM-A105F"],
    "a10s":        ["SM-A107F"],
    "a20":         ["SM-A205F"],
    "a20e":        ["SM-A202F"],
    "a20s":        ["SM-A207F"],
    "a30":         ["SM-A305F"],
    "a30s":        ["SM-A307F"],
    "a40":         ["SM-A405F"],
    "a40s":        ["SM-A3050"],
    "a60q":        ["SM-A6060"],
    "a80":         ["SM-A805F"],
    # Galaxy Note series
    "crownlte":    ["SM-N960F", "SM-N960U"],   # Note 9
    "d1":          ["SM-N970F", "SM-N970U"],   # Note 10
    "d1x":         ["SM-N975F", "SM-N975U"],   # Note 10+
    "d2q":         ["SM-N981B", "SM-N981U"],   # Note 20
    "d2xq":        ["SM-N986B", "SM-N986U"],   # Note 20 Ultra
    "d2s":         ["SM-N981B"],
    # Galaxy Tab
    "gts7l":       ["SM-T870", "SM-T875"],
    "gts7xl":      ["SM-T970", "SM-T975"],
    "gts8":        ["SM-X700", "SM-X706B"],
    "gts9fe":      ["SM-X510", "SM-X516B"],
    # Galaxy M series
    "m51":         ["SM-M515F"],
    "m31":         ["SM-M315F"],
    "m21":         ["SM-M215F"],
    # Galaxy F series
    "f62":         ["SM-E625F"],
    "f41":         ["SM-F415F"],
    # Galaxy Z series
    "b0q":         ["SM-F936B"],               # Z Fold4
    "q4q":         ["SM-F721B"],               # Z Flip4
    "gts7fewifi":  ["SM-T733"],
}

def get_samfw_link(codename: str, model: str | None = None) -> str | None:
    """Return samfw.com link for a Samsung device."""
    if model:
        return f"https://samfw.com/{model}"
    models = SAMSUNG_MODELS.get(codename.lower())
    if models:
        return f"https://samfw.com/{models[0]}"
    return None

def get_samsung_models(codename: str) -> list[str]:
    """Return known model numbers for a Samsung codename."""
    return SAMSUNG_MODELS.get(codename.lower(), [])

async def get_samfw_for_device(codename: str) -> list[dict]:
    """
    Return SamFW firmware entries for a Samsung device codename.
    Returns list of stock firmware links for each known model number.
    """
    ck = f"samfw:{codename}"
    cached = await cache_get(ck)
    if cached is not None:
        return cached

    models = get_samsung_models(codename)
    if not models:
        # Try to infer from codename — Samsung codenames often have model hints
        # e.g. SM-A536B → a53x, but we can't reverse this reliably
        await cache_set(ck, [], ttl=86400)
        return []

    entries = []
    for model in models:
        entries.append({
            "name":         f"Stock firmware ({model})",
            "codename":     codename,
            "model":        model,
            "source":       "samfw",
            "type":         "stock_firmware",
            "download_url": f"https://samfw.com/{model}",
            "description":  f"Official Samsung firmware for {model} — download via SamFW.com",
        })

    await cache_set(ck, entries, ttl=86400)
    return entries
