# Droidify

Live Android ecosystem indexer. Devices, ROMs, recoveries, tools, guides, and buying/selling advice — fetched in real time from 20+ public sources. No hardcoded data. No payment. Sign in with GitHub is optional — browse everything without an account.

**Use the hosted version:** [eliekh05-droidify-hf.hf.space](https://eliekh05-droidify-hf.hf.space)

## About

Droidify indexes custom ROMs, recoveries, root tools, and guides for 945+ Android devices. All data is fetched live from LineageOS, OrangeFox, TWRP, crDroid, /e/OS, GrapheneOS, postmarketOS, and 15+ other public sources.

## Stack

| | |
|---|---|
| Frontend | HTML + Vanilla JS — no build step |
| Backend | FastAPI + Python 3.12, fully async |
| Web server | nginx Alpine |
| Deploy | Docker Compose |

## API

All endpoints are GET-only. No auth required. Interactive docs at `/docs`.

| Endpoint | |
|---|---|
| `GET /api/devices` | Search 945+ devices by name, codename, manufacturer |
| `GET /api/devices/{codename}` | Device detail — ROMs, recoveries, firmware, guides |
| `GET /api/roms` | Full ROM index |
| `GET /api/recoveries` | TWRP, OrangeFox, PBRP, SHRP |
| `GET /api/tools` | Root and flashing tools with live version data |
| `GET /api/android-versions` | Android version history |
| `GET /api/guides` | Root, flash, unlock, buy, sell guides |
| `GET /api/guides/{codename}` | Device-specific guides |
| `GET /api/health` | Health check |

## License

MIT — the code is open. The hosted service is operated separately.
