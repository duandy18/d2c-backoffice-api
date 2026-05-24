"""PMS projection sync action contracts."""

from pydantic import BaseModel


class PmsProjectionSyncScopeResponse(BaseModel):
    scope: str
    endpoint: str | None
    status: str
    rows_fetched: int
    rows_upserted: int
    error_code: str | None
    error_message: str | None


__all__ = ["PmsProjectionSyncScopeResponse"]
