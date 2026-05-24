"""Backoffice listing services."""

from sqlalchemy.orm import Session

from app.domains.listing.contracts.listing_contract import (
    BackofficeListingHealthResponse,
    ProductListingConfigContract,
    ProductListingConfigsResponse,
    ProductListingContentContract,
    ProductListingMediaContract,
    SkuListingConfigContract,
    SkuListingConfigsResponse,
)
from app.domains.listing.models.listing import (
    ProductListingConfig,
    ProductListingContent,
    ProductListingMedia,
    SkuListingConfig,
)
from app.domains.listing.repos.listing_repo import (
    list_product_listing_configs,
    list_product_listing_contents,
    list_product_listing_media,
    list_sku_listing_configs,
)


def get_backoffice_listing_health() -> BackofficeListingHealthResponse:
    return BackofficeListingHealthResponse(
        status="ok",
        module="backoffice_listing",
        surface="merchant_management",
    )


def _build_content(row: ProductListingContent | None) -> ProductListingContentContract | None:
    if row is None:
        return None

    return ProductListingContentContract(
        id=row.id,
        product_listing_config_id=row.product_listing_config_id,
        display_title=row.display_title,
        subtitle=row.subtitle,
        short_description=row.short_description,
        detail_description=row.detail_description,
        seo_title=row.seo_title,
        seo_description=row.seo_description,
        selling_points=row.selling_points,
        content_status=row.content_status,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _build_media(row: ProductListingMedia) -> ProductListingMediaContract:
    return ProductListingMediaContract(
        id=row.id,
        product_listing_config_id=row.product_listing_config_id,
        media_type=row.media_type,
        source_type=row.source_type,
        pms_asset_id=row.pms_asset_id,
        object_key=row.object_key,
        url=row.url,
        alt_text=row.alt_text,
        usage_type=row.usage_type,
        sort_order=row.sort_order,
        is_primary=row.is_primary,
        status=row.status,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _build_product(
    row: ProductListingConfig,
    content: ProductListingContent | None,
    media_rows: list[ProductListingMedia],
) -> ProductListingConfigContract:
    return ProductListingConfigContract(
        id=row.id,
        pms_item_id=row.pms_item_id,
        pms_sku=row.pms_sku,
        listing_code=row.listing_code,
        listing_status=row.listing_status,
        display_status=row.display_status,
        sell_status=row.sell_status,
        sort_order=row.sort_order,
        visible_from=row.visible_from,
        visible_until=row.visible_until,
        created_at=row.created_at,
        updated_at=row.updated_at,
        content=_build_content(content),
        media=[_build_media(media) for media in media_rows],
    )


def get_product_listing_configs(session: Session) -> ProductListingConfigsResponse:
    products = list_product_listing_configs(session)
    contents = {
        row.product_listing_config_id: row for row in list_product_listing_contents(session)
    }
    media_by_product: dict[int, list[ProductListingMedia]] = {}
    for media in list_product_listing_media(session):
        media_by_product.setdefault(media.product_listing_config_id, []).append(media)

    rows = [
        _build_product(
            product,
            contents.get(product.id),
            media_by_product.get(product.id, []),
        )
        for product in products
    ]
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
