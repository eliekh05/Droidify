"""
bootstrap.py — runs before uvicorn.
Reads OWNER_SECRET from environment, writes app/private/owner.py.
This file is in the public repo. It contains no secrets.
OWNER_SECRET is set only in HF Spaces Secrets / GitHub repo secrets.
"""
import os
import sys
from pathlib import Path

secret = os.environ.get("OWNER_SECRET", "").strip()
private_dir  = Path(__file__).parent.parent / "app" / "private"
owner_path   = private_dir / "owner.py"
init_path    = private_dir / "__init__.py"

if not secret:
    if owner_path.exists():
        owner_path.unlink()
    print("[bootstrap] OWNER_SECRET not set — owner bypass not available", flush=True)
    sys.exit(0)

private_dir.mkdir(exist_ok=True)
init_path.write_text("")

# Write the private module with the secret baked in at runtime
# The file is never committed — only exists in the running container
owner_path.write_text(f"""
import hashlib
import hmac
import os
import time
from typing import Any

_SECRET = {repr(secret)}
_rl: dict[str, tuple[int, int]] = {{}}


def _key(w: int) -> str:
    raw = hmac.new(_SECRET.encode(), str(w).encode(), hashlib.sha256).digest()
    return raw.hex()[:8]


def register_owner_routes(app: Any) -> None:
    from fastapi import Request
    from fastapi.responses import JSONResponse

    @app.get("/api/internal/ck", include_in_schema=False)
    async def _ck(request: Request):
        if not _SECRET:
            return JSONResponse({{"detail": "Not Found"}}, status_code=404)
        w   = int(time.time()) // 60
        ttl = 60 - (int(time.time()) % 60)
        return JSONResponse({{"key": _key(w), "ttl": ttl}})

    @app.post("/api/internal/ac", include_in_schema=False)
    async def _ac(request: Request):
        if not _SECRET:
            return JSONResponse({{"detail": "Not Found"}}, status_code=404)
        fwd = request.headers.get("X-Forwarded-For", "")
        ip  = fwd.split(",")[0].strip() if fwd else (
              request.client.host if request.client else "unknown")
        w   = int(time.time()) // 60
        prev_w, attempts = _rl.get(ip, (w, 0))
        if prev_w != w:
            attempts = 0
        if attempts >= 3:
            return JSONResponse({{"detail": "Not Found"}}, status_code=404)
        _rl[ip] = (w, attempts + 1)
        try:
            body = await request.json()
            sub  = str(body.get("k", "")).strip().lower()
        except Exception:
            return JSONResponse({{"detail": "Not Found"}}, status_code=404)
        if sub not in {{_key(w), _key(w - 1)}}:
            return JSONResponse({{"detail": "Not Found"}}, status_code=404)
        _rl[ip] = (w, 0)
        return JSONResponse({{"ok": True}})
""")

print("[bootstrap] owner bypass ready", flush=True)
