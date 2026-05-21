#!/usr/bin/env bash
set -e
IMAGE=${IMAGE:-eliekh05/droidify}
TAG=${TAG:-latest}
docker build -t "$IMAGE:$TAG" .
echo "✓ Built $IMAGE:$TAG"
[[ "${PUSH:-0}" == "1" ]] && docker push "$IMAGE:$TAG" && echo "✓ Pushed"
