"""PMS projection sync action contracts."""

from datetime import datetime

from pydantic import BaseModel


class PmsProjectionSyncScopeResponse(BaseModel):
    scope: str
    endpoint: str | None
    source_base_url: str | None
    source_endpoint: str | None
    status: str
    started_at: datetime | None
    finished_at: datetime | None
    requested_by: str | None
    rows_fetched: int
    rows_upserted: int
    rows_deleted: int
    error_code: str | None
    error_message: str | None


__all__ = ["PmsProjectionSyncScopeResponse"]
