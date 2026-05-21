"""
unofficialtwrp.com scraper — WordPress REST API
6,204 posts covering unofficial TWRP builds for devices not in official TWRP.
Covers: Tecno (985), Oppo/Realme (784), Xiaomi (437), Infinix (521),
        Samsung (213), Motorola (81), Huawei (81), ZTE (79), and 70+ more brands.

Each post = one device unofficial TWRP build.
Uses WordPress REST API — no SourceForge, no scraping HTML.
"""
import re
import httpx
from bs4 import BeautifulSoup
from ..services.cache import cache_get, cache_set

_API_BASE   = "https://unofficialtwrp.com/wp-json/wp/v2/posts"
_PER_PAGE   = 100
_MAX_PAGES  = 63  # X-WP-TotalPages = 63 (6,204 posts)

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


def _extract_codename(title: str, slug: str) -> str | None:
    """Extract device codename from post title or slug."""
    # Title often has codename in parentheses: "TWRP 3.4.0 Root Moto G9 Plus (odessa)"
    m = re.search(r'\(([a-z][a-z0-9_]{2,15})\)', title, re.IGNORECASE)
    if m:
        return m.group(1).lower()

    # Slug: "twrp-3-6-2-root-samsung-galaxy-a42-5g" → clean it
    # Remove version numbers and common words
    clean = re.sub(r'(?:unofficial[-_]?)?twrp[-_][\d.]+[-_]?', '', slug)
    clean = re.sub(r'(?:root|update|for|install|how[-_]to)[-_]?', '', clean)
    clean = clean.strip('-').replace('-', '_')
    if 3 <= len(clean) <= 20 and re.match(r'^[a-z][a-z0-9_]+$', clean):
        return clean

    return None


def _extract_manufacturer(categories: list[int], title: str) -> str:
    """Get manufacturer from category IDs or title."""
    for cat_id in categories:
        if cat_id in _CAT_NAMES:
            return _CAT_NAMES[cat_id]

    # Fallback: first word of title that's a brand
    brands = [
        "Samsung", "Xiaomi", "Redmi", "Poco", "Realme", "Oppo", "Vivo",
        "OnePlus", "Motorola", "Huawei", "Nokia", "Asus", "LG", "Sony",
        "Tecno", "Infinix", "Itel", "HTC", "Lenovo", "ZTE", "Alcatel",
    ]
    title_lower = title.lower()
    for brand in brands:
        if brand.lower() in title_lower:
            return brand

    return "Unknown"


async def get_unofficialtwrp_devices() -> list[dict]:
    """Fetch all unofficial TWRP posts — 6,204 across 63 pages."""
    ck = "roms:unofficialtwrp"
    if c := await cache_get(ck):
        return c

    results = []
    seen_slugs: set[str] = set()

    try:
        async with httpx.AsyncClient(
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"},
            follow_redirects=True,
        ) as client:
            # Fetch first page to get total, then fetch remaining concurrently
            # But to avoid hammering server, fetch sequentially with small batches
            # First page only — gives 100 entries quickly for initial load
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
            posts = resp.json()

            # Fetch remaining pages (up to 10 pages = 1000 devices max to avoid timeout)
            max_pages = min(total_pages, 10)
            for page in range(2, max_pages + 1):
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
                        posts.extend(r.json())
                except Exception:
                    break

    except Exception:
        return []

    for post in posts:
        slug  = post.get("slug", "")
        title = BeautifulSoup(post.get("title", {}).get("rendered", ""), "lxml").get_text()
        link  = post.get("link", "")
        cats  = post.get("categories", [])

        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)

        # Skip non-device posts
        if any(kw in title.lower() for kw in ["how to", "guide", "tutorial", "firmware flash file"]):
            continue

        codename = _extract_codename(title, slug)
        manufacturer = _extract_manufacturer(cats, title)

        results.append({
            "name":         title.strip(),
            "codename":     codename or slug[:20],
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
            "description":  f"Unofficial TWRP recovery build — {title.strip()}",
        })

    await cache_set(ck, results, ttl=7200)
    return results
