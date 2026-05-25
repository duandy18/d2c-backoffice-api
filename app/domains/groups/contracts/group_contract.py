"""Backoffice group API contracts."""

from datetime import datetime

from pydantic import BaseModel, Field


class BackofficeGroupCreateRequest(BaseModel):
    group_code: str = Field(..., min_length=1, max_length=96)
    group_name: str = Field(..., min_length=1, max_length=160)
    group_kind: str = Field(..., min_length=1, max_length=32)
    description: str | None = None
    image_url: str | None = None
    sort_order: int = Field(default=100, ge=0)
    display_status: str = Field(default="visible", min_length=1, max_length=32)
    is_active: bool = True
    source_type: str = Field(default="manual", min_length=1, max_length=32)
    source_ref: str | None = Field(default=None, max_length=160)


class BackofficeGroupContract(BaseModel):
    id: int
    group_code: str
    group_name: str
    group_kind: str
    description: str | None
    image_url: str | None
    sort_order: int
    display_status: str
    is_active: bool
    source_type: str
    source_ref: str | None
    created_at: datetime
    updated_at: datetime


class BackofficeGroupsResponse(BaseModel):
    count: int = Field(..., ge=0)
    groups: list[BackofficeGroupContract]
