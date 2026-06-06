# Contributing

Open an issue before writing any code. Tell us what you want to fix or add and why. Unsolicited pull requests are closed without review — not because we are being difficult, but because we need to understand a change before it lands in the codebase.

---

## What is welcome

- Bug fixes with a clear reproduction
- New scrapers for sources you have personally confirmed are publicly accessible without authentication
- Data corrections with a source link that proves the correct value
- Guide improvements where a step is wrong, missing, or out of order

## What is not welcome

- Style or formatting changes for their own sake
- Dependency bumps without a specific reason tied to a bug or CVE
- Changes to `LICENSE`, `Dockerfile`, `docker-compose.yml`, or CI config without prior discussion
- Hardcoded data when a live source exists and works

---

## On hardcoded data

Everything should be live. If you are writing a scraper it must fetch from a real public endpoint — not a static list you typed out yourself. If a live source genuinely does not exist or is unreliable enough to degrade the user experience, say so in the issue before writing any code and we will discuss the right approach.

The only hardcoded data in the project right now is the Android versions reference table. The live sources for Android version history are slow, inconsistent, and occasionally return incomplete data. We seed from a reference table and merge any live updates on top. Every version from Android 1.0 to the latest is accounted for. New releases are added when they are announced. This is documented, intentional, and the only exception we make.

---

## Commit style

Short subject line. Present tense. No emoji. No period at the end.

Good: `Fix guides sort order`
Good: `Add crDroid scraper for unofficial builds`
Not this: `Fixed the thing with the guides 🔧.`
