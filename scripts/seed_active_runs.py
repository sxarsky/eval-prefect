"""Eval seed: create a deployment with a realistic mix of active and finished
flow runs so the deployment's run-activity view has data to report. Runs after
the server is healthy (invoked by scripts/eval-start.sh)."""
import json
import sys
import urllib.error
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

    # 3 active (non-terminal) runs
    for _ in range(3):
        post(f"/deployments/{dep_id}/create_flow_run", {})

    # 2 finished (terminal) runs — force straight to CANCELLED
    for _ in range(2):
        run = post(f"/deployments/{dep_id}/create_flow_run", {})
        post(f"/flow_runs/{run['id']}/set_state", {"state": {"type": "CANCELLED"}, "force": True})

    print(f"[seed] deployment {dep_id} (perf-monitoring): 3 active + 2 cancelled flow runs")
except Exception as e:  # never block server startup
    print(f"[seed] FAILED: {e}", file=sys.stderr)
    sys.exit(0)
