#!/usr/bin/env bash
set -e
command -v docker &>/dev/null || { echo "Docker required: https://docs.docker.com/get-docker/"; exit 1; }
docker compose build && docker compose up -d
echo "✓ Droidify running at http://localhost:7860"
