"""Backoffice PMS projection API contracts."""

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class PmsProjectionHealthResponse(BaseModel):
    status: str
    module: str
    surface: str


class PmsProductProjectionContract(BaseModel):
    id: int
    pms_item_id: int
    pms_sku: str
    item_name: str
    item_spec: str | None
    enabled: bool
    supplier_id: int | None
    brand_id: int | None
    brand_code: str | None
    brand_name: str | None
    category_id: int | None
    category_code: str | None
    category_name: str | None
    category_path_code: str | None
    category_level: int | None
    category_is_leaf: bool | None
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsProductProjectionsResponse(BaseModel):
    count: int = Field(..., ge=0)
    products: list[PmsProductProjectionContract]


class PmsUnitProjectionContract(BaseModel):
    id: int
    pms_item_uom_id: int
    pms_item_id: int
    uom: str
    uom_name: str
    display_name: str | None
    ratio_to_base: Decimal
    net_weight_kg: Decimal | None
    is_base: bool
    is_purchase_default: bool
    is_inbound_default: bool
    is_outbound_default: bool
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsUnitProjectionsResponse(BaseModel):
    count: int = Field(..., ge=0)
    units: list[PmsUnitProjectionContract]


class PmsSkuCodeProjectionContract(BaseModel):
    id: int
    pms_sku_code_id: int
    pms_item_id: int
    sku_code: str
    code_type: str
    is_primary: bool
    is_active: bool
    effective_from: datetime | None
    effective_to: datetime | None
    remark: str | None
    item_sku: str
    item_name: str
    item_enabled: bool
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsSkuCodeProjectionsResponse(BaseModel):
    count: int = Field(..., ge=0)
    sku_codes: list[PmsSkuCodeProjectionContract]


class PmsBarcodeProjectionContract(BaseModel):
    id: int
    pms_barcode_id: int
    pms_item_id: int
    pms_item_uom_id: int
    barcode: str
    symbology: str | None
    active: bool
    is_primary: bool
    uom: str
    uom_name: str
    ratio_to_base: Decimal
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsBarcodeProjectionsResponse(BaseModel):
    count: int = Field(..., ge=0)
    barcodes: list[PmsBarcodeProjectionContract]


class PmsItemContentProjectionContract(BaseModel):
    id: int
    pms_content_id: int
    pms_item_id: int
    item_sku: str | None
    item_name: str | None
    base_title: str | None
    base_description: str | None
    short_description: str | None
    spec_params: dict[str, Any] | list[Any] | None
    material_text: str | None
    ingredients_text: str | None
    dimensions_text: str | None
    weight_text: str | None
    safety_instructions: str | None
    usage_instructions: str | None
    storage_instructions: str | None
    status: str
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsItemContentsProjectionResponse(BaseModel):
    count: int = Field(..., ge=0)
    item_contents: list[PmsItemContentProjectionContract]


class PmsItemAssetProjectionContract(BaseModel):
    id: int
    pms_asset_id: int
    pms_item_id: int
    item_sku: str | None
    item_name: str | None
    asset_type: str
    usage_type: str
    source_type: str
    object_key: str | None
    url: str | None
    alt_text: str | None
    sort_order: int
    is_primary: bool
    status: str
    raw_meta: dict[str, Any] | None
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsItemAssetsProjectionResponse(BaseModel):
    count: int = Field(..., ge=0)
    item_assets: list[PmsItemAssetProjectionContract]


class PmsDisplayCategoryProjectionContract(BaseModel):
    id: int
    pms_display_category_id: int
    parent_id: int | None
    level: int
    category_code: str
    category_name: str
    display_name: str | None
    path_code: str
    description: str | None
    image_url: str | None
    sort_order: int
    is_active: bool
    is_leaf: bool
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsDisplayCategoriesProjectionResponse(BaseModel):
    count: int = Field(..., ge=0)
    display_categories: list[PmsDisplayCategoryProjectionContract]


class PmsItemDisplayCategoryBindingProjectionContract(BaseModel):
    id: int
    pms_binding_id: int
    pms_item_id: int
    pms_display_category_id: int
    item_sku: str | None
    item_name: str | None
    display_category_code: str | None
    display_category_name: str | None
    display_category_path_code: str | None
    is_primary: bool
    sort_order: int
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsItemDisplayCategoryBindingsProjectionResponse(BaseModel):
    count: int = Field(..., ge=0)
    item_display_category_bindings: list[PmsItemDisplayCategoryBindingProjectionContract]


class PmsBrandProfileProjectionContract(BaseModel):
    id: int
    pms_profile_id: int
    brand_id: int
    brand_code: str | None
    brand_name: str | None
    display_name: str | None
    official_name: str | None
    brand_story: str | None
    country_or_region: str | None
    website_url: str | None
    seo_title: str | None
    seo_description: str | None
    status: str
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsBrandProfilesProjectionResponse(BaseModel):
    count: int = Field(..., ge=0)
    brand_profiles: list[PmsBrandProfileProjectionContract]


class PmsBrandAssetProjectionContract(BaseModel):
    id: int
    pms_asset_id: int
    brand_id: int
    brand_code: str | None
    brand_name: str | None
    asset_type: str
    usage_type: str
    object_key: str | None
    url: str | None
    alt_text: str | None
    sort_order: int
    is_primary: bool
    status: str
    raw_meta: dict[str, Any] | None
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsBrandAssetsProjectionResponse(BaseModel):
    count: int = Field(..., ge=0)
    brand_assets: list[PmsBrandAssetProjectionContract]


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
