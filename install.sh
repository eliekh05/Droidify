#!/usr/bin/env bash
set -e

echo ""
echo "  ██████╗ ██████╗  ██████╗ ██╗██████╗ ██╗███████╗██╗   ██╗"
echo "  ██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗██║██╔════╝╚██╗ ██╔╝"
echo "  ██║  ██║██████╔╝██║   ██║██║██║  ██║██║█████╗   ╚████╔╝ "
echo "  ██║  ██║██╔══██╗██║   ██║██║██║  ██║██║██╔══╝    ╚██╔╝  "
echo "  ██████╔╝██║  ██║╚██████╔╝██║██████╔╝██║██║        ██║   "
echo "  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝ ╚═╝╚═╝        ╚═╝  "
echo ""
echo "  Android ROM & Device Index"
echo ""

# Check Docker
if ! command -v docker &>/dev/null; then
  echo "✗ Docker not found. Install with:"
  echo "  curl -fsSL https://get.docker.com | sh"
  exit 1
fi

# Check Docker Compose
if ! docker compose version &>/dev/null; then
  echo "✗ Docker Compose not found. Update Docker to a recent version."
  exit 1
fi

echo "→ Building Droidify (this may take a few minutes on first run)..."
docker compose build

echo "→ Starting Droidify..."
docker compose up -d

echo ""
echo "✓ Droidify is running at http://localhost:8000"
echo ""
echo "  Useful commands:"
echo "    docker logs droidify -f     — view logs"
echo "    docker compose down         — stop"
echo "    docker compose restart      — restart"
echo ""
