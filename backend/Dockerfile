FROM python:3.12-alpine AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-alpine

RUN adduser -D -u 1000 -g "" user

ENV PORT=8000 \
    CORS_ORIGINS="*" \
    CACHE_DEFAULT_TTL="300"

WORKDIR /home/user/app

COPY --from=builder /usr/local/lib/python3.12/site-packages \
                    /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

ARG BUILDTIME=unknown
RUN echo "${BUILDTIME}"

COPY --chown=user:user app     ./app

USER user
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 \
    CMD python3 -c \
    "import urllib.request,os; urllib.request.urlopen('http://localhost:'+os.environ.get('PORT','8000')+'/api/health',timeout=8)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
