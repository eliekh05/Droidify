---
title: Droidify
emoji: 💻
colorFrom: green
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: Live Android ROM & device indexer. No signin. No payment.
---

# Droidify — Android ROM & Device Index

Live Android ecosystem indexer. Browse 1,000+ ROMs, 1,100+ devices, recoveries, tools and guides — fetched in real time from 20+ sources. No signin. No payment. No hardcoded data.

🌐 **Live**: [eliekh05-droidify.hf.space](https://eliekh05-droidify.hf.space)

---

## Architecture

Single process — FastAPI serves both the REST API and the entire frontend on one port. No nginx. No separate static file directory — all HTML, CSS, JS and assets are embedded directly in Python modules inside `app/frontend/`.

```
Droidify/
├── Dockerfile                        # Single-stage, Python Alpine
├── docker-compose.yml
├── Makefile
├── install.sh
├── build.sh
└── backend/
    ├── requirements.txt
    └── app/
        ├── main.py                   # FastAPI app — mounts API + frontend routers
        ├── api/                      # REST routers (/api/*)
        │   ├── devices.py
        │   ├── roms.py
        │   ├── recoveries.py
        │   ├── tools.py
        │   ├── android_versions.py
        │   └── guides.py
        ├── scrapers/                 # Live data fetchers (no DB, no hardcoded data)
        │   ├── devices.py            # LineageOS + OrangeFox + TWRP merger
        │   ├── roms.py               # ROM index coordinator
        │   ├── sourceforge_roms.py   # 26 SF projects, concurrent fetch
        │   ├── unofficialtwrp.py     # WordPress API, 6,200 posts
        │   ├── pixelexperience.py    # 148 devices via GitHub JSON
        │   ├── recoveries.py
        │   ├── guides.py
        │   ├── tools.py
        │   └── android_versions.py
        ├── services/
        │   ├── cache.py              # In-memory TTL cache
        │   └── http.py               # Shared async HTTP client
        └── frontend/                 # Embedded frontend — no filesystem reads at runtime
            ├── __init__.py
            ├── assets.py             # CSS, JS, SVG, JSON, icons (base64) as Python strings
            ├── pages.py              # All 9 HTML pages as Python strings
            └── router.py             # FastAPI router — serves every asset with correct headers
```

---

## Data Sources

| Source | Coverage |
|--------|----------|
| LineageOS API | 281 active devices |
| OrangeFox API | 159 recovery devices |
| TWRP | 896 recovery devices |
| SourceForge (26 ROM projects) | ~1,600 ROM entries |
| unofficialtwrp.com | ~6,200 posts via WordPress API |
| Pixel Experience | 148 devices via GitHub JSON |
| GrapheneOS | 14 Pixel devices |
| DivestOS / CalyxOS / /e/OS | Privacy ROM device lists |
| Ubuntu Touch | 110 devices |
| Kali NetHunter | 113 devices |
| postmarketOS | Alpine Linux mobile OS |
| GitHub API | Magisk, KernelSU, APatch versions |

---

## Quick Start

```bash
git clone https://github.com/eliekh05/Droidify
cd Droidify
./install.sh          # → http://localhost:7860

# or dev mode (hot reload):
make dev
```

---

## API

| Endpoint | Description |
|----------|-------------|
| `GET /api/devices` | Search devices (supports model numbers like SM-J701F) |
| `GET /api/devices/{codename}` | Device detail + ROMs + recoveries |
| `GET /api/roms` | ROM index |
| `GET /api/recoveries` | Recovery index |
| `GET /api/tools` | Root tools |
| `GET /api/android-versions` | Android version history |
| `GET /api/guides/{codename}` | Flashing guides |
| `GET /api/health` | Health check |
| `GET /docs` | Swagger UI |

---

## License

MIT
