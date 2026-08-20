#!/usr/bin/env bash
# Wait for the staging Prefect server to come up, then emit a CSRF token
# for the deploy pipeline's smoke requests.
set -euo pipefail

PREFECT_API_URL="${PREFECT_API_URL:-http://localhost:4200/api}"
CLIENT_ID="${STAGING_SMOKE_CLIENT_ID:-staging-smoke}"

for _ in $(seq 1 30); do
  if curl -fsS "${PREFECT_API_URL}/health" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

curl -fsS "${PREFECT_API_URL}/csrf-token?client=${CLIENT_ID}"
