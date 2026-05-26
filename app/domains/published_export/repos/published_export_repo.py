"""Backoffice published export repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.promotions.models.promotion_rule import Coupon, PromotionRule
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


def list_published_promotion_export_rows(session: Session) -> list[PromotionRule]:
    statement = select(PromotionRule).order_by(PromotionRule.priority, PromotionRule.id)
    return list(session.scalars(statement).all())


def list_published_coupon_export_rows(session: Session) -> list[tuple[Coupon, PromotionRule]]:
    statement = (
        select(Coupon, PromotionRule)
        .join(PromotionRule, PromotionRule.id == Coupon.promotion_rule_id)
        .order_by(Coupon.id)
    )
    return list(session.execute(statement).all())
