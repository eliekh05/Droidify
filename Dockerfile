FROM python:alpine

# HF Spaces requires UID 1000; Alpine uses adduser not useradd
RUN adduser -D -u 1000 -g "" user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PORT=7860 \
    CORS_ORIGINS="*" \
    SCRAPER_USER_AGENT="DroidifyBot/2.0" \
    SCRAPER_CONCURRENCY="10" \
    SCRAPER_TIMEOUT="20" \
    CACHE_DEFAULT_TTL="300"

WORKDIR /home/user/app

# Build deps needed by lxml on Alpine (cached — rarely changes)
RUN apk add gcc musl-dev libxml2-dev libxslt-dev

RUN pip install --upgrade pip wheel

# ── Cache bust point ─────────────────────────────────────────────────────────
# BUILDTIME is injected by publish.yml as a Unix timestamp on every push.
# Changing it invalidates this layer and everything below — forcing a fresh
# pip install and code copy on every deployment, with no stale HF cache.
ARG BUILDTIME=0
RUN echo "Build timestamp: ${BUILDTIME}"

COPY --chown=user:user backend/requirements.txt .
RUN pip install -r requirements.txt

RUN apk del gcc musl-dev

# Only copy the backend — frontend is embedded in app/frontend/
COPY --chown=user:user backend/app ./app

USER user

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 \
    CMD ["sh", "-c", "python3 -c \"import urllib.request,sys,os; urllib.request.urlopen('http://localhost:' + os.environ.get('PORT','$PORT') + '/api/health',timeout=8); sys.exit(0)\""]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT", "--workers", "1"]
