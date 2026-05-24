"""PMS projection sync run contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PmsProjectionSyncRunContract(BaseModel):
    id: int
    sync_scope: str
    source_service: str
    source_base_url: str | None
    source_endpoint: str | None
    status: str
    started_at: datetime
    finished_at: datetime | None
    requested_by: str | None
    rows_fetched: int
    rows_upserted: int
    rows_deleted: int
    error_code: str | None
    error_message: str | None
    raw_summary: dict[str, Any] | None


class PmsProjectionSyncRunsResponse(BaseModel):
    count: int = Field(..., ge=0)
    sync_runs: list[PmsProjectionSyncRunContract]


__all__ = ["PmsProjectionSyncRunContract", "PmsProjectionSyncRunsResponse"]
