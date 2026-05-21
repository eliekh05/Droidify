.PHONY: dev build up down logs clean

dev:
	cd backend && FRONTEND_DIR=../backend/frontend uvicorn app.main:app --host 0.0.0.0 --port 7860 --reload

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
