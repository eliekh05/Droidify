FROM python:3.12-alpine AS builder

RUN apk add --no-cache gcc musl-dev libxml2-dev libxslt-dev

WORKDIR /build
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel \
 && pip install --no-cache-dir -r requirements.txt

# ── Final image ───────────────────────────────────────────────────────────────
FROM python:3.12-alpine

RUN adduser -D -u 1000 -g "" user \
 && apk add --no-cache libxml2 libxslt

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PORT=8000 \
    CORS_ORIGINS="*" \
    SCRAPER_USER_AGENT="DroidifyBot/2.0" \
    SCRAPER_CONCURRENCY="10" \
    SCRAPER_TIMEOUT="20" \
    CACHE_DEFAULT_TTL="300"

WORKDIR /home/user/app

# Copy installed packages from builder — no gcc in final image
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

ARG BUILDTIME=0
RUN echo "Build: ${BUILDTIME}"

COPY --chown=user:user backend/app ./app

USER user

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 \
    CMD python3 -c "import urllib.request,os; urllib.request.urlopen('http://localhost:'+os.environ.get('PORT','8000')+'/api/health',timeout=8)"

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
