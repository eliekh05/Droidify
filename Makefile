.PHONY: dev dev-backend dev-frontend build up down logs clean reset

# ── Development ───────────────────────────────────────────────────────────────
dev-backend:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

dev-frontend:
	cd frontend && npm run dev

# ── Frontend build ────────────────────────────────────────────────────────────
frontend-install:
	cd frontend && npm install

frontend-build:
	cd frontend && npm run build

# ── Docker ────────────────────────────────────────────────────────────────────
build:
	BUILDTIME=$$(date +%s) docker compose build

build-fresh:
	BUILDTIME=$$(date +%s) docker compose build --no-cache

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f droidify

restart:
	docker compose restart droidify

# ── Full reset ─────────────────────────────────────────────────────────────────
reset:
	docker compose down
	docker system prune -a --volumes -f
	BUILDTIME=$$(date +%s) docker compose build --no-cache
	docker compose up -d

# ── Cleanup ───────────────────────────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf frontend/dist
