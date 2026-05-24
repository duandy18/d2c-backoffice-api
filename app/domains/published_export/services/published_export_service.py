"""Backoffice read-v1 published export services."""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.domains.listing.models.listing import (
    ProductListingConfig,
    ProductListingContent,
    ProductListingMedia,
    SkuListingConfig,
    StorefrontCategory,
)
from app.domains.pms_projection.models.pms_projection import (
    PmsBarcodeProjection,
    PmsBrandProfileProjection,
    PmsDisplayCategoryProjection,
    PmsItemAssetProjection,
    PmsItemContentProjection,
    PmsProductProjection,
    PmsSkuCodeProjection,
    PmsUnitProjection,
)
from app.domains.pricing.models.price_config import PriceConfig
from app.domains.promotions.models.promotion import Coupon, Promotion
from app.domains.publish.models.publish_version import PublishVersion
from app.domains.published_export.contracts.published_export_contract import (
    PublishedCatalogExportResponse,
    PublishedCouponExport,
    PublishedCouponsExportResponse,
    PublishedExportHealthResponse,
    PublishedPriceExport,
    PublishedPricesExportResponse,
    PublishedProductExport,
    PublishedPromotionExport,
    PublishedPromotionsExportResponse,
    PublishedSkuExport,
)
from app.domains.published_export.repos.published_export_repo import (
    get_publish_version,
    list_published_coupon_export_rows,
    list_published_price_export_rows,
    list_published_product_export_rows,
    list_published_promotion_export_rows,
    list_published_sku_export_rows,
)


def get_published_export_health() -> PublishedExportHealthResponse:
    return PublishedExportHealthResponse(
        status="ok",
        module="published_export",
        surface="service_read_v1",
    )


def _published_at(version: PublishVersion) -> datetime:
    return version.published_at or version.created_at or datetime.now(UTC)


def _empty_catalog(version: PublishVersion | None) -> PublishedCatalogExportResponse:
    return PublishedCatalogExportResponse(
        publish_version=version.publish_version if version else None,
        product_count=0,
        sku_count=0,
        products=[],
        skus=[],
    )


def _empty_prices(version: PublishVersion | None) -> PublishedPricesExportResponse:
    return PublishedPricesExportResponse(
        publish_version=version.publish_version if version else None,
        count=0,
        prices=[],
    )


def _empty_promotions(version: PublishVersion | None) -> PublishedPromotionsExportResponse:
    return PublishedPromotionsExportResponse(
        publish_version=version.publish_version if version else None,
        count=0,
        promotions=[],
    )


def _empty_coupons(version: PublishVersion | None) -> PublishedCouponsExportResponse:
    return PublishedCouponsExportResponse(
        publish_version=version.publish_version if version else None,
        count=0,
        coupons=[],
    )


def _clean_text(value: str | None) -> str | None:
    if value is None:
        return None

    text = value.strip()
    return text or None


def _first_text(*values: str | None) -> str | None:
    for value in values:
        cleaned = _clean_text(value)
        if cleaned is not None:
            return cleaned

    return None


def _product_raw_payload(
    listing: ProductListingConfig,
    content: ProductListingContent | None,
    primary_media: ProductListingMedia | None,
    pms_product: PmsProductProjection,
    category: StorefrontCategory | None,
    pms_content: PmsItemContentProjection | None,
    pms_primary_asset: PmsItemAssetProjection | None,
    pms_display_category: PmsDisplayCategoryProjection | None,
    pms_brand_profile: PmsBrandProfileProjection | None,
) -> dict[str, Any]:
    return {
        "source": "d2c-backoffice-api",
        "source_product_listing_config_id": listing.id,
        "source_product_listing_content_id": content.id if content else None,
        "source_primary_media_id": primary_media.id if primary_media else None,
        "pms_item_id": pms_product.pms_item_id,
        "pms_sku": pms_product.pms_sku,
        "pms_item_content_id": pms_content.pms_content_id if pms_content else None,
        "pms_item_asset_id": pms_primary_asset.pms_asset_id if pms_primary_asset else None,
        "pms_display_category_id": (
            pms_display_category.pms_display_category_id if pms_display_category else None
        ),
        "pms_brand_profile_id": pms_brand_profile.pms_profile_id if pms_brand_profile else None,
        "pms_category_code": pms_product.category_code,
        "pms_category_name": pms_product.category_name,
        "storefront_category_code": category.category_code if category else None,
    }


def _build_product(
    publish_version: str,
    published_at: datetime,
    listing: ProductListingConfig,
    content: ProductListingContent | None,
    primary_media: ProductListingMedia | None,
    pms_product: PmsProductProjection,
    category: StorefrontCategory | None,
    pms_content: PmsItemContentProjection | None,
    pms_primary_asset: PmsItemAssetProjection | None,
    pms_display_category: PmsDisplayCategoryProjection | None,
    pms_brand_profile: PmsBrandProfileProjection | None,
) -> PublishedProductExport:
    active_content = content if content is not None and content.content_status == "active" else None

    category_code = _first_text(
        category.category_code if category else None,
        pms_display_category.category_code if pms_display_category else None,
        pms_product.category_code,
    )
    category_name = _first_text(
        category.category_name if category else None,
        pms_display_category.display_name if pms_display_category else None,
        pms_display_category.category_name if pms_display_category else None,
        pms_product.category_name,
    )
    display_name = _first_text(
        active_content.display_title if active_content else None,
        pms_content.base_title if pms_content else None,
        pms_product.item_name,
    )
    description = _first_text(
        active_content.detail_description if active_content else None,
        active_content.short_description if active_content else None,
        pms_content.base_description if pms_content else None,
        pms_content.short_description if pms_content else None,
    )
    image_url = _first_text(
        primary_media.url if primary_media else None,
        pms_primary_asset.url if pms_primary_asset else None,
    )
    brand_name = _first_text(
        pms_brand_profile.display_name if pms_brand_profile else None,
        pms_brand_profile.official_name if pms_brand_profile else None,
        pms_product.brand_name,
    )

    return PublishedProductExport(
        publish_version=publish_version,
        pms_item_id=pms_product.pms_item_id,
        pms_sku=pms_product.pms_sku,
        product_code=listing.listing_code,
        product_name=pms_product.item_name,
        display_name=display_name or pms_product.item_name,
        description=description,
        image_url=image_url,
        category_code=category_code,
        category_name=category_name,
        brand_code=pms_product.brand_code,
        brand_name=brand_name,
        display_status=listing.display_status,
        sell_status=listing.sell_status,
        sort_order=listing.sort_order,
        visible_from=listing.visible_from,
        visible_until=listing.visible_until,
        published_at=published_at,
        source_product_id=listing.id,
        source_updated_at=listing.updated_at,
        raw_payload=_product_raw_payload(
            listing,
            content,
            primary_media,
            pms_product,
            category,
            pms_content,
            pms_primary_asset,
            pms_display_category,
            pms_brand_profile,
        ),
    )


def _sku_raw_payload(
    sku_listing: SkuListingConfig,
    sku_code: PmsSkuCodeProjection,
    unit: PmsUnitProjection,
    barcode: PmsBarcodeProjection | None,
) -> dict[str, Any]:
    return {
        "source": "d2c-backoffice-api",
        "source_sku_listing_config_id": sku_listing.id,
        "pms_sku_code_id": sku_code.pms_sku_code_id,
        "pms_item_uom_id": unit.pms_item_uom_id,
        "pms_barcode_id": barcode.pms_barcode_id if barcode else None,
    }


def _build_sku(
    publish_version: str,
    published_at: datetime,
    sku_listing: SkuListingConfig,
    product_listing: ProductListingConfig,
    sku_code: PmsSkuCodeProjection,
    unit: PmsUnitProjection,
    barcode: PmsBarcodeProjection | None,
) -> PublishedSkuExport:
    is_sellable = (
        sku_listing.listing_status in {"ready", "published"}
        and sku_listing.display_status == "visible"
        and sku_listing.sell_status == "sellable"
    )

    return PublishedSkuExport(
        publish_version=publish_version,
        product_code=product_listing.listing_code,
        sku_code=sku_code.sku_code,
        sku_name=sku_code.item_name,
        display_sku_name=sku_listing.sku_display_name,
        sales_unit_code=unit.uom,
        sales_unit_name=unit.display_name or unit.uom_name,
        barcode=barcode.barcode if barcode else None,
        spec_text=sku_listing.sku_spec_text,
        is_sellable=is_sellable,
        sort_order=sku_listing.sort_order,
        published_at=published_at,
        source_sku_id=sku_listing.id,
        source_updated_at=sku_listing.updated_at,
        raw_payload=_sku_raw_payload(sku_listing, sku_code, unit, barcode),
    )


def get_published_catalog_export(
    session: Session,
    publish_version: str | None,
) -> PublishedCatalogExportResponse:
    version = get_publish_version(session, publish_version, ("catalog",))
    if version is None:
        return _empty_catalog(version)

    resolved_published_at = _published_at(version)
    resolved_version = version.publish_version

    products = [
        _build_product(
            resolved_version,
            resolved_published_at,
            listing,
            content,
            primary_media,
            pms_product,
            category,
            pms_content,
            pms_primary_asset,
            pms_display_category,
            pms_brand_profile,
        )
        for (
            listing,
            content,
            primary_media,
            pms_product,
            category,
            pms_content,
            pms_primary_asset,
            pms_display_category,
            pms_brand_profile,
        ) in list_published_product_export_rows(session)
    ]

    skus = [
        _build_sku(
            resolved_version,
            resolved_published_at,
            sku_listing,
            product_listing,
            sku_code,
            unit,
            barcode,
        )
        for sku_listing, product_listing, sku_code, unit, barcode in list_published_sku_export_rows(
            session
        )
    ]

    return PublishedCatalogExportResponse(
        publish_version=resolved_version,
        product_count=len(products),
        sku_count=len(skus),
        products=products,
        skus=skus,
    )


def _price_raw_payload(price_config: PriceConfig) -> dict[str, Any]:
    return {
        "source": "d2c-backoffice-api",
        "source_price_config_id": price_config.id,
        "price_config_code": price_config.price_config_code,
    }


def _build_price(
    publish_version: str,
    published_at: datetime,
    price_config: PriceConfig,
    sku_code: PmsSkuCodeProjection,
) -> PublishedPriceExport:
    return PublishedPriceExport(
        publish_version=publish_version,
        price_list_code=price_config.price_config_code,
        channel=price_config.channel,
        sku_code=sku_code.sku_code,
        currency=price_config.currency,
        price_cents=price_config.price_cents,
        compare_at_price_cents=price_config.compare_at_price_cents,
        effective_from=price_config.effective_from,
        effective_until=price_config.effective_until,
        is_active=price_config.is_active,
        priority=price_config.priority,
        published_at=published_at,
        source_price_id=price_config.id,
        source_updated_at=price_config.updated_at,
        raw_payload=_price_raw_payload(price_config),
    )


def get_published_prices_export(
    session: Session,
    publish_version: str | None,
) -> PublishedPricesExportResponse:
    version = get_publish_version(session, publish_version, ("price", "prices"))
    if version is None:
        return _empty_prices(version)

    resolved_published_at = _published_at(version)
    resolved_version = version.publish_version

    prices = [
        _build_price(resolved_version, resolved_published_at, price_config, sku_code)
        for price_config, _sku_listing, sku_code in list_published_price_export_rows(session)
    ]

    return PublishedPricesExportResponse(
        publish_version=resolved_version,
        count=len(prices),
        prices=prices,
    )


def _promotion_raw_payload(promotion: Promotion) -> dict[str, Any]:
    return {
        "source": "d2c-backoffice-api",
        "source_promotion_id": promotion.id,
        "status": promotion.status,
    }


def _build_promotion(
    publish_version: str,
    published_at: datetime,
    promotion: Promotion,
) -> PublishedPromotionExport:
    return PublishedPromotionExport(
        publish_version=publish_version,
        promotion_code=promotion.promotion_code,
        promotion_name=promotion.name,
        promotion_type=promotion.promotion_type,
        discount_type=promotion.discount_type,
        discount_value=promotion.discount_value,
        scope_type=promotion.scope_type,
        min_order_amount_cents=promotion.min_order_amount_cents,
        max_discount_cents=promotion.max_discount_cents,
        currency=promotion.currency,
        starts_at=promotion.starts_at,
        ends_at=promotion.ends_at,
        priority=promotion.priority,
        stackable=promotion.stackable,
        is_active=promotion.is_active,
        published_at=published_at,
        source_promotion_id=promotion.id,
        source_updated_at=promotion.updated_at,
        raw_payload=_promotion_raw_payload(promotion),
    )


def get_published_promotions_export(
    session: Session,
    publish_version: str | None,
) -> PublishedPromotionsExportResponse:
    version = get_publish_version(session, publish_version, ("promotion", "promotions"))
    if version is None:
        return _empty_promotions(version)

    resolved_published_at = _published_at(version)
    resolved_version = version.publish_version

    promotions = [
        _build_promotion(resolved_version, resolved_published_at, promotion)
        for promotion in list_published_promotion_export_rows(session)
    ]

    return PublishedPromotionsExportResponse(
        publish_version=resolved_version,
        count=len(promotions),
        promotions=promotions,
    )


def _coupon_raw_payload(coupon: Coupon, promotion: Promotion) -> dict[str, Any]:
    return {
        "source": "d2c-backoffice-api",
        "source_coupon_id": coupon.id,
        "source_promotion_id": promotion.id,
        "status": coupon.status,
    }


def _build_coupon(
    publish_version: str,
    published_at: datetime,
    coupon: Coupon,
    promotion: Promotion,
) -> PublishedCouponExport:
    return PublishedCouponExport(
        publish_version=publish_version,
        coupon_code=coupon.coupon_code,
        coupon_name=coupon.name,
        promotion_code=promotion.promotion_code,
        coupon_type=coupon.coupon_type,
        total_limit=coupon.total_limit,
        per_customer_limit=coupon.per_customer_limit,
        starts_at=coupon.starts_at,
        ends_at=coupon.ends_at,
        is_active=coupon.is_active,
        published_at=published_at,
        source_coupon_id=coupon.id,
        source_updated_at=coupon.updated_at,
        raw_payload=_coupon_raw_payload(coupon, promotion),
    )


def get_published_coupons_export(
    session: Session,
    publish_version: str | None,
) -> PublishedCouponsExportResponse:
    version = get_publish_version(session, publish_version, ("coupon", "coupons"))
    if version is None:
        return _empty_coupons(version)

    resolved_published_at = _published_at(version)
    resolved_version = version.publish_version

    coupons = [
        _build_coupon(resolved_version, resolved_published_at, coupon, promotion)
        for coupon, promotion in list_published_coupon_export_rows(session)
    ]

    return PublishedCouponsExportResponse(
        publish_version=resolved_version,
        count=len(coupons),
        coupons=coupons,
    )
