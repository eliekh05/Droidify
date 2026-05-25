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

command -v docker &>/dev/null || {
  echo "✗ Docker not found. Install with: curl -fsSL https://get.docker.com | sh"
  exit 1
}
docker compose version &>/dev/null || {
  echo "✗ Docker Compose not found. Update Docker to a recent version."
  exit 1
}

echo "→ Building Droidify..."
BUILDTIME=$(date +%s) docker compose build

echo "→ Starting Droidify..."
docker compose up -d

echo ""
echo "✓ Droidify running at http://localhost"
echo ""
echo "  Commands:"
echo "    make logs          — view all logs"
echo "    make logs-backend  — backend only"
echo "    make reset         — full rebuild"
echo "    make down          — stop"
echo ""
