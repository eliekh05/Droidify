# Security

Droidify is a read-only web application. It fetches public data from third-party sources, renders HTML, and stores a minimal amount of data for people who choose to sign in. No payments. No file uploads. No private data beyond a GitHub username and a watchlist.

-----

## What we want to hear about

- FastAPI route vulnerabilities — injection, path traversal, SSRF
- Authentication or session issues — login bypass, accessing another user’s watchlist without permission
- Data exposure — any user data visible to someone who should not see it
- SSRF in scrapers — a scraper being manipulated into fetching internal addresses
- Dependency CVEs with a realistic exploit path on this specific stack

## What is out of scope

- Inaccurate data from upstream sources — wrong ROM version or missing device is a data issue, not a security vulnerability
- Content or safety of download links hosted by third parties — we link to them, we do not control them
- Social engineering
- Generic observations with no demonstrated impact — “you should add rate limiting to X” without a proof of concept

-----

## How to report

Open a GitHub issue. If the details should not be public yet, describe the category without the full exploit and we will follow up privately. Tell us what the vulnerability is, how to reproduce it, and what an attacker could actually do with it.

Do not disclose publicly before a fix is deployed. We will move as fast as we can.

No bug bounty. If you want credit we will put your name in the commit.

-----

## What we store

**Never signed in** — nothing. No analytics. No cookies. No fingerprinting. No tracking. Not even a page view counter.

**Signed in with GitHub** — your GitHub username, avatar URL, and numeric GitHub ID. Your watchlist of up to 20 device codenames. One signed session cookie that expires after 30 days. The cookie is httponly, samesite, and signed server-side — it cannot be read by JavaScript, sent cross-site, or forged.

We do not store passwords, email addresses, IP addresses, location, or any record of what pages you visited or when.