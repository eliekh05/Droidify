"""In-memory TTL cache with optional disk persistence."""
import asyncio
import json
import logging
import os
import time
from pathlib import Path
from typing import Any

_log   = logging.getLogger("droidify.cache")
_store: dict[str, tuple[Any, float]] = {}
_lock  = asyncio.Lock()

DEFAULT_TTL  = 300    # 5 minutes
_data_dir = Path("/data") if Path("/data").exists() else Path("/tmp")
PERSIST_PATH = Path(os.environ.get("CACHE_PERSIST_PATH", str(_data_dir / "droidify_cache.json")))

async def get(key: str) -> Any | None:
    async with _lock:
        if key in _store:
            value, expires = _store[key]
            if time.monotonic() < expires:
                return value
            del _store[key]
    return None

async def set(key: str, value: Any, ttl: int = DEFAULT_TTL) -> None:
    async with _lock:
        _store[key] = (value, time.monotonic() + ttl)

async def delete(key: str) -> None:
    async with _lock:
        _store.pop(key, None)

async def clear() -> None:
    async with _lock:
        _store.clear()

def cache_key(*parts) -> str:
    return ":".join(str(p) for p in parts)

def save_to_disk() -> None:
    """Serialize non-expired cache entries to disk."""
    now = time.monotonic()
    try:
        serializable = {}
        for key, (value, expires) in list(_store.items()):
            if expires > now:
                remaining = expires - now
                try:
                    json.dumps(value)   # only persist JSON-serializable entries
                    serializable[key] = {"value": value, "ttl": remaining}
                except (TypeError, ValueError):
                    pass

        PERSIST_PATH.write_text(json.dumps(serializable))
        _log.info("Cache saved: %d entries → %s", len(serializable), PERSIST_PATH)
    except Exception as e:
        _log.warning("Cache save failed: %s", e)

def load_from_disk() -> int:
    """Restore cache from disk. Returns number of entries restored."""
    if not PERSIST_PATH.exists():
        return 0
    try:
        data = json.loads(PERSIST_PATH.read_text())
        now  = time.monotonic()
        count = 0
        for key, entry in data.items():
            ttl   = entry.get("ttl", DEFAULT_TTL)
            value = entry.get("value")
            if ttl > 0 and value is not None:
                _store[key] = (value, now + ttl)
                count += 1
        _log.info("Cache restored: %d entries from %s", count, PERSIST_PATH)
        return count
    except Exception as e:
        _log.warning("Cache load failed: %s", e)
        return 0

def cached(key: str, ttl: int = DEFAULT_TTL):
    """Decorator for async functions."""
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
