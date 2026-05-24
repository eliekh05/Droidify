# ── Stage 1: Build Svelte frontend ───────────────────────────────────────────
FROM node:22-alpine AS frontend-builder

WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build
# Output: /frontend/dist/

# ── Stage 2: Build Python dependencies ───────────────────────────────────────
FROM python:3.12-alpine AS py-builder

# gcc + musl-dev: required to compile lxml's C extensions
# libxml2-dev + libxslt-dev: lxml links against these at compile time
RUN apk add --no-cache gcc musl-dev libxml2-dev libxslt-dev

WORKDIR /build
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel \
 && pip install --no-cache-dir -r requirements.txt

# ── Stage 3: Final image ──────────────────────────────────────────────────────
FROM python:3.12-alpine

# Only runtime libs needed — no build tools in final image
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

COPY --from=py-builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=py-builder /usr/local/bin /usr/local/bin

ARG BUILDTIME=0
RUN echo "Build: ${BUILDTIME}"

# Copy Python backend
COPY --chown=user:user backend/app ./app

# Copy Svelte build output into the static directory FastAPI serves
COPY --from=frontend-builder --chown=user:user /frontend/dist ./app/frontend/static

USER user
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 \
    CMD python3 -c "import urllib.request,os; urllib.request.urlopen('http://localhost:'+os.environ.get('PORT','8000')+'/api/health',timeout=8)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
