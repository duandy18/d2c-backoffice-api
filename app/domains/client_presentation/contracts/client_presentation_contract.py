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


class ClientPresentationSurfaceCreateRequest(BaseModel):
    surface_code: str = Field(..., min_length=1, max_length=64)
    surface_name: str = Field(..., min_length=1, max_length=160)
    surface_type: str = Field(..., min_length=1, max_length=32)
    device_family: str = Field(..., min_length=1, max_length=32)
    breakpoint_profile: dict[str, Any] | None = None
    supported_renderer_keys: list[str] = Field(default_factory=list)
    is_active: bool = True
    source_type: str = Field(default="manual", min_length=1, max_length=32)
    source_ref: str | None = Field(default=None, max_length=160)


class ClientPresentationSurfaceContract(BaseModel):
    id: int
    surface_code: str
    surface_name: str
    surface_type: str
    device_family: str
    breakpoint_profile: dict[str, Any] | None
    supported_renderer_keys: list[str]
    is_active: bool
    source_type: str
    source_ref: str | None
    created_at: datetime
    updated_at: datetime


class ClientPresentationSurfacesResponse(BaseModel):
    count: int = Field(..., ge=0)
    surfaces: list[ClientPresentationSurfaceContract]


class ClientPresentationDataBindingCreateRequest(BaseModel):
    binding_code: str = Field(..., min_length=1, max_length=96)
    target_type: str = Field(..., min_length=1, max_length=32)
    target_code: str = Field(..., min_length=1, max_length=120)
    data_source_type: str = Field(..., min_length=1, max_length=32)
    data_source_ref: str | None = Field(default=None, max_length=160)
    content_type: str = Field(..., min_length=1, max_length=32)
    query_params: dict[str, Any] | None = None
    result_limit: int | None = Field(default=None, ge=1)
    sort_policy: dict[str, Any] | None = None
    refresh_policy: dict[str, Any] | None = None
    is_active: bool = True
    source_type: str = Field(default="manual", min_length=1, max_length=32)
    source_ref: str | None = Field(default=None, max_length=160)


class ClientPresentationDataBindingContract(BaseModel):
    id: int
    binding_code: str
    target_type: str
    target_code: str
    data_source_type: str
    data_source_ref: str | None
    content_type: str
    query_params: dict[str, Any] | None
    result_limit: int | None
    sort_policy: dict[str, Any] | None
    refresh_policy: dict[str, Any] | None
    is_active: bool
    source_type: str
    source_ref: str | None
    created_at: datetime
    updated_at: datetime


class ClientPresentationDataBindingsResponse(BaseModel):
    count: int = Field(..., ge=0)
    data_bindings: list[ClientPresentationDataBindingContract]


class ClientPresentationVisibilityRuleCreateRequest(BaseModel):
    rule_code: str = Field(..., min_length=1, max_length=96)
    target_type: str = Field(..., min_length=1, max_length=32)
    target_code: str = Field(..., min_length=1, max_length=120)
    client_surface_codes: list[str] = Field(default_factory=list)
    customer_segments: list[str] = Field(default_factory=list)
    login_state: str | None = Field(default=None, max_length=32)
    locale: str | None = Field(default=None, max_length=16)
    currency: str | None = Field(default=None, max_length=3)
    visible_from: datetime | None = None
    visible_until: datetime | None = None
    rule_expression: dict[str, Any] | None = None
    priority: int = Field(default=100, ge=0)
    is_active: bool = True
    source_type: str = Field(default="manual", min_length=1, max_length=32)
    source_ref: str | None = Field(default=None, max_length=160)


class ClientPresentationVisibilityRuleContract(BaseModel):
    id: int
    rule_code: str
    target_type: str
    target_code: str
    client_surface_codes: list[str]
    customer_segments: list[str]
    login_state: str | None
    locale: str | None
    currency: str | None
    visible_from: datetime | None
    visible_until: datetime | None
    rule_expression: dict[str, Any] | None
    priority: int
    is_active: bool
    source_type: str
    source_ref: str | None
    created_at: datetime
    updated_at: datetime


class ClientPresentationVisibilityRulesResponse(BaseModel):
    count: int = Field(..., ge=0)
    visibility_rules: list[ClientPresentationVisibilityRuleContract]


class ClientPresentationActionPolicyCreateRequest(BaseModel):
    policy_code: str = Field(..., min_length=1, max_length=96)
    target_type: str = Field(..., min_length=1, max_length=32)
    target_code: str = Field(..., min_length=1, max_length=120)
    action_type: str = Field(..., min_length=1, max_length=32)
    label: str | None = Field(default=None, max_length=120)
    target_url: str | None = None
    target_page_code: str | None = Field(default=None, max_length=96)
    target_ref: str | None = Field(default=None, max_length=160)
    open_mode: str = Field(default="same", min_length=1, max_length=32)
    action_payload: dict[str, Any] | None = None
    is_active: bool = True
    source_type: str = Field(default="manual", min_length=1, max_length=32)
    source_ref: str | None = Field(default=None, max_length=160)


class ClientPresentationActionPolicyContract(BaseModel):
    id: int
    policy_code: str
    target_type: str
    target_code: str
    action_type: str
    label: str | None
    target_url: str | None
    target_page_code: str | None
    target_ref: str | None
    open_mode: str
    action_payload: dict[str, Any] | None
    is_active: bool
    source_type: str
    source_ref: str | None
    created_at: datetime
    updated_at: datetime


class ClientPresentationActionPoliciesResponse(BaseModel):
    count: int = Field(..., ge=0)
    action_policies: list[ClientPresentationActionPolicyContract]


class ClientPresentationTrackingPolicyCreateRequest(BaseModel):
    policy_code: str = Field(..., min_length=1, max_length=96)
    target_type: str = Field(..., min_length=1, max_length=32)
    target_code: str = Field(..., min_length=1, max_length=120)
    event_name: str = Field(..., min_length=1, max_length=96)
    event_type: str = Field(..., min_length=1, max_length=32)
    event_trigger: str = Field(..., min_length=1, max_length=32)
    tracking_params: dict[str, Any] | None = None
    is_required: bool = False
    is_active: bool = True
    source_type: str = Field(default="manual", min_length=1, max_length=32)
    source_ref: str | None = Field(default=None, max_length=160)


class ClientPresentationTrackingPolicyContract(BaseModel):
    id: int
    policy_code: str
    target_type: str
    target_code: str
    event_name: str
    event_type: str
    event_trigger: str
    tracking_params: dict[str, Any] | None
    is_required: bool
    is_active: bool
    source_type: str
    source_ref: str | None
    created_at: datetime
    updated_at: datetime


class ClientPresentationTrackingPoliciesResponse(BaseModel):
    count: int = Field(..., ge=0)
    tracking_policies: list[ClientPresentationTrackingPolicyContract]
