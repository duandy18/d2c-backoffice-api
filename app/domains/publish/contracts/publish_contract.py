"""Backoffice publish API contracts."""

from datetime import datetime

from pydantic import BaseModel, Field


class BackofficePublishHealthResponse(BaseModel):
    status: str
    module: str
    surface: str


class PublishVersionContract(BaseModel):
    id: int
    publish_version: str
    publish_scope: str
    status: str
    source: str
    started_at: datetime | None
    published_at: datetime | None
    published_by: str | None
    note: str | None
    created_at: datetime
    updated_at: datetime


class PublishVersionsResponse(BaseModel):
    count: int = Field(..., ge=0)
    publish_versions: list[PublishVersionContract]
