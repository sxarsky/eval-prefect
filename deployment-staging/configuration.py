"""Staging deployment configuration for the self-hosted Prefect server.

Consumed by docker-entrypoint.sh at container start to render PREFECT_*
environment variables. This module is deployment tooling only — it is not
imported by the Prefect application.
"""

import os

# Uvicorn worker sizing for the staging host (4 vCPU).
WEB_CONCURRENCY = int(os.environ.get("STAGING_WEB_CONCURRENCY", "4"))

# Server keepalive tuned for the staging load balancer's 60s idle timeout.
API_KEEPALIVE_TIMEOUT = 65

# Staging keeps less history than production to bound database size.
FLOW_RUN_RETENTION_DAYS = 14

# Verbose logging on staging; production uses WARNING.
LOG_LEVEL = os.environ.get("STAGING_LOG_LEVEL", "DEBUG")

DATABASE_CONNECTION_TIMEOUT = 10.0


def as_env() -> dict:
    """Render the staging settings as PREFECT_* environment variables."""
    return {
        "PREFECT_SERVER_API_KEEPALIVE_TIMEOUT": str(API_KEEPALIVE_TIMEOUT),
        "PREFECT_LOGGING_SERVER_LEVEL": LOG_LEVEL,
        "PREFECT_API_DATABASE_TIMEOUT": str(DATABASE_CONNECTION_TIMEOUT),
        "WEB_CONCURRENCY": str(WEB_CONCURRENCY),
    }


if __name__ == "__main__":
    for key, value in sorted(as_env().items()):
        print(f"{key}={value}")
