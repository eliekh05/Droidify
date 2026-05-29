"""
unofficialtwrp.com scraper — WordPress REST API
6,200+ posts covering unofficial TWRP builds for devices not in official TWRP.
Covers: Tecno (985), Oppo/Realme (784), Xiaomi (437), Infinix (521),
        Samsung (213), Motorola (81), Huawei (81), ZTE (79), and 70+ more brands.

Each post = one device unofficial TWRP build.
Uses WordPress REST API — no SourceForge, no scraping HTML.
Fetches ALL pages concurrently (63 pages × 100 posts = ~6,200 entries).
"""
import re
import asyncio
import httpx
from bs4 import BeautifulSoup
from ..services.cache import get as cache_get, set as cache_set

_API_BASE  = "https://unofficialtwrp.com/wp-json/wp/v2/posts"
_PER_PAGE  = 100
_TIMEOUT   = 20
_HEADERS   = {"User-Agent": "DroidifyBot/2.0 (+https://github.com/eliekh05/Droidify)"}

# Category ID → manufacturer name
_CAT_NAMES = {
    95: "Acer", 638: "Alcatel", 684: "Allview", 711: "Archos",
    736: "Asus", 909: "Blackview", 781: "BLU", 796: "Bluboo",
    931: "BQ", 2996: "Dexp", 2930: "Digma", 823: "Doogee",
    1640: "Elephone", 3081: "Fly", 1027: "Gionee", 3293: "Haier",
    2229: "HTC", 825: "Huawei", 1731: "Infinix", 3571: "Itel",
    1858: "Lava", 1922: "Leagoo", 1903: "Lenovo", 1231: "LG",
    5117: "Meizu", 1047: "Micromax", 920: "Motorola", 14650: "Motorola",
    2853: "Nokia", 10922: "OnePlus", 1432: "Oppo", 147: "Other",
    2065: "Oukitel", 4884: "Panasonic", 14648: "RedMagic",
    1004: "Samsung", 4037: "Sony", 14651: "Teclast", 2882: "Tecno",
    172: "Ulefone", 184: "Umidigi", 14652: "Unihertz", 1505: "Vernee",
    1051: "Vivo", 1179: "Xiaomi", 833: "ZTE", 1995: "Symphony",
    1382: "Walton", 1814: "Wiko", 5205: "Vertex", 1002: "Cubot",
    210: "Coolpad", 1183: "Condor", 1009: "Cherry Mobile",
    4365: "Mediatek", 3956: "Maze", 3407: "Inoi",
}

# Words to strip from slugs before treating remainder as codename
_SLUG_STRIP = re.compile(
    r'(?:unofficial[-_]?)?(?:twrp|orangefox|ofox|shrp|pbrp|recovery)[-_]?'
    r'[\d.]*[-_]?(?:root|install|how[-_]to|update|guide|for[-_])?',
    re.IGNORECASE,
)
_KNOWN_BRANDS = re.compile(
    r'^(?:samsung|xiaomi|redmi|poco|realme|oppo|vivo|oneplus|motorola|moto|'
    r'huawei|nokia|asus|rog|lg|sony|tecno|infinix|itel|htc|lenovo|zte|'
    r'alcatel|wiko|umidigi|oukitel|doogee|blackview|ulefone|blu|coolpad|'
    r'symphony|walton|honor|meizu|sharp|fujitsu|panasonic|google|pixel)[-_]',
    re.IGNORECASE,
)


def _extract_codename(title: str, slug: str) -> str | None:
    """
    Extract device codename from post title or slug.
    Priority:
      1. Parenthesised token in title: "TWRP for Galaxy A52 (a52q)"
      2. Bracket token in title: "TWRP [a52q] ..."
      3. Slug after stripping TWRP/version/brand noise
    """
    # 1. Parentheses — most reliable
    m = re.search(r'\(([a-z][a-z0-9_]{2,20})\)', title, re.IGNORECASE)
    if m:
        return m.group(1).lower()

    # 2. Square brackets
    m = re.search(r'\[([a-z][a-z0-9_]{2,20})\]', title, re.IGNORECASE)
    if m:
        return m.group(1).lower()

    # 3. Slug processing — strip TWRP/version/install noise
    clean = _SLUG_STRIP.sub('', slug)
    # Strip leading brand names
    clean = _KNOWN_BRANDS.sub('', clean)
    # Clean separators
    clean = clean.strip('-_').replace('-', '_')
    # Must look like a codename: lowercase letters+digits+underscore, 3-20 chars
    if re.match(r'^[a-z][a-z0-9_]{2,19}$', clean) and '_' not in clean[:2]:
        return clean

    return None


def _extract_manufacturer(categories: list[int], title: str) -> str:
    for cat_id in categories:
        if cat_id in _CAT_NAMES:
            return _CAT_NAMES[cat_id]
    brands = [
        "Samsung", "Xiaomi", "Redmi", "Poco", "Realme", "Oppo", "Vivo",
        "OnePlus", "Motorola", "Huawei", "Nokia", "Asus", "LG", "Sony",
        "Tecno", "Infinix", "Itel", "HTC", "Lenovo", "ZTE", "Alcatel",
    ]
    tl = title.lower()
    for brand in brands:
        if brand.lower() in tl:
            return brand
    return "Unknown"


async def _fetch_page(client: httpx.AsyncClient, page: int) -> list[dict]:
    try:
        r = await client.get(
            _API_BASE,
            params={
                "per_page": _PER_PAGE,
                "page": page,
                "_fields": "id,title,slug,link,categories",
                "status": "publish",
            },
        )
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []


async def get_unofficialtwrp_devices() -> list[dict]:
    """Fetch ALL unofficial TWRP posts concurrently — all ~6,200 entries."""
    ck = "roms:unofficialtwrp"
    if c := await cache_get(ck):
        return c

    results: list[dict] = []
    seen: set[str] = set()

    try:
        async with httpx.AsyncClient(
            timeout=_TIMEOUT,
            headers=_HEADERS,
            follow_redirects=True,
        ) as client:
            # Fetch page 1 to discover total page count
            resp = await client.get(
                _API_BASE,
                params={
                    "per_page": _PER_PAGE,
                    "page": 1,
                    "_fields": "id,title,slug,link,categories",
                    "status": "publish",
                },
            )
            resp.raise_for_status()
            total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
            all_posts = list(resp.json())

            # Fetch ALL remaining pages concurrently in batches of 10
            # to avoid overwhelming the server
            remaining = list(range(2, total_pages + 1))
            batch_size = 10
            for i in range(0, len(remaining), batch_size):
                batch = remaining[i : i + batch_size]
                pages = await asyncio.gather(
                    *[_fetch_page(client, p) for p in batch],
                    return_exceptions=True,
                )
                for page_data in pages:
                    if isinstance(page_data, list):
                        all_posts.extend(page_data)
                # Small delay between batches — be polite
                if i + batch_size < len(remaining):
                    await asyncio.sleep(0.3)

    except Exception:
        return []

    skip_kw = {"how to", "guide", "tutorial", "firmware flash file", "firmware file"}

    for post in all_posts:
        slug  = post.get("slug", "")
        title = BeautifulSoup(
            post.get("title", {}).get("rendered", ""), "html.parser"
        ).get_text().strip()
        link  = post.get("link", "")
        cats  = post.get("categories", [])

        if slug in seen:
            continue
        seen.add(slug)

        if not title or any(kw in title.lower() for kw in skip_kw):
            continue

        codename     = _extract_codename(title, slug)
        manufacturer = _extract_manufacturer(cats, title)

        # Only include entries where we extracted a real codename
        if not codename:
            continue

        results.append({
            "name":         title,
            "codename":     codename,
            "manufacturer": manufacturer,
            "android_base": None,
            "rom_type":     "recovery",
            "status":       "active",
            "official":     False,
            "maintainer":   "Unofficial Community",
            "source_url":   link,
            "download_url": link,
            "data_source":  "unofficialtwrp",
            "rom_name":     "Unofficial TWRP",
            "description":  f"Unofficial TWRP recovery build — {title}",
        })

    await cache_set(ck, results, ttl=7200)
    return results
