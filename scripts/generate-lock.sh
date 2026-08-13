#!/usr/bin/env bash
set -euo pipefail

# Generate a reproducible requirements.lock for runtime packages.
# Requires `pip-tools` (pip install pip-tools) and network access.
# Run from the repository root: ./scripts/generate-lock.sh

here="$(cd "$(dirname "$0")/.." && pwd)"
cd "$here"

if ! command -v pip-compile >/dev/null 2>&1; then
  echo "pip-compile not found. Install pip-tools: pip install pip-tools" >&2
  exit 2
fi

echo "Generating requirements.lock from requirements.txt..."
pip-compile --output-file=requirements.lock requirements.txt
echo "Wrote requirements.lock"
