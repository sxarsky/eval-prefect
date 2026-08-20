"""
Aggregation helper for work-queue stats.

Both ``GET /api/work_queues/{id}/stats`` and the nested ``stats`` block on
``GET /api/work_queues/{id}`` call into this helper so the two surfaces
agree on every field — there is a single source of truth for each count.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

import prefect.server.models as models
import prefect.server.schemas as schemas
from prefect.server.schemas.states import StateType


async def compute_work_queue_stats(
    session: Any,
    work_queue_id: UUID,
) -> dict[str, int]:
    """Return aggregate flow-run counts for a work queue.

    Keys:

    - ``running``: count of currently RUNNING flow runs routed to this queue
    - ``pending``: count of currently PENDING flow runs routed to this queue
    - ``scheduled_count``: count of currently SCHEDULED flow runs routed to
      this queue (included in the response of both the /stats endpoint and
      the parent GET /{id} response's nested ``stats`` block — consumers
      can rely on the two surfaces agreeing exactly)
    """
    wq_filter = schemas.filters.WorkQueueFilter(
        id=schemas.filters.WorkQueueFilterId(any_=[work_queue_id])
    )

    async def _count(state_type: StateType) -> int:
        return await models.flow_runs.count_flow_runs(
            session=session,
            flow_run_filter=schemas.filters.FlowRunFilter(
                state=schemas.filters.FlowRunFilterState(
                    type=schemas.filters.FlowRunFilterStateType(any_=[state_type])
                )
            ),
            work_queue_filter=wq_filter,
        )

    return {
        "running": await _count(StateType.RUNNING),
        "pending": await _count(StateType.PENDING),
        "scheduled_count": await _count(StateType.SCHEDULED),
    }
