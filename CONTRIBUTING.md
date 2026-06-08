# 🤝 Contributing

> **Open an issue before writing any code.** Tell us what you want to fix or add and why. Unsolicited pull requests are closed without review — not because we are being difficult, but because we need to understand a change before it lands.

---

## ✅ What is welcome

- 🐛 **Bug fixes** with a clear reproduction
- 🔍 **New scrapers** for sources you have personally confirmed are publicly accessible without authentication
- 📊 **Data corrections** with a source link that proves the correct value
- 📖 **Guide improvements** where a step is wrong, missing, or out of order

## ❌ What is not welcome

- 🎨 Style or formatting changes for their own sake
- 📦 Dependency bumps without a specific reason tied to a bug or CVE
- 🔒 Changes to `LICENSE`, `Dockerfile`, `docker-compose.yml`, or CI config without prior discussion
- 🔢 Hardcoded data when a live source exists and works

---

## 🔢 On hardcoded data

Everything should be live. If you are writing a scraper it must fetch from a real public endpoint — not a static list you typed out. If a live source genuinely does not exist or is too unreliable, say so in the issue before writing any code.

> **The only hardcoded data in the project** is the Android versions reference table. The live sources are slow, inconsistent, and don't reliably include all subversions. We seed from a reference table verified against official SDK documentation. This is intentional, documented, and _the only exception we make_.

---

## 📲 On the Android APK

The APK **does not need to be regenerated** for any code or data change. A new build is only needed when:

- The app icon changes
- The package name changes
- The signing key changes
- The splash screen changes

Everything else is live the moment the site deploys to HuggingFace. _Do not open issues asking for APK updates_ — it is already updated.

---

## ✏️ Commit style

Short subject line. Present tense. No period at the end.

```
Fix guides sort order
Add crDroid scraper for unofficial builds
```
_Not this:_ `Fixed the thing with the guides 🔧.`
