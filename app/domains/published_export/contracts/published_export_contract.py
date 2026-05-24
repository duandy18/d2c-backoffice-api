"""Backoffice read-v1 published export contracts.

These contracts are consumed by d2c-api published sync. Keep field names aligned
with d2c-api d2c_published_* runtime tables, excluding runtime-local id and
created/updated timestamps.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PublishedExportHealthResponse(BaseModel):
    status: str
    module: str
    surface: str


class PublishedProductExport(BaseModel):
    publish_version: str
    pms_item_id: int | None
    pms_sku: str | None
    product_code: str
    product_name: str
    display_name: str
    description: str | None
    image_url: str | None
    category_code: str | None
    category_name: str | None
    brand_code: str | None
    brand_name: str | None
    display_status: str
    sell_status: str
    sort_order: int
    visible_from: datetime | None
    visible_until: datetime | None
    published_at: datetime
    source_product_id: int | None
    source_updated_at: datetime | None
    raw_payload: dict[str, Any] | None


class PublishedSkuExport(BaseModel):
    publish_version: str
    product_code: str
    sku_code: str
    sku_name: str
    display_sku_name: str
    sales_unit_code: str | None
    sales_unit_name: str | None
    barcode: str | None
    spec_text: str | None
    is_sellable: bool
    sort_order: int
    published_at: datetime
    source_sku_id: int | None
    source_updated_at: datetime | None
    raw_payload: dict[str, Any] | None


class PublishedCatalogExportResponse(BaseModel):
    publish_version: str | None
    product_count: int = Field(..., ge=0)
    sku_count: int = Field(..., ge=0)
    products: list[PublishedProductExport]
    skus: list[PublishedSkuExport]


class PublishedPriceExport(BaseModel):
    publish_version: str
    price_list_code: str
    channel: str
    sku_code: str
    currency: str
    price_cents: int
    compare_at_price_cents: int | None
    effective_from: datetime | None
    effective_until: datetime | None
    is_active: bool
    priority: int
    published_at: datetime
    source_price_id: int | None
    source_updated_at: datetime | None
    raw_payload: dict[str, Any] | None


class PublishedPricesExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    prices: list[PublishedPriceExport]


class PublishedPromotionExport(BaseModel):
    publish_version: str
    promotion_code: str
    promotion_name: str
    promotion_type: str
    discount_type: str
    discount_value: int
    scope_type: str
    min_order_amount_cents: int | None
    max_discount_cents: int | None
    currency: str
    starts_at: datetime | None
    ends_at: datetime | None
    priority: int
    stackable: bool
    is_active: bool
    published_at: datetime
    source_promotion_id: int | None
    source_updated_at: datetime | None
    raw_payload: dict[str, Any] | None


class PublishedPromotionsExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    promotions: list[PublishedPromotionExport]


class PublishedCouponExport(BaseModel):
    publish_version: str
    coupon_code: str
    coupon_name: str
    promotion_code: str
    coupon_type: str
    total_limit: int | None
    per_customer_limit: int | None
    starts_at: datetime | None
    ends_at: datetime | None
    is_active: bool
    published_at: datetime
    source_coupon_id: int | None
    source_updated_at: datetime | None
    raw_payload: dict[str, Any] | None


class PublishedCouponsExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    coupons: list[PublishedCouponExport]
