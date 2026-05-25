"""Backoffice client presentation API contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ClientPresentationHealthResponse(BaseModel):
    status: str
    module: str
    owner_tables: list[str]
    published_tables: list[str]


class ClientPresentationPageCreateRequest(BaseModel):
    page_code: str = Field(..., min_length=1, max_length=96)
    page_type: str = Field(..., min_length=1, max_length=32)
    route_path: str = Field(..., min_length=1, max_length=240)
    title: str = Field(..., min_length=1, max_length=160)
    description: str | None = None
    seo_title: str | None = Field(default=None, max_length=200)
    seo_description: str | None = None
    sort_order: int = Field(default=100, ge=0)
    display_status: str = Field(default="visible", min_length=1, max_length=32)
    is_active: bool = True
    source_type: str = Field(default="manual", min_length=1, max_length=32)
    source_ref: str | None = Field(default=None, max_length=160)


class ClientPresentationPageContract(BaseModel):
    id: int
    page_code: str
    page_type: str
    route_path: str
    title: str
    description: str | None
    seo_title: str | None
    seo_description: str | None
    sort_order: int
    display_status: str
    is_active: bool
    source_type: str
    source_ref: str | None
    created_at: datetime
    updated_at: datetime


class ClientPresentationPagesResponse(BaseModel):
    count: int = Field(..., ge=0)
    pages: list[ClientPresentationPageContract]


class ClientPresentationRegionCreateRequest(BaseModel):
    region_code: str = Field(..., min_length=1, max_length=120)
    region_type: str = Field(..., min_length=1, max_length=32)
    title: str = Field(..., min_length=1, max_length=160)
    description: str | None = None
    sort_order: int = Field(default=100, ge=0)
    is_required: bool = False
    max_blocks: int | None = Field(default=None, ge=1)
    allowed_block_types: list[str] = Field(default_factory=list)
    display_status: str = Field(default="visible", min_length=1, max_length=32)
    is_active: bool = True
    source_type: str = Field(default="manual", min_length=1, max_length=32)
    source_ref: str | None = Field(default=None, max_length=160)


class ClientPresentationRegionContract(BaseModel):
    id: int
    page_id: int
    page_code: str
    region_code: str
    region_type: str
    title: str
    description: str | None
    sort_order: int
    is_required: bool
    max_blocks: int | None
    allowed_block_types: list[str]
    display_status: str
    is_active: bool
    source_type: str
    source_ref: str | None
    created_at: datetime
    updated_at: datetime


class ClientPresentationRegionsResponse(BaseModel):
    count: int = Field(..., ge=0)
    regions: list[ClientPresentationRegionContract]


class ClientPresentationBlockTypeCreateRequest(BaseModel):
    block_type: str = Field(..., min_length=1, max_length=64)
    display_name: str = Field(..., min_length=1, max_length=160)
    description: str | None = None
    renderer_key: str = Field(..., min_length=1, max_length=160)
    data_contract_version: str = Field(default="v1", min_length=1, max_length=32)
    allowed_region_types: list[str] = Field(default_factory=list)
    allowed_content_types: list[str] = Field(default_factory=list)
    layout_schema: dict[str, Any] | None = None
    slot_schema: dict[str, Any] | None = None
    action_schema: dict[str, Any] | None = None
    analytics_schema: dict[str, Any] | None = None
    display_status: str = Field(default="visible", min_length=1, max_length=32)
    is_active: bool = True
    source_type: str = Field(default="manual", min_length=1, max_length=32)
    source_ref: str | None = Field(default=None, max_length=160)


class ClientPresentationBlockTypeContract(BaseModel):
    id: int
    block_type: str
    display_name: str
    description: str | None
    renderer_key: str
    data_contract_version: str
    allowed_region_types: list[str]
    allowed_content_types: list[str]
    layout_schema: dict[str, Any] | None
    slot_schema: dict[str, Any] | None
    action_schema: dict[str, Any] | None
    analytics_schema: dict[str, Any] | None
    display_status: str
    is_active: bool
    source_type: str
    source_ref: str | None
    created_at: datetime
    updated_at: datetime


class ClientPresentationBlockTypesResponse(BaseModel):
    count: int = Field(..., ge=0)
    block_types: list[ClientPresentationBlockTypeContract]
