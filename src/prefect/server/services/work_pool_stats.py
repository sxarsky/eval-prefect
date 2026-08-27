"""
Aggregation helper for the work-pool stats endpoint.

Given a work pool id, computes the current running / pending counts and
the completed-in-the-last-24-hours count across all flow runs associated
with that pool (via the pool's work queues).
"""

from __future__ import annotations

import datetime
from typing import Any
from uuid import UUID

import prefect.server.models as models
import prefect.server.schemas as schemas
from prefect.server.schemas.states import StateType
from prefect.types._datetime import now


async def compute_work_pool_stats(
    session: Any,
    work_pool_id: UUID,
) -> dict[str, int]:
    """Return aggregate flow-run counts for a work pool.

    Keys in the returned dict:

    - ``running``: count of currently RUNNING flow runs
    - ``pending``: count of currently PENDING flow runs
    - ``completed_last_24h``: count of flow runs in a COMPLETED state whose
      ``end_time`` is within the trailing 24 hours.

    The counts are computed by filtering on the pool's associated work
    queues; if the pool has no queues, all counts are zero.
    """
    pool_filter = schemas.filters.WorkPoolFilter(
        id=schemas.filters.WorkPoolFilterId(any_=[work_pool_id])
    )

    running = await models.flow_runs.count_flow_runs(
        session=session,
        flow_run_filter=schemas.filters.FlowRunFilter(
            state=schemas.filters.FlowRunFilterState(
                type=schemas.filters.FlowRunFilterStateType(any_=[StateType.RUNNING])
            )
        ),
        work_pool_filter=pool_filter,
    )
    pending = await models.flow_runs.count_flow_runs(
        session=session,
        flow_run_filter=schemas.filters.FlowRunFilter(
            state=schemas.filters.FlowRunFilterState(
                type=schemas.filters.FlowRunFilterStateType(any_=[StateType.PENDING])
            )
        ),
        work_pool_filter=pool_filter,
    )

    since = now("UTC") - datetime.timedelta(hours=24)
    completed_last_24h = await models.flow_runs.count_flow_runs(
        session=session,
        flow_run_filter=schemas.filters.FlowRunFilter(
            state=schemas.filters.FlowRunFilterState(
                type=schemas.filters.FlowRunFilterStateType(any_=[StateType.COMPLETED])
            ),
            end_time=schemas.filters.FlowRunFilterEndTime(after_=since),
        ),
        work_pool_filter=pool_filter,
    )

    return {
        "running": running,
        "pending": pending,
        "completed_last_24h": completed_last_24h,
    }
