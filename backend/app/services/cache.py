"""Simple in-memory TTL cache.

No Redis, no database — purely in-process.
Avoids hammering external free APIs on every request.
"""
import asyncio
import time
from typing import Any

_store: dict[str, tuple[Any, float]] = {}
_lock = asyncio.Lock()

DEFAULT_TTL = 300  # 5 minutes


async def get(key: str) -> Any | None:
    """Return cached value or None if expired/missing."""
    async with _lock:
        if key in _store:
            value, expires = _store[key]
            if time.monotonic() < expires:
                return value
            del _store[key]
    return None


async def set(key: str, value: Any, ttl: int = DEFAULT_TTL) -> None:
    """Store value with TTL seconds expiry."""
    async with _lock:
        _store[key] = (value, time.monotonic() + ttl)


async def cached(key: str, ttl: int = DEFAULT_TTL):
    """Decorator factory for async functions."""
    def decorator(fn):
        async def wrapper(*args, **kwargs):
            hit = await get(key)
            if hit is not None:
                return hit
            result = await fn(*args, **kwargs)
            await set(key, result, ttl)
            return result
        return wrapper
    return decorator


def cache_key(*parts) -> str:
    return ":".join(str(p) for p in parts)
