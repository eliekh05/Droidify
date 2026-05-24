#!/usr/bin/env bash
set -e

IMAGE=${IMAGE:-eliekh05/droidify}
TAG=${TAG:-latest}

echo "→ Building $IMAGE:$TAG"
docker build -t "$IMAGE:$TAG" .
echo "✓ Built $IMAGE:$TAG"

if [ "${PUSH:-0}" = "1" ]; then
  docker push "$IMAGE:$TAG"
  echo "✓ Pushed $IMAGE:$TAG"
fi
