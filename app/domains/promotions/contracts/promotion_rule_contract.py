"""Backoffice PromotionRule API contracts."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

PromotionType = Literal[
    "offer_discount",
    "group_discount",
    "order_discount",
    "coupon_discount",
]
DiscountType = Literal[
    "percentage",
    "amount_off",
    "threshold_amount",
    "fixed_price",
]
PromotionTargetType = Literal["all_store", "group", "offer", "offer_type"]
CouponType = Literal["public_code"]


class BackofficePromotionRuleHealthResponse(BaseModel):
    status: str
    module: str
    surface: str


class BackofficePromotionRuleCreateRequest(BaseModel):
    promotion_code: str = Field(..., min_length=1, max_length=64)
    promotion_name: str = Field(..., min_length=1, max_length=160)
    description: str | None = None
    promotion_type: PromotionType
    discount_type: DiscountType
    discount_value: int = Field(..., ge=1)
    threshold_amount_cents: int | None = Field(default=None, ge=0)
    max_discount_cents: int | None = Field(default=None, ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    priority: int = Field(default=100, ge=0)
    stackable: bool = False
    display_badge: str | None = Field(default=None, max_length=64)


class BackofficePromotionRule(BaseModel):
    id: int
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
    status: str
    priority: int
    stackable: bool
    is_active: bool
    display_badge: str | None
    created_at: datetime
    updated_at: datetime


class BackofficePromotionRulesResponse(BaseModel):
    count: int = Field(..., ge=0)
    promotion_rules: list[BackofficePromotionRule]


class BackofficePromotionTargetCreateRequest(BaseModel):
    target_type: PromotionTargetType
    target_id: int | None = None
    target_code: str | None = Field(default=None, max_length=96)


class BackofficePromotionTarget(BaseModel):
    id: int
    promotion_rule_id: int
    promotion_code: str
    target_type: str
    target_id: int | None
    target_code: str | None
    created_at: datetime


class BackofficePromotionTargetsResponse(BaseModel):
    count: int = Field(..., ge=0)
    promotion_targets: list[BackofficePromotionTarget]


class BackofficeCouponCreateRequest(BaseModel):
    coupon_code: str = Field(..., min_length=1, max_length=64)
    coupon_name: str = Field(..., min_length=1, max_length=160)
    coupon_type: CouponType = "public_code"
    total_limit: int | None = Field(default=None, ge=1)
    per_customer_limit: int | None = Field(default=None, ge=1)
    starts_at: datetime | None = None
    ends_at: datetime | None = None


class BackofficeCoupon(BaseModel):
    id: int
    coupon_code: str
    coupon_name: str
    promotion_rule_id: int
    promotion_code: str
    coupon_type: str
    total_limit: int | None
    per_customer_limit: int | None
    starts_at: datetime | None
    ends_at: datetime | None
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class BackofficeCouponsResponse(BaseModel):
    count: int = Field(..., ge=0)
    coupons: list[BackofficeCoupon]


class BackofficePromotionPreviewOffer(BaseModel):
    offer_code: str
    title: str
    offer_type: str
    group_codes: list[str]
    base_price_cents: int
    final_price_cents: int
    discount_cents: int
    promotion_badges: list[str]


class BackofficePromotionPreviewResponse(BaseModel):
    promotion_code: str
    promotion_name: str
    matched_offer_count: int = Field(..., ge=0)
    offers: list[BackofficePromotionPreviewOffer]
    blocking_reasons: list[str]
