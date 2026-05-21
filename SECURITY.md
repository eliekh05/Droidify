# Security

## Scope

Droidify is a read-only indexer. It fetches public data from upstream sources and serves it. It has no user accounts, no authentication, no file uploads, and no database.

**In scope:** vulnerabilities in the FastAPI application, SSRF via scraper URLs, dependency issues.

**Out of scope:** data accuracy of upstream sources, content of external download links, issues with third-party APIs Droidify indexes.

## Reporting

Open a GitHub issue marked **[security]** or email the address on the GitHub profile. Please do not disclose publicly before a fix is in place.
