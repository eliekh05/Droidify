# 🤖 Droidify

> **One place for Android modding.** Search any device and see every custom ROM, recovery, root tool, and guide available for it — pulled live from 20+ public sources. No account needed. No ads. No paywalls.

**🌐 Live site:** [eliekh05-droidify-hf.hf.space](https://eliekh05-droidify-hf.hf.space)

---

## 💡 Why this exists

Since Android 1.0 there has **never** been a single place to find what is available for your device. You had to check the LineageOS wiki, then TWRP, then OrangeFox, then XDA, then SourceForge, then crDroid — each one completely separate, none of them connected. You had to *already know what existed* in order to find it, which is completely useless for anyone just starting out.

All of that data has been publicly accessible the whole time. LineageOS has had a JSON API for years. TWRP has had a search endpoint for years. OrangeFox has had structured CDN data for years. **Nobody built the aggregator. So we did.**

---

## 📊 The data

Everything you see on Droidify is fetched live from the original source. Nothing is made up, approximated, or served as current when it is actually old. If something fails to fetch you will see it clearly marked — it will never quietly pretend to be fresh data when it is not.

> ⚠️ **One exception:** The Android versions page uses a hardcoded reference table — explained below.

---

## 🤖 The Android versions page

Most websites that cover Android versions only list the major releases. They skip the subversions that actually shipped on real hardware — things like _2.3.1 through 2.3.7_, _4.0 through 4.0.4_, _4.4 through 4.4.4_, and so on. Those versions existed. Devices shipped with them.

The naming makes it worse. When someone sees a ROM targeting **Android 14**, many people think that means 14GB of storage. Others confuse it with the API level, which is actually **34**. Android went from version 9 (Pie) straight to 10 and dropped the dessert naming entirely. **Android 12L** appeared between 12 and 13 and most people have never heard of it.

Version number, API level, internal codename, and release year are *four completely different things* and almost no site puts them all together clearly. We do.

The data is **hardcoded** because the live sources — Wikipedia and apilevels.com — are inconsistent, don't reliably include all subversions, and change format without warning. A carefully maintained reference table is more accurate and more stable. Every entry is verified against official Android SDK documentation and [source.android.com](https://source.android.com) build numbers. New versions are added when Google announces them.

---

## ✅ What it covers

| Category | Details |
|---|---|
| 📱 **Devices** | 946+ — search by name, codename, or manufacturer |
| 💿 **Custom ROMs** | LineageOS, GrapheneOS, crDroid, /e/OS, CalyxOS, DivestOS, postmarketOS, PixelExperience, and more |
| 🔧 **Recoveries** | TWRP, OrangeFox, PBRP, SHRP, unofficial builds |
| ⚡ **Root tools** | Magisk, KernelSU, APatch, LSPosed — live versions from GitHub |
| 🛠️ **Flashing tools** | Odin, ADB/Fastboot, SP Flash Tool, Mi Flash, QFIL — live versions |
| 📖 **Guides** | Unlock bootloader → recovery → ROM → root → restore → buy/sell |
| 🤖 **Android versions** | Every version from 1.0 to latest including all subversions |
| 📋 **Watchlist + alerts** | Save devices, get notified when new builds drop |
| 📲 **PWA** | Install directly from the browser on any device |

---

## 📲 Install

### 🌐 Browser — *recommended for everyone*
Open the site in Chrome or Edge. An install button appears automatically. Works on **Android, Windows, macOS, and Linux**. On iOS: Safari → Share → _Add to Home Screen_.

This is the best option on every platform — no warnings, no friction, instant updates.

### 🤖 Android APK
Download [**Droidify.apk**](https://github.com/eliekh05/Droidify/releases/download/v1.0.0/Droidify.apk) from Releases. Enable unknown sources, install, done. Full screen, no browser chrome.

This is a **TWA (Trusted Web Activity)** — a thin native shell that opens the website directly. When the site updates, the app updates automatically. _No new APK needed_ for any content or feature change.

### 🪟 Windows
Download [**Droidify.msix**](https://github.com/eliekh05/Droidify/releases/download/v1.0.0/Droidify.msix) from Releases and double click to install.

> ⚠️ **Expect SmartScreen warnings.** The package is not signed through the Microsoft Store so Windows will complain about it. Click _"More info"_ → _"Run anyway"_. The app is safe and the source code is right above. If you want none of this friction, use the browser install — Microsoft cannot interfere with that and it works better anyway.

---

## 🚫 Issues

This project should not have issues. If it does, open one and we will reach out. Nothing gets closed without an explanation. If something is broken we will fix it. If it cannot be fixed we will tell you exactly why.

---

## 🏗️ Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python 3.12, fully async |
| Templates | Jinja2 server-side rendering |
| Frontend | 3 JS files, no framework, no build step |
| Deploy | Docker on HuggingFace Spaces |
| Database | SQLite via aiosqlite, persistent via HF Storage Bucket |
| Auth | GitHub OAuth2, optional |

---

## 🔌 API

_Public. No authentication required. All GET._

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

## 🌐 Data sources

_LineageOS API · LineageOS Wiki · OrangeFox CDN · TWRP search.json · Wikipedia · crDroid · SourceForge · GrapheneOS · postmarketOS · DivestOS · CalyxOS · /e/OS · Ubuntu Touch · NetHunter · customrombay.org · SamFW · GitHub Releases_

> Nothing is redistributed. Every download link goes directly to the original project's own servers.

---

## 📄 License

MIT. The code is yours. See [DMCA.md](DMCA.md) for data and takedown policy.
