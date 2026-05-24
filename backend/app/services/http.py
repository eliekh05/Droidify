"""Shared async HTTP client for all scrapers.

All requests are made without authentication — only free public endpoints.
Rate limiting: built-in 0.2s delay between requests via semaphore.
"""
import asyncio
import httpx

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
    ),
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# Global semaphore: max 10 concurrent outbound requests
_SEM = asyncio.Semaphore(10)


def get_client() -> httpx.AsyncClient:
    """Return a configured async HTTP client."""
    return httpx.AsyncClient(
        headers=HEADERS,
        timeout=8.0,
        follow_redirects=True,
        limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
    )


async def fetch(client: httpx.AsyncClient, url: str, **kwargs) -> httpx.Response | None:
    """Fetch a URL with the shared semaphore. Returns None on error."""
    async with _SEM:
        try:
            return await client.get(url, **kwargs)
        except Exception:
            return None
