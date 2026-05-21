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

Single process — FastAPI serves both the REST API and frontend on one port. No nginx.

```
Droidify/
├── Dockerfile                   # Single-stage, Python 3.12-slim
├── docker-compose.yml
├── Makefile
├── install.sh
├── build.sh
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py              # FastAPI + StaticFiles mount
│       ├── api/                 # REST routers
│       │   ├── devices.py
│       │   ├── roms.py
│       │   ├── recoveries.py
│       │   ├── tools.py
│       │   ├── android_versions.py
│       │   └── guides.py
│       ├── scrapers/            # Live data fetchers
│       │   ├── devices.py       # LineageOS + OrangeFox + TWRP
│       │   ├── roms.py          # ROM index coordinator
│       │   ├── sourceforge_roms.py  # 26 SF projects, concurrent fetch
│       │   ├── unofficialtwrp.py    # WordPress API, 6,200 posts
│       │   ├── pixelexperience.py   # 148 devices via GitHub JSON
│       │   ├── recoveries.py
│       │   ├── guides.py
│       │   ├── tools.py
│       │   └── android_versions.py
│       └── services/
│           ├── cache.py         # In-memory TTL cache
│           └── http.py          # Shared async HTTP client
└── frontend/
    ├── index.html
    ├── devices.html
    ├── device.html
    ├── roms.html
    ├── recoveries.html
    ├── tools.html
    ├── android.html
    ├── guides.html
    ├── 404.html
    ├── css/style.css
    ├── js/
    │   ├── api.js               # API client + PWA install (all pages)
    │   ├── home.js
    │   ├── devices.js
    │   ├── device-detail.js
    │   ├── roms.js
    │   ├── recoveries.js
    │   ├── tools.js
    │   ├── android.js
    │   └── guides.js
    ├── icons/
    ├── manifest.json
    ├── sw.js
    ├── favicon.svg
    └── robots.txt
```

---

## Data Sources

| Source | Coverage |
|--------|----------|
| LineageOS API | 281 active devices |
| OrangeFox API | 159 recovery devices |
| TWRP | 896 recovery devices |
| SourceForge (26 ROM projects) | ~1,600 ROM entries, concurrent fetch |
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
| `GET /api/devices` | Search devices |
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
