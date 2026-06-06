# Security

Droidify is a read-only web application. It fetches public data, renders HTML pages, and stores a small amount of data for people who choose to sign in. No payments. No file uploads. No private data beyond a GitHub username and a watchlist of up to 20 device codenames.

---

## What we want to hear about

- FastAPI route vulnerabilities — injection, path traversal, SSRF
- Auth or session issues — login bypass, accessing another user's watchlist without permission
- Data exposure — user data visible to someone who should not see it
- SSRF in scrapers — a scraper being manipulated into making requests to internal addresses
- Dependency CVEs that have a realistic exploit path on this specific stack

## What is out of scope

- Inaccurate data from upstream sources — wrong ROM info is a data issue, not a security vulnerability
- Content of download links hosted by third parties — we do not control what they host
- Social engineering scenarios
- Observations without a demonstrated impact

---

## How to report

Open a GitHub issue tagged `[security]`. If the details should not be public yet, describe the category and we will follow up privately. Tell us what the vulnerability is, how to reproduce it, and what an attacker could actually do with it. Do not disclose publicly before a fix is deployed. We will move as fast as we can.

No bug bounty. We will credit you in the commit if you want.

---

## What we store

**Never signed in:** nothing at all. No analytics. No cookies. No fingerprinting. No tracking of any kind.

**Signed in with GitHub:** your GitHub username, avatar URL, and numeric GitHub ID. Your watchlist of up to 20 device codenames. One signed session cookie that expires after 30 days.

We do not store passwords, email addresses, IP addresses, location data, or any record of what pages you visited or when.
