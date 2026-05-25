# Droidify — Android ROM & Device Index

Live Android ecosystem indexer. Devices, ROMs, recoveries, tools, and guides — fetched in real time from 20+ free public sources. Zero hardcoded data. No signin. No payment.

**Docker Hub**: [eliekh05/droidify](https://hub.docker.com/r/eliekh05/droidify)  
**GitHub**: [eliekh05/Droidify](https://github.com/eliekh05/Droidify)

---

## Quick Start

```bash
git clone https://github.com/eliekh05/Droidify
cd Droidify
./install.sh
```

Opens at **http://localhost**

---

## Architecture

```
nginx:alpine  (port 80)
├── /          → serves frontend/  (HTML, CSS, JS, PWA)
├── /api/*     → proxy → FastAPI (port 8000, internal)
└── /*         → try_files → /index.html

python:alpine  (port 8000, internal)
└── FastAPI — REST API, scrapers, cache
```

No build step for the frontend. Edit HTML/CSS/JS directly — refresh browser to see changes. No Node.js, no npm, no bundler.

---

## Development

```bash
# Backend with hot reload
make dev   # http://localhost:8000/api

# Frontend — just open frontend/ files in browser
# Point browser to http://localhost after starting backend
```

Edit `frontend/css/style.css`, `frontend/js/*.js`, or `frontend/*.html` directly. No build step needed.

---

## Stack

| Layer | Technology |
|---|---|
| Frontend | Plain HTML + CSS + Vanilla JS |
| Animations | IntersectionObserver + CSS transitions (GPU-accelerated) |
| PWA | Web App Manifest + Service Worker |
| Web server | nginx:alpine |
| Backend | FastAPI + Python 3.12 |
| Container | Docker multi-stage Alpine |

---

## API

| Endpoint | Description |
|---|---|
| `GET /api/devices` | Search devices |
| `GET /api/devices/{codename}` | Device detail with ROMs |
| `GET /api/roms` | ROM index |
| `GET /api/recoveries` | Recovery index |
| `GET /api/tools` | Root tools |
| `GET /api/android-versions` | Android history |
| `GET /api/guides/{codename}` | Flashing guides |
| `GET /api/health` | Health check |
| `GET /docs` | Swagger UI |

---

## Project Structure

```
Droidify/
├── frontend/               ← Static files (edit directly)
│   ├── css/style.css       ← All styles
│   ├── js/
│   │   ├── api.js          ← API client
│   │   ├── reveal.js       ← Scroll animations
│   │   ├── nav.js          ← Nav + PWA install
│   │   ├── home.js
│   │   ├── devices.js
│   │   ├── device.js
│   │   ├── roms.js
│   │   ├── recoveries.js
│   │   ├── tools.js
│   │   ├── android.js
│   │   └── guides.js
│   ├── bak/                ← Svelte source backups
│   ├── *.html              ← Pages
│   ├── manifest.json       ← PWA manifest
│   ├── sw.js               ← Service worker
│   └── icons/              ← PWA icons
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── scrapers/
│   │   └── services/
│   ├── requirements.txt
│   └── Dockerfile
│
├── nginx/
│   ├── nginx.conf
│   └── Dockerfile
│
├── docker-compose.yml
├── Makefile
└── install.sh
```

---

## License

MIT
