"""Backoffice pricing API contracts."""

from datetime import datetime

from pydantic import BaseModel, Field


class BackofficePricingHealthResponse(BaseModel):
    status: str
    module: str
    surface: str


class PriceConfigContract(BaseModel):
    id: int
    sku_listing_config_id: int
    price_config_code: str
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


class PriceConfigsResponse(BaseModel):
    count: int = Field(..., ge=0)
    price_configs: list[PriceConfigContract]
