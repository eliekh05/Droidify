"""
android_versions.py — Complete Android version history, fully hardcoded.

Every release that shipped on real devices, with correct API levels,
release dates, and official codenames. No scraping. No live fetching.
No network calls. The data does not change — old Android versions
do not get new API levels. New versions are added here manually
when Google releases them.

Why hardcoded: live sources (apilevels.com, Wikipedia) are inconsistent
on subversions. Wikipedia's table format changes without notice and
breaks parsers. The data is stable — this is the right approach.

Sources verified against:
  - developer.android.com/tools/releases/platforms
  - source.android.com/docs/setup/about/build-numbers
  - en.wikipedia.org/wiki/Android_version_history
"""

from app.services.cache import get as cache_get, set as cache_set

# ── Status helper ──────────────────────────────────────────────────────────────
def _status(ver: str, year: int) -> str:
    """
    Status verified against endoflife.date/android — June 2026:
    - active:      Android 14, 15, 16 — isMaintained=True per endoflife.date
    - unsupported: Android 13 and below — all EOL per Google security bulletins

    Android 13 reached EOL on 2026-03-02.
    Android 12/12L reached EOL on 2025-03-03.
    Android 11 reached EOL on 2024-02-05.
    Source: https://endoflife.date/android
    """
    try:
        major = float(ver.split()[0]) if ver else 0
    except (ValueError, IndexError):
        major = 0

    if major >= 14:  return "active"       # 14, 15, 16 — maintained
    return "unsupported"                   # 13 and below — all EOL


# ── Master version table ───────────────────────────────────────────────────────
# Every row = one distinct API level that shipped on real devices.
# Columns: version_number, codename, api_level, release_date, release_year
_VERSIONS = [
    # ── Pre-dessert ─────────────────────────────────────────────────────────────
    ("1.0",   None,                  1,  "2008-09-23", 2008),
    ("1.1",   "Petit Four",          2,  "2009-02-09", 2009),
    # ── Cupcake / Donut ─────────────────────────────────────────────────────────
    ("1.5",   "Cupcake",             3,  "2009-04-27", 2009),
    ("1.6",   "Donut",               4,  "2009-09-15", 2009),
    # ── Eclair ──────────────────────────────────────────────────────────────────
    ("2.0",   "Eclair",              5,  "2009-10-26", 2009),
    ("2.0.1", "Eclair",              6,  "2009-12-03", 2009),
    ("2.1",   "Eclair",              7,  "2010-01-12", 2010),
    # ── Froyo ───────────────────────────────────────────────────────────────────
    ("2.2",   "Froyo",               8,  "2010-05-20", 2010),
    ("2.2.1", "Froyo",               8,  "2011-01-18", 2011),
    ("2.2.2", "Froyo",               8,  "2011-01-22", 2011),
    ("2.2.3", "Froyo",               8,  "2011-11-21", 2011),
    # ── Gingerbread ─────────────────────────────────────────────────────────────
    ("2.3",   "Gingerbread",         9,  "2010-12-06", 2010),
    ("2.3.1", "Gingerbread",         9,  "2010-12-09", 2010),
    ("2.3.2", "Gingerbread",         9,  "2011-01-10", 2011),
    ("2.3.3", "Gingerbread",         10, "2011-02-09", 2011),
    ("2.3.4", "Gingerbread",         10, "2011-04-28", 2011),
    ("2.3.5", "Gingerbread",         10, "2011-07-25", 2011),
    ("2.3.6", "Gingerbread",         10, "2011-09-02", 2011),
    ("2.3.7", "Gingerbread",         10, "2011-09-21", 2011),
    # ── Honeycomb (tablets only) ─────────────────────────────────────────────────
    ("3.0",   "Honeycomb",           11, "2011-02-22", 2011),
    ("3.1",   "Honeycomb",           12, "2011-05-10", 2011),
    ("3.2",   "Honeycomb",           13, "2011-07-15", 2011),
    ("3.2.1", "Honeycomb",           13, "2011-09-20", 2011),
    ("3.2.2", "Honeycomb",           13, "2011-09-30", 2011),
    ("3.2.4", "Honeycomb",           13, "2012-03-29", 2012),
    ("3.2.6", "Honeycomb",           13, "2012-07-05", 2012),
    # ── Ice Cream Sandwich ──────────────────────────────────────────────────────
    ("4.0",   "Ice Cream Sandwich",  14, "2011-10-18", 2011),
    ("4.0.1", "Ice Cream Sandwich",  14, "2011-10-21", 2011),
    ("4.0.2", "Ice Cream Sandwich",  14, "2011-11-28", 2011),
    ("4.0.3", "Ice Cream Sandwich",  15, "2011-12-16", 2011),
    ("4.0.4", "Ice Cream Sandwich",  15, "2012-03-29", 2012),
    # ── Jelly Bean ──────────────────────────────────────────────────────────────
    ("4.1",   "Jelly Bean",          16, "2012-07-09", 2012),
    ("4.1.1", "Jelly Bean",          16, "2012-07-25", 2012),
    ("4.1.2", "Jelly Bean",          16, "2012-10-09", 2012),
    ("4.2",   "Jelly Bean",          17, "2012-11-13", 2012),
    ("4.2.1", "Jelly Bean",          17, "2012-11-27", 2012),
    ("4.2.2", "Jelly Bean",          17, "2013-02-11", 2013),
    ("4.3",   "Jelly Bean",          18, "2013-07-24", 2013),
    ("4.3.1", "Jelly Bean",          18, "2013-10-03", 2013),
    # ── KitKat ──────────────────────────────────────────────────────────────────
    ("4.4",   "KitKat",              19, "2013-10-31", 2013),
    ("4.4.1", "KitKat",              19, "2013-12-05", 2013),
    ("4.4.2", "KitKat",              19, "2013-12-09", 2013),
    ("4.4.3", "KitKat",              19, "2014-06-02", 2014),
    ("4.4.4", "KitKat",              19, "2014-06-19", 2014),
    ("4.4W",  "KitKat Watch",        20, "2014-06-25", 2014),
    ("4.4W.1","KitKat Watch",        20, "2014-09-06", 2014),
    ("4.4W.2","KitKat Watch",        20, "2014-10-21", 2014),
    # ── Lollipop ────────────────────────────────────────────────────────────────
    ("5.0",   "Lollipop",            21, "2014-11-12", 2014),
    ("5.0.1", "Lollipop",            21, "2014-12-02", 2014),
    ("5.0.2", "Lollipop",            21, "2014-12-19", 2014),
    ("5.1",   "Lollipop",            22, "2015-03-02", 2015),
    ("5.1.1", "Lollipop",            22, "2015-04-20", 2015),
    # ── Marshmallow ─────────────────────────────────────────────────────────────
    ("6.0",   "Marshmallow",         23, "2015-10-05", 2015),
    ("6.0.1", "Marshmallow",         23, "2015-12-07", 2015),
    # ── Nougat ──────────────────────────────────────────────────────────────────
    ("7.0",   "Nougat",              24, "2016-08-22", 2016),
    ("7.1",   "Nougat",              25, "2016-10-04", 2016),
    ("7.1.1", "Nougat",              25, "2016-12-05", 2016),
    ("7.1.2", "Nougat",              25, "2017-04-03", 2017),
    # ── Oreo ────────────────────────────────────────────────────────────────────
    ("8.0",   "Oreo",                26, "2017-08-21", 2017),
    ("8.1",   "Oreo",                27, "2017-12-05", 2017),
    # ── Pie ─────────────────────────────────────────────────────────────────────
    ("9",     "Pie",                 28, "2018-08-06", 2018),
    # ── Android 10 ──────────────────────────────────────────────────────────────
    ("10",    "Quince Tart",         29, "2019-09-03", 2019),
    # ── Android 11 ──────────────────────────────────────────────────────────────
    ("11",    "Red Velvet Cake",     30, "2020-09-08", 2020),
    # ── Android 12 ──────────────────────────────────────────────────────────────
    ("12",    "Snow Cone",           31, "2021-10-04", 2021),
    ("12L",   "Snow Cone v2",        32, "2022-03-07", 2022),
    # ── Android 13 ──────────────────────────────────────────────────────────────
    ("13",    "Tiramisu",            33, "2022-08-15", 2022),
    # ── Android 14 ──────────────────────────────────────────────────────────────
    ("14",    "Upside Down Cake",    34, "2023-10-04", 2023),
    # ── Android 15 ──────────────────────────────────────────────────────────────
    ("15",    "Vanilla Ice Cream",   35, "2024-10-15", 2024),
    # ── Android 16 ──────────────────────────────────────────────────────────────
    ("16",    "Baklava",             36, "2025-06-03", 2025),
    # ── Android 17 ──────────────────────────────────────────────────────────────
    ("17",    "Cinnamon Bun",        37, "2026-06-16", 2026),
]


def _build_versions() -> list[dict]:
    out = []
    for ver, codename, api, date, year in _VERSIONS:
        out.append({
            "version_number":  ver,
            "codename":        codename,
            "api_level":       api,
            "release_date":    date,
            "release_year":    year,
            "is_beta":         False,
            "status":          _status(ver, year),
            "source":          "hardcoded",
        })
    return out


async def get_android_versions() -> list[dict]:
    ck = "android_versions_v7"
    if cached := await cache_get(ck):
        return cached
    versions = _build_versions()
    await cache_set(ck, versions, ttl=86400)  # 24h — data never changes
    return versions


async def get_android_versions_dict() -> dict:
    """API-friendly wrapper returning {total, versions}."""
    versions = await get_android_versions()
    return {"total": len(versions), "versions": versions}
