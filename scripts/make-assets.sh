#!/usr/bin/env bash
# Rebuild assets/rodan-*.png from assets/source/. Runs in Docker; nothing is installed on the host.
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
docker run --rm -v "$repo":/repo -w /tmp python:3.12-slim \
  sh -c 'pip install --quiet --disable-pip-version-check --root-user-action=ignore pillow && python -I /repo/scripts/make_assets.py /repo'
