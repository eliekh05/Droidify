.PHONY: dev build up down logs clean lint

dev:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

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
	find . -name "*.pyc" -delete 2>/dev/null || true

lint:
	cd backend && python -m py_compile app/main.py app/frontend/assets.py app/frontend/pages.py
