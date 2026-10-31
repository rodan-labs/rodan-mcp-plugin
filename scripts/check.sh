#!/usr/bin/env bash
# Validate every manifest, the listing limits and the writing rules.
# Runs in Docker (python:3.12-slim, standard library only). Nothing is installed on the host.
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
docker run --rm -v "$repo":/repo:ro -w /tmp python:3.12-slim \
  python -I -B /repo/scripts/rodan_tools.py check /repo
