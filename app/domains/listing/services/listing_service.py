"""Backoffice listing services."""

from sqlalchemy.orm import Session

from app.domains.listing.contracts.listing_contract import (
    BackofficeListingHealthResponse,
    ProductListingConfigContract,
    ProductListingConfigsResponse,
    SkuListingConfigContract,
    SkuListingConfigsResponse,
)
from app.domains.listing.models.listing import ProductListingConfig, SkuListingConfig
from app.domains.listing.repos.listing_repo import (
    list_product_listing_configs,
    list_sku_listing_configs,
)


def get_backoffice_listing_health() -> BackofficeListingHealthResponse:
    return BackofficeListingHealthResponse(
        status="ok",
        module="backoffice_listing",
        surface="merchant_management",
    )


def _build_product(row: ProductListingConfig) -> ProductListingConfigContract:
    return ProductListingConfigContract(
        id=row.id,
        pms_item_id=row.pms_item_id,
        pms_sku=row.pms_sku,
        listing_code=row.listing_code,
        display_name=row.display_name,
        subtitle=row.subtitle,
        description_override=row.description_override,
        cover_image_url=row.cover_image_url,
        listing_status=row.listing_status,
        display_status=row.display_status,
        sell_status=row.sell_status,
        sort_order=row.sort_order,
        visible_from=row.visible_from,
        visible_until=row.visible_until,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def get_product_listing_configs(session: Session) -> ProductListingConfigsResponse:
    rows = [_build_product(row) for row in list_product_listing_configs(session)]
    return ProductListingConfigsResponse(count=len(rows), products=rows)


def _build_sku(row: SkuListingConfig) -> SkuListingConfigContract:
    return SkuListingConfigContract(
        id=row.id,
        product_listing_config_id=row.product_listing_config_id,
        pms_item_id=row.pms_item_id,
        pms_sku_code_id=row.pms_sku_code_id,
        pms_item_uom_id=row.pms_item_uom_id,
        pms_barcode_id=row.pms_barcode_id,
        sku_display_name=row.sku_display_name,
        sku_spec_text=row.sku_spec_text,
        sku_image_url=row.sku_image_url,
        listing_status=row.listing_status,
        display_status=row.display_status,
        sell_status=row.sell_status,
        sort_order=row.sort_order,
        visible_from=row.visible_from,
        visible_until=row.visible_until,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def get_sku_listing_configs(session: Session) -> SkuListingConfigsResponse:
    rows = [_build_sku(row) for row in list_sku_listing_configs(session)]
    return SkuListingConfigsResponse(count=len(rows), skus=rows)
