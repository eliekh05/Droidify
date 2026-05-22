# Droidify — Android ROM & Device Index

Live Android ecosystem indexer. Devices, ROMs, recoveries, tools, and guides — fetched in real time from 20+ free public sources. Zero hardcoded data. No signin. No payment.

🌐 **Live**:
📦 **GitHub**: [eliekh05/Droidify](https://github.com/eliekh05/Droidify)

---

## What it does

- Browse 1,100+ Android devices indexed from LineageOS, OrangeFox, and TWRP
- Find ROMs from 26+ sources including SourceForge, Pixel Experience, crDroid, and more
- Search recoveries, root tools, and flashing guides by device codename
- All data fetched live — nothing is hardcoded or stored in a database

## Architecture

Single FastAPI process. Serves the REST API at `/api/*` and the entire frontend on the same port. No nginx, no separate static file server. All HTML, CSS, JS, and assets are embedded as Python string literals inside `app/frontend/` — zero filesystem reads at runtime.

```
Droidify/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── install.sh
├── build.sh
└── backend/
    ├── requirements.txt
    └── app/
        ├── main.py                   # FastAPI app — mounts API + frontend routers
        ├── api/                      # REST endpoints (/api/*)
        │   ├── devices.py
        │   ├── roms.py
        │   ├── recoveries.py
        │   ├── tools.py
        │   ├── android_versions.py
        │   └── guides.py
        ├── scrapers/                 # Live data fetchers — no DB, no hardcoded lists
        │   ├── devices.py            # LineageOS + OrangeFox + TWRP merger
        │   ├── roms.py               # ROM coordinator (all sources)
        │   ├── sourceforge_roms.py   # 26 SourceForge ROM projects
        │   ├── unofficialtwrp.py     # ~6,200 posts via WordPress API
        │   ├── pixelexperience.py    # 148 devices via GitHub JSON
        │   ├── recoveries.py
        │   ├── guides.py
        │   ├── tools.py
        │   └── android_versions.py
        ├── services/
        │   ├── cache.py              # In-memory TTL cache
        │   └── http.py               # Shared async HTTP client
        └── frontend/                 # Embedded — no /frontend folder on disk
            ├── assets.py             # CSS, JS, SVG, JSON, icons (base64) as Python strings
            ├── pages.py              # All HTML pages as Python strings
            └── router.py             # FastAPI router serving every asset
```

## Data Sources

| Source | What it provides |
|--------|-----------------|
| LineageOS API + Wiki | 281 active codenames, model names |
| OrangeFox API | 159 recovery devices |
| TWRP | 896 recovery devices |
| SourceForge (26 projects) | ~1,600 ROM build entries |
| unofficialtwrp.com | ~6,200 posts via WordPress API |
| Pixel Experience | 148 devices via GitHub JSON |
| GrapheneOS | 14 Pixel devices |
| DivestOS / CalyxOS / /e/OS | Privacy ROM device lists |
| Ubuntu Touch | 110 devices |
| Kali NetHunter | 113 devices |
| postmarketOS | Alpine Linux mobile targets |
| GitHub API | Magisk, KernelSU, APatch releases |

## Quick Start

```bash
git clone https://github.com/eliekh05/Droidify
cd Droidify
./install.sh          # builds and runs at http://localhost:7860

# or dev mode with hot reload:
make dev
```

## API Reference

| Endpoint | Description |
|----------|-------------|
| `GET /api/devices` | Search devices by name, codename, or manufacturer |
| `GET /api/devices/{codename}` | Device detail with ROMs and recoveries |
| `GET /api/roms` | ROM index with filtering |
| `GET /api/recoveries` | Recovery index |
| `GET /api/tools` | Root tools (Magisk, KernelSU, APatch) |
| `GET /api/android-versions` | Android version history |
| `GET /api/guides/{codename}` | Flashing and rooting guides |
| `GET /api/health` | Health check |
| `GET /docs` | Interactive Swagger UI |

## License

MIT
