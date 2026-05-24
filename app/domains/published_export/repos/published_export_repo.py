"""Backoffice published export repositories."""

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.domains.listing.models.listing import (
    ProductListingConfig,
    ProductListingContent,
    ProductListingMedia,
    SkuListingConfig,
    StorefrontCategory,
    StorefrontCategoryBinding,
)
from app.domains.pms_projection.models.pms_projection import (
    PmsBarcodeProjection,
    PmsBrandProfileProjection,
    PmsDisplayCategoryProjection,
    PmsItemAssetProjection,
    PmsItemContentProjection,
    PmsItemDisplayCategoryBindingProjection,
    PmsProductProjection,
    PmsSkuCodeProjection,
    PmsUnitProjection,
)
from app.domains.pricing.models.price_config import PriceConfig
from app.domains.promotions.models.promotion import Coupon, Promotion
from app.domains.publish.models.publish_version import PublishVersion


def get_publish_version(
    session: Session,
    publish_version: str | None,
    publish_scopes: tuple[str, ...],
) -> PublishVersion | None:
    if publish_version is not None:
        statement = select(PublishVersion).where(PublishVersion.publish_version == publish_version)
        return session.scalar(statement)

    statement = (
        select(PublishVersion)
        .where(PublishVersion.status == "published")
        .where(PublishVersion.publish_scope.in_((*publish_scopes, "all")))
        .order_by(PublishVersion.published_at.desc().nullslast(), PublishVersion.id.desc())
        .limit(1)
    )
    return session.scalar(statement)


def list_published_product_export_rows(
    session: Session,
) -> list[
    tuple[
        ProductListingConfig,
        ProductListingContent | None,
        ProductListingMedia | None,
        PmsProductProjection,
        StorefrontCategory | None,
        PmsItemContentProjection | None,
        PmsItemAssetProjection | None,
        PmsDisplayCategoryProjection | None,
        PmsBrandProfileProjection | None,
    ]
]:
    statement = (
        select(
            ProductListingConfig,
            ProductListingContent,
            ProductListingMedia,
            PmsProductProjection,
            StorefrontCategory,
            PmsItemContentProjection,
            PmsItemAssetProjection,
            PmsDisplayCategoryProjection,
            PmsBrandProfileProjection,
        )
        .join(
            PmsProductProjection,
            PmsProductProjection.pms_item_id == ProductListingConfig.pms_item_id,
        )
        .outerjoin(
            ProductListingContent,
            ProductListingContent.product_listing_config_id == ProductListingConfig.id,
        )
        .outerjoin(
            ProductListingMedia,
            and_(
                ProductListingMedia.product_listing_config_id == ProductListingConfig.id,
                ProductListingMedia.usage_type == "cover",
                ProductListingMedia.is_primary.is_(True),
                ProductListingMedia.status == "active",
            ),
        )
        .outerjoin(
            StorefrontCategoryBinding,
            and_(
                StorefrontCategoryBinding.product_listing_config_id == ProductListingConfig.id,
                StorefrontCategoryBinding.is_primary.is_(True),
            ),
        )
        .outerjoin(
            StorefrontCategory,
            StorefrontCategory.id == StorefrontCategoryBinding.storefront_category_id,
        )
        .outerjoin(
            PmsItemContentProjection,
            and_(
                PmsItemContentProjection.pms_item_id == PmsProductProjection.pms_item_id,
                PmsItemContentProjection.status == "active",
            ),
        )
        .outerjoin(
            PmsItemAssetProjection,
            and_(
                PmsItemAssetProjection.pms_item_id == PmsProductProjection.pms_item_id,
                PmsItemAssetProjection.usage_type == "main",
                PmsItemAssetProjection.is_primary.is_(True),
                PmsItemAssetProjection.status == "active",
            ),
        )
        .outerjoin(
            PmsItemDisplayCategoryBindingProjection,
            and_(
                PmsItemDisplayCategoryBindingProjection.pms_item_id
                == PmsProductProjection.pms_item_id,
                PmsItemDisplayCategoryBindingProjection.is_primary.is_(True),
            ),
        )
        .outerjoin(
            PmsDisplayCategoryProjection,
            and_(
                PmsDisplayCategoryProjection.pms_display_category_id
                == PmsItemDisplayCategoryBindingProjection.pms_display_category_id,
                PmsDisplayCategoryProjection.is_active.is_(True),
            ),
        )
        .outerjoin(
            PmsBrandProfileProjection,
            and_(
                PmsBrandProfileProjection.brand_id == PmsProductProjection.brand_id,
                PmsBrandProfileProjection.status == "active",
            ),
        )
        .order_by(ProductListingConfig.sort_order, ProductListingConfig.id)
    )
    return list(session.execute(statement).all())


def list_published_sku_export_rows(
    session: Session,
) -> list[
    tuple[
        SkuListingConfig,
        ProductListingConfig,
        PmsSkuCodeProjection,
        PmsUnitProjection,
        PmsBarcodeProjection | None,
    ]
]:
    statement = (
        select(
            SkuListingConfig,
            ProductListingConfig,
            PmsSkuCodeProjection,
            PmsUnitProjection,
            PmsBarcodeProjection,
        )
        .join(
            ProductListingConfig,
            ProductListingConfig.id == SkuListingConfig.product_listing_config_id,
        )
        .join(
            PmsSkuCodeProjection,
            PmsSkuCodeProjection.pms_sku_code_id == SkuListingConfig.pms_sku_code_id,
        )
        .join(
            PmsUnitProjection,
            PmsUnitProjection.pms_item_uom_id == SkuListingConfig.pms_item_uom_id,
        )
        .outerjoin(
            PmsBarcodeProjection,
            PmsBarcodeProjection.pms_barcode_id == SkuListingConfig.pms_barcode_id,
        )
        .order_by(
            ProductListingConfig.sort_order,
            ProductListingConfig.id,
            SkuListingConfig.sort_order,
            SkuListingConfig.id,
        )
    )
    return list(session.execute(statement).all())


def list_published_price_export_rows(
    session: Session,
) -> list[tuple[PriceConfig, SkuListingConfig, PmsSkuCodeProjection]]:
    statement = (
        select(PriceConfig, SkuListingConfig, PmsSkuCodeProjection)
        .join(SkuListingConfig, SkuListingConfig.id == PriceConfig.sku_listing_config_id)
        .join(
            PmsSkuCodeProjection,
            PmsSkuCodeProjection.pms_sku_code_id == SkuListingConfig.pms_sku_code_id,
        )
        .order_by(PriceConfig.priority, PriceConfig.id)
    )
    return list(session.execute(statement).all())


def list_published_promotion_export_rows(session: Session) -> list[Promotion]:
    statement = select(Promotion).order_by(Promotion.priority, Promotion.id)
    return list(session.scalars(statement).all())


def list_published_coupon_export_rows(session: Session) -> list[tuple[Coupon, Promotion]]:
    statement = (
        select(Coupon, Promotion)
        .join(Promotion, Promotion.id == Coupon.promotion_id)
        .order_by(Coupon.id)
    )
    return list(session.execute(statement).all())
