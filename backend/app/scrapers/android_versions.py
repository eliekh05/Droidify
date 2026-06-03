"""Android version history — live from apilevels.com, Wikipedia fallback, static fallback."""
import re
from html import unescape

from app.services.cache import get as cache_get, set as cache_set
from app.services.http import fetch, get_client

APILEVELS_URL = "https://apilevels.com"

# Authoritative version_code → codename mapping (from developer.android.com)
# Used to correct codename when rowspan inheritance gives wrong value
_VCODE_CODENAME: dict[str, str] = {
    "BASE": None, "BASE_1_1": "Petit Four",
    "CUPCAKE": "Cupcake", "DONUT": "Donut",
    "ECLAIR": "Eclair", "ECLAIR_0_1": "Eclair", "ECLAIR_MR1": "Eclair",
    "FROYO": "Froyo",
    "GINGERBREAD": "Gingerbread", "GINGERBREAD_MR1": "Gingerbread",
    "HONEYCOMB": "Honeycomb", "HONEYCOMB_MR1": "Honeycomb", "HONEYCOMB_MR2": "Honeycomb",
    "ICE_CREAM_SANDWICH": "Ice Cream Sandwich", "ICE_CREAM_SANDWICH_MR1": "Ice Cream Sandwich",
    "JELLY_BEAN": "Jelly Bean", "JELLY_BEAN_MR1": "Jelly Bean", "JELLY_BEAN_MR2": "Jelly Bean",
    "KITKAT": "KitKat", "KITKAT_WATCH": "KitKat Watch",
    "LOLLIPOP": "Lollipop", "LOLLIPOP_MR1": "Lollipop",
    "M": "Marshmallow",
    "N": "Nougat", "N_MR1": "Nougat",
    "O": "Oreo", "O_MR1": "Oreo",
    "P": "Pie",
    "Q": "Quince Tart",
    "R": "Red Velvet Cake",
    "S": "Snow Cone", "S_V2": "Snow Cone v2",
    "TIRAMISU": "Tiramisu",
    "UPSIDE_DOWN_CAKE": "Upside Down Cake",
    "VANILLA_ICE_CREAM": "Vanilla Ice Cream",
    "BAKLAVA": "Baklava",
    "CINNAMON_BUN": "Cinnamon Bun",
}

WIKIPEDIA_URL = (
    "https://en.wikipedia.org/w/api.php"
    "?action=parse&page=Android_version_history"
    "&prop=text&format=json&disableeditsection=1"
)

_SKIP_KW = ("Jetpack", "targetSdk", "Google Play", "Earlier", "AndroidX",
            "minSdk", "requirement", "library")
_MONTH_MAP = {
    "january":"01","february":"02","march":"03","april":"04",
    "may":"05","june":"06","july":"07","august":"08",
    "september":"09","october":"10","november":"11","december":"12",
}

def _ct(cell) -> str:
    """Clean cell text — strip <style> and <sup> tags, collapse whitespace."""
    for tag in cell.find_all(["style", "sup"]):
        tag.decompose()
    t = unescape(cell.get_text(separator=" ", strip=True))
    return re.sub(r"\s{2,}", " ", t).strip()

def _version_code(raw: str) -> str | None:
    """Extract first valid UPPER_SNAKE_CASE version code from cell text."""
    # Single-letter codes: M, N, O, P, Q, R, S (Android 6-12)
    if re.match(r"^[A-Z]$", raw.strip()):
        return raw.strip()
    # Multi-char codes: BAKLAVA, CINNAMON_BUN, JELLY_BEAN_MR1, ...
    codes = re.findall(r"\b([A-Z][A-Z_0-9]{2,})\b", raw)
    skip  = {"BETA", "TBD", "API", "SDK", "ABI", "PREVIEW"}
    valid = [c for c in codes if c not in skip]
    return valid[0] if valid else None

def _parse_date(year: int | None) -> str | None:
    return f"{year}-01-01" if year and year >= 2008 else None

def _parse_status(api: int, is_beta: bool, release_year: int | None = None) -> str:
    """Parse support status string to active/preview/discontinued."""
    if is_beta:
        return "partial"
    if release_year is None:
        # Year TBD = developer preview, not publicly released yet
        return "partial"
    if api >= 34:
        return "active"
    return "unsupported"

def _parse_row(texts: list[str]) -> list[dict] | None:
    """
    Parse one table row from apilevels.com into a list of API-level dicts.
    Returns None for rows that should be skipped.
    """
    if not texts:
        return None
    n = len(texts)

    # Skip 1-cell notice rows
    if n == 1:
        return None

    # Is the first cell an Android major version label?
    is_android = bool(re.match(r"^Android\s+\d", texts[0], re.I))

    if is_android:
        android_cell = texts[0]
        api_cell     = texts[1] if n > 1 else ""
        vcode_cell   = texts[2] if n > 2 else ""
        cn_cell      = texts[3] if n > 3 else ""
        usage_cell   = texts[4] if n > 4 else ""
        year_cell    = texts[5] if n > 5 else ""
    else:
        android_cell = ""
        api_cell     = texts[0]
        vcode_cell   = texts[1] if n > 1 else ""
        cn_cell      = ""
        usage_cell   = ""
        year_cell    = ""
        # For 3-cell sub-rows: [api_cell, vcode_cell, X] — X is usage/year/codename
        if n == 3:
            x = texts[2]
            if re.search(r"\d+\.?\d*%|No data", x):  usage_cell = x
            elif re.search(r"\b20\d{2}\b", x):        year_cell  = x
            else:                                      cn_cell    = x
        elif n == 4:
            # [api, vcode, X, Y]
            x, y = texts[2], texts[3]
            if re.search(r"\d+\.?\d*%|No data", x):  usage_cell = x; year_cell = y
            else:                                      cn_cell = x; year_cell = y

    # API levels — a row can have one ("Level 35") or two sub-levels
    apis = [int(m) for m in re.findall(r"Level\s+(\d+)", api_cell, re.I)]
    if not apis:
        return None

    # Sub-version map: "Level 27 Android 8.1" → {27: "8.1"}
    sub_versions: dict[int, str] = {}
    for m in re.finditer(r"Level\s+(\d+)\s+Android\s+([\d.]+[\w.]*)", api_cell, re.I):
        sub_versions[int(m.group(1))] = m.group(2)

    # Android major from android_cell label
    android_major = ""
    if android_cell:
        am = re.search(r"Android\s+([\d.]+)", android_cell, re.I)
        if am:
            android_major = am.group(1)

    # Version code
    vcode = _version_code(vcode_cell)

    # Codename: reject noise values
    cn: str | None = None
    cn_raw = cn_cell.strip()
    if cn_raw and cn_raw not in ("None", "—", "-", "", "No data", "TBD"):
        cn = cn_raw

    # Year
    yr: int | None = None
    for src in [year_cell, api_cell]:
        ym = re.search(r"\b(200[89]|201\d|202[0-9])\b", src)
        if ym:
            yr = int(ym.group(1))
            break

    # Usage
    usage: float | None = None
    for src in [usage_cell]:
        um = re.search(r"(\d+\.?\d*)\s*%", src)
        if um:
            usage = float(um.group(1))
            break

    # Beta
    joined = " ".join(texts)
    is_beta = "BETA" in joined or "PREVIEW" in joined.upper()

    result = []
    for api in apis:
        ver = sub_versions.get(api, android_major)
        result.append({
            "api_level":        api,
            "version_number":   ver,
            "version_code":     vcode,
            "codename":         cn,
            "release_year":     yr,
            "cumulative_usage": usage,
            "is_beta":          is_beta,
        })
    return result

def _parse_apilevels(html: str) -> list[dict]:
    """Parse apilevels.com HTML → list of Android version dicts."""
    from bs4 import BeautifulSoup
    soup  = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="full-width")
    if not table:
        return []

    rows = table.find_all("tr")
    if not rows:
        return []

    # Track inherited (rowspan) values for: android_major, codename, year, usage
    # We track last_android_major to avoid inheriting codenames across Android versions
    last_android      = ""
    last_android_major = ""       # e.g. "4", "5", "12"  — major version number
    last_codename: str | None = None
    last_year:     int | None = None
    last_usage:    float | None = None

    all_entries: list[dict] = []

    for row in rows[1:]:  # skip header
        # Clean style/sup before reading text
        for tag in row.find_all(["style", "sup"]):
            tag.decompose()

        cells = row.find_all(["td", "th"])
        if not cells:
            continue

        texts = [_ct(c) for c in cells]
        joined = " ".join(texts)

        # Skip notice rows
        if len(cells) <= 2 and any(kw in joined for kw in _SKIP_KW):
            continue
        if len(cells) == 1:
            continue

        entries = _parse_row(texts)
        if not entries:
            continue

        # Update inherited values from this row
        for e in entries:
            if e["version_number"]:
                last_android = e["version_number"]
                # Extract major version number for cross-version boundary detection
                maj_m = re.match(r"^(\d+)", e["version_number"])
                if maj_m:
                    last_android_major = maj_m.group(1)
            if e["codename"] is not None:
                last_codename = e["codename"]
            if e["release_year"] is not None:
                last_year = e["release_year"]
            if e["cumulative_usage"] is not None:
                last_usage = e["cumulative_usage"]

        # Fill inherited values for fields that were rowspan'd
        for e in entries:
            if not e["version_number"] and last_android:
                e["version_number"] = last_android
            if e["codename"] is None:
                # Only inherit codename if same major Android version
                ver = e["version_number"] or ""
                maj_m = re.match(r"^(\d+)", ver)
                same_major = (maj_m and maj_m.group(1) == last_android_major)
                if same_major and last_codename:
                    e["codename"] = last_codename
            if e["release_year"] is None and last_year:
                e["release_year"] = last_year
            if e["cumulative_usage"] is None and last_usage:
                e["cumulative_usage"] = last_usage

        for e in entries:
            api = e["api_level"]
            status = _parse_status(api, e["is_beta"], e.get("release_year"))
            # Override codename with authoritative map when version_code is known
            codename = e["codename"]
            if e["version_code"] and e["version_code"] in _VCODE_CODENAME:
                codename = _VCODE_CODENAME[e["version_code"]]
            all_entries.append({
                "version_number":   e["version_number"] or "?",
                "codename":         codename,
                "api_level":        api,
                "version_code":     e["version_code"],
                "release_date":     _parse_date(e["release_year"]),
                "security_patch":   None,
                "release_year":     e["release_year"],
                "cumulative_usage": e["cumulative_usage"],
                "is_beta":          e["is_beta"],
                "status":           status,
                "source":           "apilevels.com",
                "source_url":       APILEVELS_URL,
            })

    # Sort + deduplicate by API level
    all_entries.sort(key=lambda x: x["api_level"])
    seen: set[int] = set()
    deduped: list[dict] = []
    for e in all_entries:
        if e["api_level"] not in seen:
            seen.add(e["api_level"])
            deduped.append(e)

    return deduped

def _parse_wikipedia(html: str) -> list[dict]:
    """Wikipedia fallback parser — minimal, just needs to work."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    target = None
    for tbl in soup.find_all("table", class_="wikitable"):
        hdr = " ".join(th.get_text(strip=True) for th in tbl.find_all("th")[:8])
        if "API" in hdr and "Version" in hdr:
            target = tbl; break
    if not target:
        return []

    results: list[dict] = []
    last_codename: str | None = None

    for row in target.find_all("tr")[1:]:
        cells = row.find_all(["td", "th"])
        n = len(cells)
        if n < 3:
            continue
        def ct2(i): return re.sub(r"<[^>]+>", "", str(cells[i])).strip() if i < n else ""
        if n < 5:
            ver_col = ct2(0); api_raw = ct2(1)
            codename = last_codename
        else:
            ver_col = ct2(2); api_raw = ct2(3)
            cn = re.sub(r"\[.*?\]", "", ct2(1)).strip()
            codename = (cn if cn and cn not in ("—","-","N/a") else last_codename)
            if codename: last_codename = codename

        ver_m = re.match(r"^([\d.]+[Lw]?)$", re.sub(r"\[.*$","",ver_col.split(":")[-1]).strip())
        if not ver_m: continue
        api_m = re.search(r"\b(\d+)\b", api_raw)
        if not api_m: continue
        api = int(api_m.group(1))
        pfx = ver_col.split(":")[0].lower() if ":" in ver_col else ""
        status = ("active" if "latest" in pfx or ("supported" in pfx and "un" not in pfx)
                  else "partial" if "preview" in pfx or "beta" in pfx
                  else "unsupported")
        yr_m = re.search(r"\b(200[89]|201\d|202[0-9])\b", ct2(4) if n > 4 else "")
        yr = int(yr_m.group(1)) if yr_m else None
        results.append({
            "version_number": ver_m.group(1), "codename": codename,
            "api_level": api, "version_code": None,
            "release_date": _parse_date(yr), "security_patch": None,
            "release_year": yr, "cumulative_usage": None, "is_beta": "preview" in pfx,
            "status": status, "source": "wikipedia",
            "source_url": "https://en.wikipedia.org/wiki/Android_version_history",
        })

    results.sort(key=lambda x: x["api_level"])
    seen: set[int] = set()
    deduped = []
    for r in results:
        if r["api_level"] not in seen:
            seen.add(r["api_level"]); deduped.append(r)
    return deduped

async def get_android_versions() -> list[dict]:
    """
    Fetch Android version history.
    Priority: apilevels.com → Wikipedia → static fallback.
    """
    ck = "android_versions_v5"
    cached = await cache_get(ck)
    if cached:
        return cached

    async with get_client() as client:
        resp_al = await fetch(client, APILEVELS_URL)
        resp_wp = await fetch(client, WIKIPEDIA_URL)

    # 1. apilevels.com
    if resp_al and resp_al.status_code == 200:
        try:
            versions = _parse_apilevels(resp_al.text)
            if len(versions) >= 25:
                await cache_set(ck, versions, ttl=3600)
                return versions
        except Exception:
            pass

    # 2. Wikipedia
    if resp_wp and resp_wp.status_code == 200:
        try:
            html = resp_wp.json()["parse"]["text"]["*"]
            versions = _parse_wikipedia(html)
            if len(versions) >= 20:
                await cache_set(ck, versions, ttl=3600)
                return versions
        except Exception:
            pass

    # 3. Static fallback
    versions = _static_fallback()
    await cache_set(ck, versions, ttl=600)
    return versions

def _static_fallback() -> list[dict]:
    """Built-in last-resort data — Android 1.0 → 17 Preview."""
    return [
        {"version_number":"1.0",  "codename":None,               "api_level":1,  "version_code":"BASE",                   "release_year":2008,"release_date":"2008-09-23","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"1.1",  "codename":"Petit Four",        "api_level":2,  "version_code":"BASE_1_1",               "release_year":2009,"release_date":"2009-02-09","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"1.5",  "codename":"Cupcake",           "api_level":3,  "version_code":"CUPCAKE",                "release_year":2009,"release_date":"2009-04-27","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"1.6",  "codename":"Donut",             "api_level":4,  "version_code":"DONUT",                  "release_year":2009,"release_date":"2009-09-15","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"2.0",  "codename":"Eclair",            "api_level":5,  "version_code":"ECLAIR",                 "release_year":2009,"release_date":"2009-10-27","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"2.0.1","codename":"Eclair",            "api_level":6,  "version_code":"ECLAIR_0_1",             "release_year":2009,"release_date":"2009-12-03","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"2.1",  "codename":"Eclair",            "api_level":7,  "version_code":"ECLAIR_MR1",             "release_year":2010,"release_date":"2010-01-11","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"2.2",  "codename":"Froyo",             "api_level":8,  "version_code":"FROYO",                  "release_year":2010,"release_date":"2010-05-20","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"2.3",  "codename":"Gingerbread",       "api_level":9,  "version_code":"GINGERBREAD",            "release_year":2010,"release_date":"2010-12-06","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"2.3.3","codename":"Gingerbread",       "api_level":10, "version_code":"GINGERBREAD_MR1",        "release_year":2011,"release_date":"2011-02-09","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"3.0",  "codename":"Honeycomb",         "api_level":11, "version_code":"HONEYCOMB",              "release_year":2011,"release_date":"2011-02-22","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"3.1",  "codename":"Honeycomb",         "api_level":12, "version_code":"HONEYCOMB_MR1",          "release_year":2011,"release_date":"2011-05-10","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"3.2",  "codename":"Honeycomb",         "api_level":13, "version_code":"HONEYCOMB_MR2",          "release_year":2011,"release_date":"2011-07-15","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"4.0",  "codename":"Ice Cream Sandwich","api_level":14, "version_code":"ICE_CREAM_SANDWICH",     "release_year":2011,"release_date":"2011-10-18","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"4.0.3","codename":"Ice Cream Sandwich","api_level":15, "version_code":"ICE_CREAM_SANDWICH_MR1", "release_year":2011,"release_date":"2011-12-16","security_patch":None,"cumulative_usage":99.9,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"4.1",  "codename":"Jelly Bean",        "api_level":16, "version_code":"JELLY_BEAN",             "release_year":2012,"release_date":"2012-07-09","security_patch":None,"cumulative_usage":99.9,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"4.2",  "codename":"Jelly Bean",        "api_level":17, "version_code":"JELLY_BEAN_MR1",         "release_year":2012,"release_date":"2012-11-13","security_patch":None,"cumulative_usage":99.9,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"4.3",  "codename":"Jelly Bean",        "api_level":18, "version_code":"JELLY_BEAN_MR2",         "release_year":2013,"release_date":"2013-07-24","security_patch":None,"cumulative_usage":99.9,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"4.4",  "codename":"KitKat",            "api_level":19, "version_code":"KITKAT",                 "release_year":2013,"release_date":"2013-10-31","security_patch":None,"cumulative_usage":None,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"4.4W", "codename":"KitKat Watch",      "api_level":20, "version_code":"KITKAT_WATCH",           "release_year":2014,"release_date":"2014-06-25","security_patch":None,"cumulative_usage":99.8,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"5.0",  "codename":"Lollipop",          "api_level":21, "version_code":"LOLLIPOP",               "release_year":2014,"release_date":"2014-11-04","security_patch":None,"cumulative_usage":99.8,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"5.1",  "codename":"Lollipop",          "api_level":22, "version_code":"LOLLIPOP_MR1",           "release_year":2015,"release_date":"2015-03-02","security_patch":None,"cumulative_usage":97.8,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"6.0",  "codename":"Marshmallow",       "api_level":23, "version_code":"M",                      "release_year":2015,"release_date":"2015-09-29","security_patch":None,"cumulative_usage":97.5,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"7.0",  "codename":"Nougat",            "api_level":24, "version_code":"N",                      "release_year":2016,"release_date":"2016-08-22","security_patch":None,"cumulative_usage":95.7,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"7.1",  "codename":"Nougat",            "api_level":25, "version_code":"N_MR1",                  "release_year":2016,"release_date":"2016-10-04","security_patch":None,"cumulative_usage":95.1,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"8.0",  "codename":"Oreo",              "api_level":26, "version_code":"O",                      "release_year":2017,"release_date":"2017-08-21","security_patch":None,"cumulative_usage":94.8,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"8.1",  "codename":"Oreo",              "api_level":27, "version_code":"O_MR1",                  "release_year":2017,"release_date":"2017-12-05","security_patch":None,"cumulative_usage":93.4,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"9",    "codename":"Pie",               "api_level":28, "version_code":"P",                      "release_year":2018,"release_date":"2018-08-06","security_patch":None,"cumulative_usage":91.8,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"10",   "codename":"Quince Tart",       "api_level":29, "version_code":"Q",                      "release_year":2019,"release_date":"2019-09-03","security_patch":None,"cumulative_usage":89.1,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"11",   "codename":"Red Velvet Cake",   "api_level":30, "version_code":"R",                      "release_year":2020,"release_date":"2020-09-08","security_patch":None,"cumulative_usage":84.4,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"12",   "codename":"Snow Cone",         "api_level":31, "version_code":"S",                      "release_year":2021,"release_date":"2021-10-04","security_patch":None,"cumulative_usage":75.3,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"12L",  "codename":"Snow Cone v2",      "api_level":32, "version_code":"S_V2",                   "release_year":2022,"release_date":"2022-03-07","security_patch":None,"cumulative_usage":75.3,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"13",   "codename":"Tiramisu",          "api_level":33, "version_code":"TIRAMISU",               "release_year":2022,"release_date":"2022-08-15","security_patch":None,"cumulative_usage":64.4,"is_beta":False,"status":"unsupported","source":"static_fallback"},
        {"version_number":"14",   "codename":"Upside Down Cake",  "api_level":34, "version_code":"UPSIDE_DOWN_CAKE",       "release_year":2023,"release_date":"2023-10-04","security_patch":None,"cumulative_usage":49.4,"is_beta":False,"status":"active","source":"static_fallback"},
        {"version_number":"15",   "codename":"Vanilla Ice Cream", "api_level":35, "version_code":"VANILLA_ICE_CREAM",      "release_year":2024,"release_date":"2024-09-03","security_patch":None,"cumulative_usage":34.4,"is_beta":False,"status":"active","source":"static_fallback"},
        {"version_number":"16",   "codename":"Baklava",           "api_level":36, "version_code":"BAKLAVA",                "release_year":2025,"release_date":"2025-06-10","security_patch":"2026-05-01","cumulative_usage":4.6,"is_beta":False,"status":"active","source":"static_fallback"},
        {"version_number":"17",   "codename":"Cinnamon Bun",      "api_level":37, "version_code":"CINNAMON_BUN",           "release_year":2026,"release_date":None,"security_patch":None,"cumulative_usage":0.0,"is_beta":True,"status":"partial","source":"static_fallback"},
    ]
