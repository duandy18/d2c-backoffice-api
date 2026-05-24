"""Backoffice listing API contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class BackofficeListingHealthResponse(BaseModel):
    status: str
    module: str
    surface: str


class ProductListingContentContract(BaseModel):
    id: int
    product_listing_config_id: int
    display_title: str
    subtitle: str | None
    short_description: str | None
    detail_description: str | None
    seo_title: str | None
    seo_description: str | None
    selling_points: dict[str, Any] | list[Any] | None
    content_status: str
    created_at: datetime
    updated_at: datetime


class ProductListingMediaContract(BaseModel):
    id: int
    product_listing_config_id: int
    media_type: str
    source_type: str
    pms_asset_id: int | None
    object_key: str | None
    url: str | None
    alt_text: str | None
    usage_type: str
    sort_order: int
    is_primary: bool
    status: str
    created_at: datetime
    updated_at: datetime


class ProductListingConfigContract(BaseModel):
    id: int
    pms_item_id: int
    pms_sku: str
    listing_code: str
    listing_status: str
    display_status: str
    sell_status: str
    sort_order: int
    visible_from: datetime | None
    visible_until: datetime | None
    created_at: datetime
    updated_at: datetime
    content: ProductListingContentContract | None
    media: list[ProductListingMediaContract]


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
