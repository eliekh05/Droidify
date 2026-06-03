.PHONY: dev build build-fresh up down logs logs-nginx logs-backend restart reset clean

dev:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

build:
	BUILDTIME=$$(date +%s) docker compose build

build-fresh:
	BUILDTIME=$$(date +%s) docker compose build --no-cache

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

logs-nginx:
	docker compose logs -f nginx

logs-backend:
	docker compose logs -f backend

restart:
	docker compose restart

reset:
	docker compose down
	docker system prune -a --volumes -f
	BUILDTIME=$$(date +%s) docker compose build --no-cache
	docker compose up -d

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
