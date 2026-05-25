"""Backoffice PromotionRule repositories."""

from sqlalchemy import or_, select, true
from sqlalchemy.orm import Session

from app.domains.groups.models.group import Group
from app.domains.offers.models.offer import Offer, OfferPosition, OfferPrice
from app.domains.promotions.models.promotion_rule import Coupon, PromotionRule, PromotionTarget


def get_promotion_rule_by_code(
    session: Session,
    promotion_code: str,
) -> PromotionRule | None:
    statement = select(PromotionRule).where(PromotionRule.promotion_code == promotion_code)
    return session.scalar(statement)


def list_promotion_rules(session: Session) -> list[PromotionRule]:
    statement = select(PromotionRule).order_by(
        PromotionRule.is_active.desc(),
        PromotionRule.status,
        PromotionRule.priority,
        PromotionRule.id.desc(),
    )
    return list(session.scalars(statement).all())


def create_promotion_rule(
    session: Session,
    rule: PromotionRule,
) -> PromotionRule:
    session.add(rule)
    session.flush()
    return rule


def create_promotion_target(
    session: Session,
    target: PromotionTarget,
) -> PromotionTarget:
    session.add(target)
    session.flush()
    return target


def list_promotion_target_rows(
    session: Session,
) -> list[tuple[PromotionTarget, PromotionRule]]:
    statement = (
        select(PromotionTarget, PromotionRule)
        .join(PromotionRule, PromotionRule.id == PromotionTarget.promotion_rule_id)
        .order_by(PromotionTarget.id.desc())
    )
    return list(session.execute(statement).all())


def list_promotion_target_rows_for_rule(
    session: Session,
    promotion_rule_id: int,
) -> list[PromotionTarget]:
    statement = select(PromotionTarget).where(
        PromotionTarget.promotion_rule_id == promotion_rule_id
    )
    return list(session.scalars(statement).all())


def get_coupon_by_code(
    session: Session,
    coupon_code: str,
) -> Coupon | None:
    statement = select(Coupon).where(Coupon.coupon_code == coupon_code)
    return session.scalar(statement)


def create_coupon(
    session: Session,
    coupon: Coupon,
) -> Coupon:
    session.add(coupon)
    session.flush()
    return coupon


def get_coupon_row_by_code(
    session: Session,
    coupon_code: str,
) -> tuple[Coupon, PromotionRule] | None:
    statement = (
        select(Coupon, PromotionRule)
        .join(PromotionRule, PromotionRule.id == Coupon.promotion_rule_id)
        .where(Coupon.coupon_code == coupon_code)
    )
    return session.execute(statement).first()


def list_coupon_rows(session: Session) -> list[tuple[Coupon, PromotionRule]]:
    statement = (
        select(Coupon, PromotionRule)
        .join(PromotionRule, PromotionRule.id == Coupon.promotion_rule_id)
        .order_by(Coupon.id.desc())
    )
    return list(session.execute(statement).all())


def list_active_price_rows_for_preview(
    session: Session,
    rule: PromotionRule,
) -> list[tuple[Offer, OfferPrice, Group | None]]:
    target_rows = list_promotion_target_rows_for_rule(session, rule.id)
    if not target_rows:
        return []

    clauses = []
    for target in target_rows:
        if target.target_type == "all_store":
            clauses.append(true())
        elif target.target_type == "offer" and target.target_code:
            clauses.append(Offer.offer_code == target.target_code)
        elif target.target_type == "group" and target.target_code:
            clauses.append(Group.group_code == target.target_code)
        elif target.target_type == "offer_type" and target.target_code:
            clauses.append(Offer.offer_type == target.target_code)

    if not clauses:
        return []

    statement = (
        select(Offer, OfferPrice, Group)
        .join(OfferPrice, OfferPrice.offer_id == Offer.id)
        .outerjoin(OfferPosition, OfferPosition.offer_id == Offer.id)
        .outerjoin(Group, Group.id == OfferPosition.group_id)
        .where(OfferPrice.is_active.is_(True))
        .where(or_(*clauses))
        .order_by(Offer.sort_order, Offer.id, OfferPrice.priority, OfferPrice.id)
    )
    return list(session.execute(statement).all())
