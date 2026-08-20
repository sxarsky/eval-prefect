#!/usr/bin/env bash
# Staging entrypoint: render PREFECT_* env vars from configuration.py,
# then start the Prefect server.
set -euo pipefail

while IFS='=' read -r key value; do
  export "$key"="$value"
done < <(python /opt/staging/configuration.py)

exec prefect server start --host 0.0.0.0 --port 4200
