"""Backoffice read-v1 published export services."""

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.domains.promotions.models.promotion_rule import Coupon, PromotionRule
from app.domains.publish.models.publish_version import PublishVersion
from app.domains.published_export.contracts.published_export_contract import (
    PublishedCouponExport,
    PublishedCouponsExportResponse,
    PublishedExportHealthResponse,
    PublishedPromotionExport,
    PublishedPromotionsExportResponse,
)
from app.domains.published_export.repos.published_export_repo import (
    get_publish_version,
    list_published_coupon_export_rows,
    list_published_promotion_export_rows,
)


def get_published_export_health() -> PublishedExportHealthResponse:
    return PublishedExportHealthResponse(
        status="ok",
        module="published_export",
        surface="service_read_v1",
    )


def _published_at(version: PublishVersion) -> datetime:
    return version.published_at or version.created_at or datetime.now(UTC)


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


def _promotion_raw_payload(promotion: PromotionRule) -> dict[str, object]:
    return {
        "source": "d2c-backoffice-api",
        "source_promotion_rule_id": promotion.id,
        "status": promotion.status,
    }


def _build_promotion(
    publish_version: str,
    published_at: datetime,
    promotion: PromotionRule,
) -> PublishedPromotionExport:
    return PublishedPromotionExport(
        publish_version=publish_version,
        promotion_code=promotion.promotion_code,
        promotion_name=promotion.promotion_name,
        promotion_type=promotion.promotion_type,
        discount_type=promotion.discount_type,
        discount_value=promotion.discount_value,
        scope_type="targets",
        min_order_amount_cents=promotion.threshold_amount_cents,
        max_discount_cents=promotion.max_discount_cents,
        currency=promotion.currency,
        starts_at=promotion.starts_at,
        ends_at=promotion.ends_at,
        priority=promotion.priority,
        stackable=promotion.stackable,
        is_active=promotion.is_active,
        published_at=published_at,
        source_promotion_rule_id=promotion.id,
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


def _coupon_raw_payload(coupon: Coupon, promotion: PromotionRule) -> dict[str, object]:
    return {
        "source": "d2c-backoffice-api",
        "source_coupon_id": coupon.id,
        "source_promotion_rule_id": promotion.id,
        "status": coupon.status,
    }


def _build_coupon(
    publish_version: str,
    published_at: datetime,
    coupon: Coupon,
    promotion: PromotionRule,
) -> PublishedCouponExport:
    return PublishedCouponExport(
        publish_version=publish_version,
        coupon_code=coupon.coupon_code,
        coupon_name=coupon.coupon_name,
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
