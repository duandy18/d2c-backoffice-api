"""Backoffice listing API contracts."""

from datetime import datetime

from pydantic import BaseModel, Field


class BackofficeListingHealthResponse(BaseModel):
    status: str
    module: str
    surface: str


class ProductListingConfigContract(BaseModel):
    id: int
    pms_item_id: int
    pms_sku: str
    listing_code: str
    display_name: str
    subtitle: str | None
    description_override: str | None
    cover_image_url: str | None
    listing_status: str
    display_status: str
    sell_status: str
    sort_order: int
    visible_from: datetime | None
    visible_until: datetime | None
    created_at: datetime
    updated_at: datetime


class ProductListingConfigsResponse(BaseModel):
    count: int = Field(..., ge=0)
    products: list[ProductListingConfigContract]


class SkuListingConfigContract(BaseModel):
    id: int
    product_listing_config_id: int
    pms_item_id: int
    pms_sku_code_id: int
    pms_item_uom_id: int
    pms_barcode_id: int | None
    sku_display_name: str
    sku_spec_text: str | None
    sku_image_url: str | None
    listing_status: str
    display_status: str
    sell_status: str
    sort_order: int
    visible_from: datetime | None
    visible_until: datetime | None
    created_at: datetime
    updated_at: datetime


class SkuListingConfigsResponse(BaseModel):
    count: int = Field(..., ge=0)
    skus: list[SkuListingConfigContract]
