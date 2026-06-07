# Droidify

One place for Android modding. Search any device and see every custom ROM, recovery, root tool, and guide available for it — all pulled from 20+ public sources in real time. No account. No ads. No paywalls.

**Live site:** [eliekh05-droidify-hf.hf.space](https://eliekh05-droidify-hf.hf.space)

---

## Why this exists

Since Android 1.0 there has never been a single place to find what is available for your device. You had to check the LineageOS wiki, then TWRP, then OrangeFox, then XDA, then SourceForge, then crDroid — each one completely separate, none of them talking to each other. You had to already know what existed in order to find it, which is completely useless for anyone who is just getting started.

All of that data has been publicly accessible the whole time. LineageOS has had a JSON API for years. TWRP has had a search endpoint for years. OrangeFox has had structured CDN data for years. Nobody built the aggregator. So we did.

---

## The data

Everything you see on Droidify is fetched live from the original source. Nothing is made up, approximated, or served as current when it is actually old. If something fails to fetch you will see it clearly marked — it will never quietly pretend to be fresh data when it is not.

There is one exception. The Android versions page uses a hardcoded reference table instead of scraping a live source. The reason is explained below.

---

## The Android versions page

Most websites that cover Android versions only list the major releases — Android 10, 11, 12, 13, 14, 15. They skip the subversions that actually shipped on real hardware. Things like 2.3.1 through 2.3.7, 4.0 through 4.0.4, 4.1 through 4.1.2, 4.4 through 4.4.4, 5.0 through 5.0.2, and so on. Those versions existed. Devices shipped with them. People still have phones running them. They deserve to be listed.

The other problem is the naming. When someone sees a ROM targeting Android 14, a lot of people assume that means 14GB of storage. Others confuse it with the API level, which is 34. Android went from version 9 (Pie) straight to 10 and dropped the dessert naming scheme entirely, which trips up anyone who learned the old system. Android 12L appeared between 12 and 13 and most people have never even heard of it. The version number, the API level, the internal codename, and the release year are four completely different things and almost no site puts them all in one place clearly.

We built this page so anyone can look up what a version actually means — not just the number but the API level, the codename, when it was released, and its current support status.

The data is hardcoded because the live sources that publish Android version history — primarily Wikipedia and apilevels.com — do not reliably include all subversions, and their format changes without warning which breaks scrapers. A carefully maintained reference table is more accurate and more stable than a live scrape that might return an incomplete list or fail entirely. Every entry has been verified against the official Android SDK documentation and source.android.com build numbers. New versions are added as Google announces them.

---

## What it covers

- **946+ devices** — search by name, codename, or manufacturer
- **Custom ROMs** — LineageOS, GrapheneOS, crDroid, /e/OS, CalyxOS, DivestOS, postmarketOS, PixelExperience, and more
- **Recoveries** — TWRP, OrangeFox, PBRP, SHRP, unofficial builds
- **Root tools** — Magisk, KernelSU, APatch, LSPosed — versions fetched live from GitHub
- **Flashing tools** — Odin, ADB/Fastboot, SP Flash Tool, Mi Flash, QFIL — live versions
- **Guides** — Unlock bootloader → install recovery → flash ROM → root → restore → buy/sell. In that order, every time.
- **Android versions** — every version from 1.0 to the latest including all subversions, with API levels, codenames, and release dates
- **Watchlist + ROM alerts** — save devices, get notified when new builds drop
- **PWA** — install directly from the browser on any device

---

## Install

**Browser — the best option for everyone:**
Open the site in Chrome or Edge. An install button appears when the browser is ready. Tap it. Works on Android, Windows, macOS, and Linux. On iOS open in Safari → Share → Add to Home Screen. This is the smoothest install experience on every platform — no warnings, no friction, instant updates.

**Android APK:**
Download [Droidify.apk](https://github.com/eliekh05/Droidify/releases/download/v1.0.0/Droidify.apk) from Releases. Enable unknown sources, install, done. Full screen, no browser chrome. This is a TWA (Trusted Web Activity) — a thin native shell that opens the website directly. When the site updates, the app updates. No new APK needed for any content or feature change.

**Windows:**
Download [Droidify.msix](https://github.com/eliekh05/Droidify/releases/download/v1.0.0/Droidify.msix) from Releases and double click to install.

> ⚠️ Expect SmartScreen warnings on Windows. The package is not signed through the Microsoft Store, so Windows will complain about it. Click "More info" then "Run anyway" if it gets blocked. The app is safe and the source code is right above. That said — installing through Chrome or Edge using the browser install button is a significantly better experience on Windows with none of this friction, and Microsoft has no ability to interfere with that. Use the browser install if you can.

---

## Issues

This project should not have issues. If it does, open one and we will reach out. Nothing gets closed without an explanation. If something is broken we will fix it. If it cannot be fixed we will tell you exactly why.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python 3.12, fully async |
| Templates | Jinja2 server-side rendering |
| Frontend | 3 JS files, no framework, no build step |
| Deploy | Docker on HuggingFace Spaces |
| Database | SQLite via aiosqlite, persistent via HF Storage Bucket |
| Auth | GitHub OAuth2, optional |

---

## API

Public. No authentication required. All GET.

| Endpoint | Description |
|---|---|
| `GET /api/devices` | Search 946+ devices |
| `GET /api/devices/{codename}` | Device detail — ROMs, recoveries, firmware |
| `GET /api/roms` | ROM index |
| `GET /api/recoveries` | Recovery index |
| `GET /api/tools` | Root and flashing tools with live versions |
| `GET /api/android-versions` | Full Android version history including all subversions |
| `GET /api/guides` | Universal guides |
| `GET /api/guides/{codename}` | Device-specific guides |
| `GET /api/health` | Health check |

---

## Data sources

LineageOS API · LineageOS Wiki · OrangeFox CDN · TWRP search.json · Wikipedia · crDroid · SourceForge · GrapheneOS · postmarketOS · DivestOS · CalyxOS · /e/OS · Ubuntu Touch · NetHunter · customrombay.org · SamFW · GitHub Releases

Nothing is redistributed. Every download link goes directly to the original project's own servers.

---

## License

MIT. The code is yours. See [DMCA.md](DMCA.md) for data and takedown policy.
