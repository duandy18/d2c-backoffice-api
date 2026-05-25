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
    source_promotion_rule_id: int | None
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


class PublishedClientPageSnapshotExport(BaseModel):
    publish_version: str
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
    published_at: datetime
    source_page_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedClientPagesExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    pages: list[PublishedClientPageSnapshotExport]


class PublishedClientRegionSnapshotExport(BaseModel):
    publish_version: str
    page_code: str
    region_code: str
    region_type: str
    title: str
    description: str | None
    sort_order: int
    is_required: bool
    max_blocks: int | None
    allowed_block_types: list[str] | None
    display_status: str
    is_active: bool
    published_at: datetime
    source_region_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedClientRegionsExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    regions: list[PublishedClientRegionSnapshotExport]


class PublishedClientBlockTypeSnapshotExport(BaseModel):
    publish_version: str
    block_type: str
    display_name: str
    description: str | None
    renderer_key: str
    data_contract_version: str
    allowed_region_types: list[str] | None
    allowed_content_types: list[str] | None
    layout_schema: dict[str, Any] | None
    slot_schema: dict[str, Any] | None
    action_schema: dict[str, Any] | None
    analytics_schema: dict[str, Any] | None
    display_status: str
    is_active: bool
    published_at: datetime
    source_block_type_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedClientBlockTypesExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    block_types: list[PublishedClientBlockTypeSnapshotExport]


class PublishedGroupExport(BaseModel):
    publish_version: str
    group_code: str
    group_name: str
    group_kind: str
    description: str | None
    image_url: str | None
    sort_order: int
    display_status: str
    is_active: bool
    published_at: datetime
    source_group_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedGroupsExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    groups: list[PublishedGroupExport]


class PublishedOfferSnapshotExport(BaseModel):
    publish_version: str
    offer_code: str
    offer_type: str
    title: str
    subtitle: str | None
    description: str | None
    image_url: str | None
    display_status: str
    sell_status: str
    published_at: datetime
    source_offer_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedOffersExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    offers: list[PublishedOfferSnapshotExport]


class PublishedOfferComponentSnapshotExport(BaseModel):
    publish_version: str
    offer_code: str
    component_no: int
    pms_item_id: int
    pms_sku: str
    pms_sku_code_id: int
    sku_code: str
    pms_item_uom_id: int
    uom_code: str
    uom_name: str
    pms_barcode_id: int | None
    barcode: str | None
    quantity: str
    component_role: str
    sort_order: int
    required: bool
    published_at: datetime
    source_component_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedOfferComponentsExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    components: list[PublishedOfferComponentSnapshotExport]


class PublishedOfferPriceSnapshotExport(BaseModel):
    publish_version: str
    offer_code: str
    price_code: str
    channel: str
    currency: str
    price_cents: int
    compare_at_price_cents: int | None
    effective_from: datetime | None
    effective_until: datetime | None
    is_active: bool
    priority: int
    published_at: datetime
    source_price_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedOfferPricesExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    prices: list[PublishedOfferPriceSnapshotExport]


class PublishedOfferPositionSnapshotExport(BaseModel):
    publish_version: str
    position_code: str
    group_code: str
    offer_code: str
    sort_order: int
    position_source: str
    is_featured: bool
    visible_from: datetime | None
    visible_until: datetime | None
    is_active: bool
    published_at: datetime
    source_position_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedOfferPositionsExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    positions: list[PublishedOfferPositionSnapshotExport]


class PublishedPromotionRuleSnapshotExport(BaseModel):
    publish_version: str
    promotion_code: str
    promotion_name: str
    description: str | None
    promotion_type: str
    discount_type: str
    discount_value: int
    threshold_amount_cents: int | None
    max_discount_cents: int | None
    currency: str
    starts_at: datetime | None
    ends_at: datetime | None
    priority: int
    stackable: bool
    is_active: bool
    display_badge: str | None
    published_at: datetime
    source_promotion_rule_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedPromotionRulesExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    promotion_rules: list[PublishedPromotionRuleSnapshotExport]


class PublishedPromotionTargetSnapshotExport(BaseModel):
    publish_version: str
    promotion_code: str
    target_type: str
    target_id: int | None
    target_code: str | None
    published_at: datetime
    source_target_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedPromotionTargetsExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    promotion_targets: list[PublishedPromotionTargetSnapshotExport]


class PublishedCouponSnapshotExport(BaseModel):
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
    raw_payload: dict[str, Any] | None


class PublishedCouponsSnapshotExportResponse(BaseModel):
    publish_version: str | None
    count: int = Field(..., ge=0)
    coupons: list[PublishedCouponSnapshotExport]


class PublishedStorefrontSectionSnapshotExport(BaseModel):
    publish_version: str
    section_code: str
    section_type: str
    group_code: str | None
    title: str
    subtitle: str | None
    description: str | None
    sort_order: int
    display_status: str
    is_active: bool
    published_at: datetime
    source_section_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedStorefrontSectionsExportResponse(BaseModel):
    publish_version: str | None
    count: int
    sections: list[PublishedStorefrontSectionSnapshotExport]


class PublishedStorefrontSectionLayoutSnapshotExport(BaseModel):
    publish_version: str
    section_code: str
    display_type: str
    columns_desktop: int
    columns_tablet: int
    columns_mobile: int
    card_size: str
    image_ratio: str
    show_promotion_badge: bool
    show_sales_summary: bool
    show_review_summary: bool
    show_compare_price: bool
    show_quantity_stepper: bool
    max_items: int | None
    published_at: datetime
    source_layout_id: int | None
    raw_payload: dict[str, Any] | None



class PublishedStorefrontSectionPositionSnapshotExport(BaseModel):
    publish_version: str
    section_code: str
    position_code: str
    offer_code: str
    sort_order: int
    position_type: str
    is_featured: bool
    visible_from: datetime | None
    visible_until: datetime | None
    is_active: bool
    published_at: datetime
    source_position_id: int | None
    raw_payload: dict[str, Any] | None


class PublishedStorefrontSectionPositionsExportResponse(BaseModel):
    publish_version: str | None
    count: int
    positions: list[PublishedStorefrontSectionPositionSnapshotExport]

class PublishedStorefrontSectionLayoutsExportResponse(BaseModel):
    publish_version: str | None
    count: int
    layouts: list[PublishedStorefrontSectionLayoutSnapshotExport]
