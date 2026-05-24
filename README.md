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

Then open **http://localhost:8000**

Or pull directly from Docker Hub:

```bash
docker run -d --name droidify --restart unless-stopped -p 8000:8000 eliekh05/droidify:latest
```

---

## Development

**Requirements:** Docker, Node.js 22+, Python 3.12+

```bash
# Install frontend dependencies
cd frontend && npm install && cd ..

# Run backend with hot reload
make dev-backend   # http://localhost:8000

# Run frontend with hot module replacement (separate terminal)
make dev-frontend  # http://localhost:5173
```

The Vite dev server proxies `/api/*` to the backend automatically.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python 3.12 |
| Frontend | Svelte + Vite |
| Container | Docker (multi-stage Alpine, ~40MB) |
| Tunnel | Cloudflare Tunnel |

---

## API

| Endpoint | Description |
|---|---|
| `GET /api/devices` | Search devices by name, codename, or manufacturer |
| `GET /api/devices/{codename}` | Device detail with ROMs and recoveries |
| `GET /api/roms` | ROM index with filtering |
| `GET /api/recoveries` | Recovery index |
| `GET /api/tools` | Root tools (Magisk, KernelSU, APatch) |
| `GET /api/android-versions` | Android version history |
| `GET /api/guides` | Flashing and rooting guides |
| `GET /api/health` | Health check |
| `GET /docs` | Interactive Swagger UI |

---

## Data Sources

| Source | What it provides |
|---|---|
| LineageOS API + Wiki | 281 active codenames |
| OrangeFox API | 159 recovery devices |
| TWRP | 896 recovery devices |
| SourceForge (26 projects) | ~1,600 ROM builds |
| GrapheneOS | 14 Pixel devices |
| DivestOS / CalyxOS / /e/OS | Privacy ROM lists |
| crDroid, Evolution X, HavocOS | Community ROMs |
| Ubuntu Touch | 110 devices |
| Kali NetHunter | 113 devices |
| GitHub API | Magisk, KernelSU, APatch |

---

## Project Structure

```
Droidify/
├── frontend/               ← Svelte + Vite source
│   ├── src/
│   │   ├── app.css         ← Global styles
│   │   ├── App.svelte      ← Root component + router
│   │   ├── lib/
│   │   │   ├── api.js      ← API client
│   │   │   └── router.js   ← SPA router
│   │   ├── components/     ← Nav, DeviceCard, Pagination
│   │   └── routes/         ← Home, Devices, Roms, etc.
│   └── public/             ← Icons, manifest, sw.js
│
├── backend/
│   └── app/
│       ├── main.py         ← FastAPI app + SPA serving
│       ├── api/            ← REST endpoints
│       ├── scrapers/       ← Live data fetchers
│       └── services/       ← Cache + HTTP client
│
├── Dockerfile              ← Multi-stage: Node → Python → Alpine
├── docker-compose.yml
└── Makefile
```

---

## License

MIT
