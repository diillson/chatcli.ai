#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
IMAGE_NAME="clawd-bot-install-cli-e2e"

echo "Building Docker image..."
docker build -t "$IMAGE_NAME" -f "$ROOT_DIR/scripts/e2e/Dockerfile" "$ROOT_DIR"

echo "Running install-cli E2E..."
docker run --rm -t "$IMAGE_NAME" bash -lc '
  set -euo pipefail
  install_prefix="/tmp/clawdbot"
  /app/public/install-cli.sh --json --no-onboard --prefix "$install_prefix" > /tmp/install.jsonl
  grep "\"event\":\"done\"" /tmp/install.jsonl
  "$install_prefix/bin/clawdbot" --version
'
