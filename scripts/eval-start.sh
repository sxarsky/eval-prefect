#!/usr/bin/env bash
# Eval SUT entrypoint: install patched source, start the server, then seed
# realistic run activity once the API is healthy.
set -e

pip install --quiet --no-deps -e .

prefect server start --host 0.0.0.0 --no-services &
SERVER_PID=$!

# Wait for the API to answer before seeding.
until python -c "import urllib.request; urllib.request.urlopen('http://localhost:4200/api/health')" 2>/dev/null; do
  sleep 2
done

python /app/scripts/seed_run_durations.py || echo "[seed] skipped"

wait "$SERVER_PID"
