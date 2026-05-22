FROM python:alpine

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

RUN apk add --no-cache gcc musl-dev libxml2-dev libxslt-dev

RUN pip install --no-cache-dir --upgrade pip wheel

ARG BUILDTIME=0
RUN echo "Build timestamp: ${BUILDTIME}"

COPY --chown=user:user backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apk del gcc musl-dev

COPY --chown=user:user backend/app ./app

USER user

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 \
    CMD python3 -c "import urllib.request,os; urllib.request.urlopen('http://localhost:'+os.environ.get('PORT')+'/api/health',timeout=8)"

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860} --workers 1
