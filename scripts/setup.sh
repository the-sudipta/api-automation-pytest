#!/usr/bin/env bash
# Prepares the repo on Linux/macOS or CI (needs uv: https://docs.astral.sh/uv/).
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync
echo "Setup complete. Run: uv run pytest"
