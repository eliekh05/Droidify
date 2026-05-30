# Droidify — Android ROM & Device Index

Live Android ecosystem indexer. Devices, ROMs, recoveries, tools, and guides — fetched in real time from 20+ free public sources. Zero hardcoded data. No signin. No payment.

**GitHub**: [eliekh05/Droidify](https://github.com/eliekh05/Droidify)

---

## Quick Start

```bash
git clone https://github.com/eliekh05/Droidify
cd Droidify
./install.sh
```

---

## Architecture

```
nginx:alpine  (port 80, public)
├── /*         → serves frontend/ (HTML, CSS, JS, PWA)
├── /api/*     → proxy → FastAPI backend (port 8000, internal)
└── /docs      → proxy → FastAPI Swagger UI

python:alpine  (port 8000, internal only)
└── FastAPI — REST API, scrapers, in-memory cache
```

No build step for the frontend. Edit `frontend/` files directly — refresh browser to see changes. No Node.js, no npm, no bundler required.

---

## Development

```bash
# Backend with hot reload (terminal 1)
make dev

# Frontend — edit files directly in frontend/, nginx serves them
# For local dev without Docker, open frontend/ in browser with a static server
```

---

## Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | Plain HTML + CSS + Vanilla JS | No build step, edit directly, works everywhere |
| Animations | IntersectionObserver + CSS transitions | GPU-accelerated, 97%+ browser support |
| PWA | Web App Manifest + Service Worker | Offline support, installable |
| Web server | nginx 1.27 Alpine | Fastest static file serving, gzip, security headers |
| Backend | FastAPI + Python 3.12 | Async HTTP, easy scraper expansion |
| HTTP client | httpx (async) | Connection pooling, concurrent scraping |
| Container | Docker multi-stage Alpine | ~50MB final image, no build tools in production |

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/devices` | Search 1,100+ devices by name, codename, manufacturer |
| `GET /api/devices/{codename}` | Device detail with ROMs, recoveries, stock firmware |
| `GET /api/roms` | ROM index (2,600+ builds) |
| `GET /api/recoveries` | Recovery index — TWRP, OrangeFox, PBRP, SHRP |
| `GET /api/tools` | Root tools — Magisk, KernelSU, APatch |
| `GET /api/android-versions` | Complete Android version history |
| `GET /api/guides/{codename}` | Flashing and rooting guides |
| `GET /api/health` | Health check |
| `GET /docs` | Interactive Swagger UI |

---

## Data Sources

| Source | Data | Devices |
|---|---|---|
| LineageOS API | Active ROM builds + branches | 281 |
| LineageOS Wiki | Device specs + model names | 583 |
| OrangeFox API | Recovery devices | ~160 |
| TWRP | Recovery devices | ~900 |
| PBRP (GitHub) | PitchBlack Recovery | ~80 |
| SHRP (GitHub) | SkyHawk Recovery | ~60 |
| SourceForge (26 projects) | ROM builds | ~1,600 |
| GrapheneOS | Privacy ROM | 14 |
| PixelExperience | Community ROM | ~200 |
| crDroid | Community ROM | ~200 |
| DivestOS | Privacy ROM | ~170 |
| CalyxOS | Privacy ROM | ~30 |
| /e/OS | Privacy ROM | ~100 |
| Evolution X | Community ROM | ~200 |
| Ubuntu Touch | Alternative OS | ~110 |
| Kali NetHunter | Security OS | ~113 |
| postmarketOS | Linux-based OS | ~500 |
| SamFW | Samsung stock firmware links | 50 codenames |
| GitHub API | Magisk, KernelSU, APatch releases | — |

---

## Project Structure

```
Droidify/
├── frontend/               ← Static files — edit directly
│   ├── css/style.css       ← All styles, animations
│   ├── js/
│   │   ├── api.js          ← API client with AbortController timeout
│   │   ├── reveal.js       ← Scroll animations (IntersectionObserver)
│   │   ├── nav.js          ← Nav, PWA install, connection overlay
│   │   ├── home.js
│   │   ├── devices.js
│   │   ├── device.js       ← Device detail with auto-retry
│   │   ├── roms.js
│   │   ├── recoveries.js
│   │   ├── tools.js
│   │   ├── android.js
│   │   └── guides.js
│   ├── *.html              ← Pages
│   ├── manifest.json       ← PWA manifest
│   ├── sw.js               ← Service worker (offline support)
│   └── icons/              ← PWA icons
│
├── backend/
│   └── app/
│       ├── main.py         ← FastAPI app, startup warmup
│       ├── api/            ← REST endpoints
│       ├── scrapers/       ← Live data fetchers (20+ sources)
│       └── services/       ← Cache + HTTP client
│
├── nginx/
│   ├── nginx.conf          ← gzip, security headers, proxy /api/*
│   └── Dockerfile
│
├── backend/Dockerfile      ← Multi-stage Alpine build
├── docker-compose.yml
├── Makefile
└── install.sh
```

---

## Commands

```bash
make reset         # Full clean rebuild
make build         # Build images
make up            # Start containers
make down          # Stop containers
make logs          # View all logs
make logs-backend  # Backend logs only
make logs-nginx    # nginx logs only
make dev           # Backend hot reload for development
```

---

## License

MIT — see [LICENSE](LICENSE)
