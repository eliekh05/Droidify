# Droidify

One place for Android modding. Search any device and see every custom ROM, recovery, root tool, and guide available for it — pulled live from 20+ public sources. No account needed. No ads. No paywalls.

**Live site:** [eliekh05-droidify-hf.hf.space](https://eliekh05-droidify-hf.hf.space)

---

## Why this exists

Since Android 1.0 there has never been a single place to find what is available for your device. You had to check the LineageOS wiki, then TWRP, then OrangeFox, then XDA, then SourceForge, then crDroid — each one separate, none connected. You had to already know what existed to find it. That is useless for anyone just starting out.

All of that data has been publicly available the entire time. LineageOS has had a JSON API for years. TWRP has had a search endpoint for years. OrangeFox has had structured CDN data for years. Nobody built the aggregator. So we did.

---

## Our promise on data

Everything shown on Droidify is fetched live from the original source. We do not invent data, approximate it, or silently serve old cached values as if they were current. If a live fetch fails you will see it marked as unavailable or cached — never presented as fresh when it is not.

We hardcode data in exactly one situation: when the live source goes down too often, responds too slowly to be usable, or does not exist at all. When that happens it is documented and visible. It is never the easy way out.

The one current example is the Android versions page — explained below.

---

## Why there is an Android versions page

Most people do not know what Android version their device runs or what version a ROM targets. The problem is made worse by how Android is named and numbered.

When someone sees Android 14, a lot of people think that is storage — like 14GB. Others think it is the API level, which is actually 34. Others think Android 15 came after Android 9 because the numbers skipped — Android went from 9 (Pie) to 10, dropping dessert names entirely. Android 12L was a surprise release between 12 and 13 that most people have never heard of. Android versions, API levels, codenames, and release years are four completely separate things that almost no website explains together in one place.

We built the Android versions page so that when someone sees a ROM listed as targeting Android 14, they can immediately look up what that means — the API level, the codename, when it was released, and whether their device can run it. Without that page, users are left Googling "is Android 14 good for my device" and getting results that are either wrong, outdated, or about phone storage.

The data on this page is seeded from a reference table and updated when new versions are released. We do this because the live sources that publish Android version history are inconsistent and sometimes slow enough to make the page time out. A complete reliable table is more useful than a live scrape that occasionally returns half the list. This is intentional, documented, and the right tradeoff.

---

## What it does

- **945+ devices** — search by name, codename, or manufacturer
- **Custom ROMs** — LineageOS, GrapheneOS, crDroid, /e/OS, CalyxOS, DivestOS, postmarketOS, PixelExperience, and more
- **Recoveries** — TWRP, OrangeFox, PBRP, SHRP, unofficial builds
- **Root tools** — Magisk, KernelSU, APatch, LSPosed — versions fetched live from GitHub
- **Flashing tools** — Odin, ADB/Fastboot, SP Flash Tool, Mi Flash, QFIL — live versions, nothing hardcoded
- **Guides** — Unlock bootloader → install recovery → flash ROM → root → restore → buy/sell. In that order, every time.
- **Android versions** — every version from 1.0 to the latest, with API levels, codenames, and release dates in one place
- **Watchlist + ROM alerts** — save devices, get notified when new builds drop
- **PWA** — installable on any device directly from the browser, works offline from cache
- **Android APK** — installable as a native Android app via PWABuilder TWA. No Play Store needed for sideload.

---

## Install

**Browser — any device:**
Open [eliekh05-droidify-hf.hf.space](https://eliekh05-droidify-hf.hf.space) in Chrome or Edge. An install button appears in the address bar or at the top of the page when the browser decides the app is ready to install. Tap it. Done. Works on Android, Windows, macOS, and Linux. On iOS use Safari → Share → Add to Home Screen.

**Android APK — sideload:**
A native Android APK is available built using TWA (Trusted Web Activity). Same site, full screen, no browser address bar, works offline from cache. No Play Store account needed to sideload.

1. Download the APK from the [Releases page](https://github.com/eliekh05/Droidify/releases)
2. On your Android device: Settings → Security → Install unknown apps → allow your browser or file manager
3. Open the APK file and install
4. Droidify appears on your home screen like any other app

**What is a TWA and why does it matter?**

A Trusted Web Activity (TWA) is a thin native Android shell that opens your website full screen — no browser address bar, no browser chrome, just the app. The APK itself contains almost no code. It is a verified pointer to the website.

This means:
- When the site is updated on HuggingFace, every user who opens the app gets the update immediately — no new APK, no Play Store release, no user action required
- It works exactly like pushing a Docker image to a registry — the container (APK) stays the same, the content inside (the website) is always the latest version
- The APK only needs to be regenerated if the package name, signing key, or app metadata changes — not for any content, data, or feature update
- Storage, battery, and memory usage is minimal because the app delegates everything to Chrome

The only thing that requires a new APK release is a change to the native shell itself — for example, updating the app icon, changing the package name, or modifying the splash screen.

## Issues

This project should never have issues. If it does, open one and we will reach out. We do not close issues without explaining why. We do not ignore reports. If something is broken we will fix it. If it cannot be fixed we will tell you exactly why.

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
| `GET /api/devices` | Search 945+ devices |
| `GET /api/devices/{codename}` | Device detail — ROMs, recoveries, firmware |
| `GET /api/roms` | ROM index |
| `GET /api/recoveries` | Recovery index |
| `GET /api/tools` | Root and flashing tools with live versions |
| `GET /api/android-versions` | Android version history with API levels and codenames |
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
