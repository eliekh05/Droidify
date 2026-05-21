# Contributing

This is a personal project maintained by someone who actually flashes these ROMs,
runs these recoveries, and uses these tools on real devices. The scrapers and data
sources in this project come from direct experience — not just reading documentation.

If you want to contribute, that context matters.

---

## Before opening anything

Talk first. Open an issue or reach out directly before writing a single line of code.
If you show up with a PR nobody asked for, it will be closed.

Read the README. Read the scrapers in `backend/app/scrapers/`. Understand what is
already being indexed and why. A lot of what looks "missing" is either intentional
or already in progress.

---

## Who can contribute

Trusted collaborators added by the author. If you have not been explicitly added,
pull requests will be closed without review.

---

## What is welcome

- Bug fixes with a clear reproduction
- New scrapers for ROM/recovery sources you have personally verified and used
- Data corrections with a source link
- Frontend fixes for real usability issues

## What will be closed

- PRs from anyone not added as a collaborator
- Reformatting or style-only changes
- Dependency bumps without a stated reason
- Features that add complexity without clear benefit
- Anything touching `LICENSE`, `CONTRIBUTING.md`, `README.md`,
  `Dockerfile`, `docker-compose.yml`, or `publish.yml` without prior discussion

---

## For everyone else

```bash
docker run -p 7860:7860 eliekh05/droidify
```
