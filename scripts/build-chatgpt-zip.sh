#!/usr/bin/env bash
# Build dist/rodan-chatgpt-plugin-VERSION.zip and validate the built ZIP.
# Runs in Docker (python:3.12-slim, standard library only). Nothing is installed on the host.
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
docker run --rm -v "$repo":/repo:rw -w /tmp python:3.12-slim \
  python -I -B /repo/scripts/rodan_tools.py zip /repo
