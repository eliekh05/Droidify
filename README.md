# Droidify — Android ROM & Device Index

Live Android ecosystem indexer. Devices, ROMs, recoveries, tools, and guides — fetched in real time from 20+ free public sources. Zero hardcoded data. No signin. No payment.

📦 **Docker Hub**: [eliekh05/droidify](https://hub.docker.com/r/eliekh05/droidify)
🐙 **GitHub**: [eliekh05/Droidify](https://github.com/eliekh05/Droidify)

---

## Quick Start

```bash
# Docker (recommended)
docker run -d --name droidify --restart unless-stopped -p 8000:8000 eliekh05/droidify:latest

# or with docker compose
git clone https://github.com/eliekh05/Droidify
cd Droidify
./install.sh
```

Then open **http://localhost:8000**

---

## What it does

- Browse 1,100+ Android devices indexed from LineageOS, OrangeFox, and TWRP
- Find ROMs from 26+ sources including SourceForge, crDroid, Evolution X, GrapheneOS and more
- Search recoveries, root tools, and flashing guides by device codename
- All data fetched live — nothing is hardcoded or stored in a database

## API

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

## Architecture

Single FastAPI process. Serves the REST API at `/api/*` and the entire embedded frontend on the same port. No nginx, no database, no separate static server. All HTML, CSS, JS, and assets live as Python string literals — zero filesystem reads at runtime.

```
backend/app/
├── main.py                 # FastAPI app
├── api/                    # REST endpoints
├── scrapers/               # Live data fetchers
├── services/               # Cache + HTTP client
└── frontend/               # Embedded pages, assets, router
```

## Data Sources

| Source | What it provides |
|--------|-----------------|
| LineageOS API + Wiki | 281 active codenames |
| OrangeFox API | 159 recovery devices |
| TWRP | 896 recovery devices |
| SourceForge (26 projects) | ~1,600 ROM builds |
| GrapheneOS | 14 Pixel devices |
| DivestOS / CalyxOS / /e/OS | Privacy ROM lists |
| Ubuntu Touch | 110 devices |
| Kali NetHunter | 113 devices |
| postmarketOS | Alpine Linux mobile |
| GitHub API | Magisk, KernelSU, APatch |

## License

MIT
