# Droidify

Live Android ecosystem indexer. Devices, ROMs, recoveries, tools, guides, and device buying/selling advice — fetched in real time from 20+ public sources. No hardcoded data. No login. No payment.

**Live demo:** [eliekh05-droidify-hf.hf.space](https://eliekh05-droidify-hf.hf.space)

## Quick start

```bash
git clone https://github.com/eliekh05/Droidify && cd Droidify && ./install.sh
```

Requires Docker. Runs at `http://localhost`.

## Commands

```
make dev     backend with hot reload
make up      start containers
make down    stop containers
make logs    stream all logs
make reset   full clean rebuild
```

## Stack

| Layer | |
|---|---|
| Frontend | HTML + Vanilla JS, no build step |
| Backend | FastAPI + Python 3.12, fully async |
| Web server | nginx Alpine — gzip, caching, SPA routing |
| Deploy | Docker Compose |

## API

All endpoints at `/api/`. Swagger UI at `/docs`.

| Endpoint | |
|---|---|
| `GET /api/devices` | Search by name, codename, manufacturer |
| `GET /api/devices/{codename}` | Device + ROMs + recoveries + firmware |
| `GET /api/roms` | Full ROM index |
| `GET /api/recoveries` | TWRP, OrangeFox, PBRP, SHRP |
| `GET /api/tools` | Root and flashing tools with live version data |
| `GET /api/android-versions` | Android version history |
| `GET /api/guides` | Root, flash, unlock, buy, sell guides |
| `GET /api/guides/{codename}` | Device-specific guides |
| `GET /api/health` | Health check |

## License

MIT
