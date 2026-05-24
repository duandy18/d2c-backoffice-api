"""PMS projection sync run service."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.sync_runs import (
    PmsProjectionSyncRunContract,
    PmsProjectionSyncRunsResponse,
)
from app.domains.pms_projection.models.sync_runs import PmsProjectionSyncRun
from app.domains.pms_projection.repos.sync_runs import list_projection_sync_runs


def _build_sync_run(row: PmsProjectionSyncRun) -> PmsProjectionSyncRunContract:
    return PmsProjectionSyncRunContract(
        id=row.id,
        sync_scope=row.sync_scope,
        source_service=row.source_service,
        source_base_url=row.source_base_url,
        source_endpoint=row.source_endpoint,
        status=row.status,
        started_at=row.started_at,
        finished_at=row.finished_at,
        requested_by=row.requested_by,
        rows_fetched=row.rows_fetched,
        rows_upserted=row.rows_upserted,
        rows_deleted=row.rows_deleted,
        error_code=row.error_code,
        error_message=row.error_message,
        raw_summary=row.raw_summary,
    )


def get_pms_projection_sync_runs(session: Session) -> PmsProjectionSyncRunsResponse:
    rows = [_build_sync_run(row) for row in list_projection_sync_runs(session)]
    return PmsProjectionSyncRunsResponse(count=len(rows), sync_runs=rows)


__all__ = ["get_pms_projection_sync_runs"]
