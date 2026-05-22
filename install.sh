#!/usr/bin/env bash
set -e
command -v docker &>/dev/null || { echo "Docker required. Install with: curl -fsSL https://get.docker.com | sh"; exit 1; }
docker compose build && docker compose up -d
echo "✓ Droidify running at http://localhost:7860"
