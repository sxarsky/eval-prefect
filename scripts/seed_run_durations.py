"""Eval seed: create a deployment with a mix of finished runs (that actually ran
for a few seconds) and not-yet-started runs, so the run-time view has data."""
import json
import sys
import time
import urllib.request

BASE = "http://localhost:4200/api"


def post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        BASE + path, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


try:
    flow = post("/flows/", {"name": "perf-seed-flow"})
    dep = post("/deployments/", {"name": "perf-monitoring", "flow_id": flow["id"]})
    dep_id = dep["id"]

    # 2 runs that run for ~3s then finish (non-zero total_run_time)
    running = []
    for _ in range(2):
        r = post(f"/deployments/{dep_id}/create_flow_run", {})
        post(f"/flow_runs/{r['id']}/set_state", {"state": {"type": "RUNNING"}, "force": True})
        running.append(r["id"])
    time.sleep(3)
    for rid in running:
        post(f"/flow_runs/{rid}/set_state", {"state": {"type": "COMPLETED"}, "force": True})

    # 3 runs that never started (total_run_time == 0)
    for _ in range(3):
        post(f"/deployments/{dep_id}/create_flow_run", {})

    print(f"[seed] deployment {dep_id} (perf-monitoring): 2 finished (~3s) + 3 not-started runs")
except Exception as e:
    print(f"[seed] FAILED: {e}", file=sys.stderr)
    sys.exit(0)
