#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 check_config.py
docker compose --profile build build
docker compose up -d
docker compose ps
