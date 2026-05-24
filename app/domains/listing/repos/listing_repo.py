"""Backoffice listing repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.listing.models.listing import ProductListingConfig, SkuListingConfig


def list_product_listing_configs(session: Session) -> list[ProductListingConfig]:
    statement = select(ProductListingConfig).order_by(
        ProductListingConfig.sort_order,
        ProductListingConfig.id,
    )
    return list(session.scalars(statement).all())


def list_sku_listing_configs(session: Session) -> list[SkuListingConfig]:
    statement = select(SkuListingConfig).order_by(
        SkuListingConfig.product_listing_config_id,
        SkuListingConfig.sort_order,
        SkuListingConfig.id,
    )
    return list(session.scalars(statement).all())
