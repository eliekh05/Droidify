# 🔐 Security

Droidify is a **read-only** web application. It fetches public data from third-party sources, renders HTML pages, and stores a minimal amount of data for people who choose to sign in. No payments. No file uploads. No private data beyond a GitHub username and a watchlist.

---

## 🎯 What we want to hear about

- **FastAPI route vulnerabilities** — injection, path traversal, SSRF
- **Auth or session issues** — login bypass, accessing another user's watchlist
- **Data exposure** — any user data visible to someone who should not see it
- **SSRF in scrapers** — a scraper being manipulated into fetching internal addresses
- **Dependency CVEs** with a realistic exploit path on this specific stack

## 🚫 What is out of scope

- _Inaccurate data from upstream sources_ — wrong ROM version is a data issue, not a security vulnerability
- _Content of download links hosted by third parties_ — we link to them, we do not control them
- _Social engineering_ scenarios
- _Generic observations_ with no demonstrated impact

---

## 📬 How to report

Open a GitHub issue. If the details should not be public yet, describe the category without the full exploit and we will follow up privately.

Tell us:
1. **What** the vulnerability is
2. **How** to reproduce it
3. **What** an attacker could actually do with it

> _Do not disclose publicly before a fix is deployed._ We will move as fast as we can.

No bug bounty. **We will credit you in the commit** if you want.

---

## 🗄️ What we store

**Never signed in** — _nothing_. No analytics. No cookies. No fingerprinting. No tracking. Not even a page view counter.

**Signed in with GitHub:**
- Your GitHub **username**, **avatar URL**, and **numeric ID**
- Your **watchlist** — up to 20 device codenames
- One **signed session cookie** expiring after 30 days

The session cookie is `httponly` _(JavaScript cannot read it)_, `samesite=lax` _(cannot be sent cross-site)_, and signed server-side _(cannot be forged)_.

> We do not store passwords, email addresses, IP addresses, location data, or any record of what pages you visited or when.
