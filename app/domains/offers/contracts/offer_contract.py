"""Backoffice Offer API contracts."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class BackofficeOfferCreateRequest(BaseModel):
    offer_code: str = Field(..., min_length=1, max_length=96)
    offer_type: str = Field(..., min_length=1, max_length=32)
    title: str = Field(..., min_length=1, max_length=200)
    subtitle: str | None = Field(default=None, max_length=240)
    description: str | None = None
    image_url: str | None = None
    display_status: str = Field(default="hidden", min_length=1, max_length=32)
    sell_status: str = Field(default="not_sellable", min_length=1, max_length=32)
    publish_status: str = Field(default="draft", min_length=1, max_length=32)
    source_type: str = Field(default="manual", min_length=1, max_length=32)
    sort_order: int = Field(default=100, ge=0)
    visible_from: datetime | None = None
    visible_until: datetime | None = None


class BackofficeOfferContract(BaseModel):
    id: int
    offer_code: str
    offer_type: str
    title: str
    subtitle: str | None
    description: str | None
    image_url: str | None
    display_status: str
    sell_status: str
    publish_status: str
    source_type: str
    sort_order: int
    visible_from: datetime | None
    visible_until: datetime | None
    created_at: datetime
    updated_at: datetime


class BackofficeOffersResponse(BaseModel):
    count: int = Field(..., ge=0)
    offers: list[BackofficeOfferContract]


class BackofficeOfferComponentCreateRequest(BaseModel):
    pms_item_id: int
    pms_sku_code_id: int
    pms_item_uom_id: int
    pms_barcode_id: int | None = None
    quantity: Decimal = Field(..., gt=0)
    component_role: str = Field(default="primary", min_length=1, max_length=32)
    sort_order: int = Field(default=100, ge=0)
    required: bool = True


class BackofficeOfferComponentContract(BaseModel):
    id: int
    offer_id: int
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
    quantity: Decimal
    component_role: str
    sort_order: int
    required: bool
    created_at: datetime
    updated_at: datetime


class BackofficeOfferPriceCreateRequest(BaseModel):
    price_code: str = Field(..., min_length=1, max_length=96)
    channel: str = Field(default="storefront", min_length=1, max_length=32)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    price_cents: int = Field(..., ge=0)
    compare_at_price_cents: int | None = Field(default=None, ge=0)
    effective_from: datetime | None = None
    effective_until: datetime | None = None
    is_active: bool = True
    priority: int = Field(default=100, ge=0)


class BackofficeOfferPriceContract(BaseModel):
    id: int
    offer_id: int
    price_code: str
    channel: str
    currency: str
    price_cents: int
    compare_at_price_cents: int | None
    effective_from: datetime | None
    effective_until: datetime | None
    is_active: bool
    priority: int
    created_at: datetime
    updated_at: datetime


class BackofficeOfferPositionCreateRequest(BaseModel):
    group_code: str = Field(..., min_length=1, max_length=96)
    position_code: str = Field(..., min_length=1, max_length=120)
    sort_order: int = Field(default=100, ge=0)
    position_source: str = Field(default="manual", min_length=1, max_length=32)
    is_featured: bool = False
    visible_from: datetime | None = None
    visible_until: datetime | None = None
    is_active: bool = True


class BackofficeOfferPositionContract(BaseModel):
    id: int
    position_code: str
    group_id: int
    group_code: str
    offer_id: int
    offer_code: str
    sort_order: int
    position_source: str
    is_featured: bool
    visible_from: datetime | None
    visible_until: datetime | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class BackofficeOfferPublishCheckResponse(BaseModel):
    offer_code: str
    can_publish: bool
    blocking_reasons: list[str]
    has_component: bool
    has_active_price: bool
    has_section_position: bool
    has_title: bool
    has_image: bool
    is_visible: bool
    is_sellable: bool
