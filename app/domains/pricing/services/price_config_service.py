"""Backoffice pricing services."""

from sqlalchemy.orm import Session

from app.domains.pricing.contracts.price_config_contract import (
    BackofficePricingHealthResponse,
    PriceConfigContract,
    PriceConfigsResponse,
)
from app.domains.pricing.models.price_config import PriceConfig
from app.domains.pricing.repos.price_config_repo import list_price_configs


def get_backoffice_pricing_health() -> BackofficePricingHealthResponse:
    return BackofficePricingHealthResponse(
        status="ok",
        module="backoffice_pricing",
        surface="merchant_management",
    )


def _build_price_config(row: PriceConfig) -> PriceConfigContract:
    return PriceConfigContract(
        id=row.id,
        sku_listing_config_id=row.sku_listing_config_id,
        price_config_code=row.price_config_code,
        channel=row.channel,
        currency=row.currency,
        price_cents=row.price_cents,
        compare_at_price_cents=row.compare_at_price_cents,
        effective_from=row.effective_from,
        effective_until=row.effective_until,
        is_active=row.is_active,
        priority=row.priority,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def get_price_configs(session: Session) -> PriceConfigsResponse:
    rows = [_build_price_config(row) for row in list_price_configs(session)]
    return PriceConfigsResponse(count=len(rows), price_configs=rows)
