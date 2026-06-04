"""
app/api/not_read.py — Serves the punishment page from the backend.
Removed from frontend so it cannot be cached or bypassed via static file access.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex, nofollow" />
  <title>Hold on — Droidify</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.4/css/bulma.min.css" />
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <script>
    (function(){{
      const t = localStorage.getItem('droidify_theme');
      if (t && t !== 'system') document.documentElement.setAttribute('data-theme', t);
    }})();
  </script>
</head>
<body>
<main class="section" style="min-height:100vh;display:flex;align-items:center;justify-content:center">
  <div class="container" style="max-width:600px;text-align:center">
    <div style="font-size:3.5rem;margin-bottom:1.5rem">🛑</div>
    <h1 class="title is-3" style="color:var(--text);margin-bottom:1rem">
      You skipped the terms.
    </h1>
    <p style="color:var(--muted);font-size:1rem;line-height:1.75;margin-bottom:1.5rem">
      Droidify shows you where to find ROMs, recoveries, and root tools for your device.
      What happens when you flash one of them is entirely on you — not on us, not on the developer
      who uploaded the file, not on anyone else.
    </p>
    <p style="color:var(--muted);font-size:1rem;line-height:1.75;margin-bottom:1.5rem">
      Knox trips the moment you unlock the bootloader. It does not un-trip.
      Data wiped during a flash does not come back. A bricked device is a bricked device.
      The terms page covers all of this. It takes about a minute to read.
    </p>
    <p style="color:var(--muted);font-size:1rem;line-height:1.75;margin-bottom:2rem">
      GitHub issues about bricked devices, tripped Knox, or lost data are closed automatically
      with no reply. The terms page explains why. You navigated away before reading it.
    </p>
    <a href="/terms.html" class="button is-primary is-medium">
      ← Go back and read the terms
    </a>
  </div>
</main>
</body>
</html>"""


@router.get("/not-read", include_in_schema=False)
async def not_read(request: Request):
    return HTMLResponse(content=_PAGE, status_code=200)
