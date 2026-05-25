"""Backoffice PromotionRule service."""

from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domains.promotions.contracts.promotion_rule_contract import (
    BackofficeCoupon,
    BackofficeCouponCreateRequest,
    BackofficeCouponsResponse,
    BackofficePromotionPreviewOffer,
    BackofficePromotionPreviewResponse,
    BackofficePromotionRule,
    BackofficePromotionRuleCreateRequest,
    BackofficePromotionRulesResponse,
    BackofficePromotionTarget,
    BackofficePromotionTargetCreateRequest,
    BackofficePromotionTargetsResponse,
)
from app.domains.promotions.models.promotion_rule import Coupon, PromotionRule, PromotionTarget
from app.domains.promotions.repos.promotion_rule_repo import (
    create_coupon,
    create_promotion_rule,
    create_promotion_target,
    get_coupon_by_code,
    get_coupon_row_by_code,
    get_promotion_rule_by_code,
    list_active_price_rows_for_preview,
    list_coupon_rows,
    list_promotion_rules,
    list_promotion_target_rows,
)


class BackofficePromotionRuleDuplicateCodeError(Exception):
    pass


class BackofficePromotionRuleInvalidRangeError(Exception):
    pass


class BackofficePromotionRuleNotFoundError(Exception):
    pass


class BackofficePromotionTargetInvalidError(Exception):
    pass


class BackofficePromotionTargetDuplicateError(Exception):
    pass


class BackofficeCouponDuplicateCodeError(Exception):
    pass


class BackofficeCouponInvalidRangeError(Exception):
    pass


class BackofficeCouponNotFoundError(Exception):
    pass


def _validate_range(start: datetime | None, end: datetime | None, error_code: str) -> None:
    if start is not None and end is not None and end <= start:
        raise BackofficePromotionRuleInvalidRangeError(error_code)


def _build_rule(rule: PromotionRule) -> BackofficePromotionRule:
    return BackofficePromotionRule(
        id=rule.id,
        promotion_code=rule.promotion_code,
        promotion_name=rule.promotion_name,
        description=rule.description,
        promotion_type=rule.promotion_type,
        discount_type=rule.discount_type,
        discount_value=rule.discount_value,
        threshold_amount_cents=rule.threshold_amount_cents,
        max_discount_cents=rule.max_discount_cents,
        currency=rule.currency,
        starts_at=rule.starts_at,
        ends_at=rule.ends_at,
        status=rule.status,
        priority=rule.priority,
        stackable=rule.stackable,
        is_active=rule.is_active,
        display_badge=rule.display_badge,
        created_at=rule.created_at,
        updated_at=rule.updated_at,
    )


def get_backoffice_promotion_rules(session: Session) -> BackofficePromotionRulesResponse:
    rules = [_build_rule(rule) for rule in list_promotion_rules(session)]
    return BackofficePromotionRulesResponse(count=len(rules), promotion_rules=rules)


def create_backoffice_promotion_rule(
    session: Session,
    payload: BackofficePromotionRuleCreateRequest,
) -> BackofficePromotionRule:
    _validate_range(payload.starts_at, payload.ends_at, "promotion_rule_effective_range_invalid")

    if get_promotion_rule_by_code(session, payload.promotion_code) is not None:
        raise BackofficePromotionRuleDuplicateCodeError("promotion_code_already_exists")

    rule = PromotionRule(
        promotion_code=payload.promotion_code,
        promotion_name=payload.promotion_name,
        description=payload.description,
        promotion_type=payload.promotion_type,
        discount_type=payload.discount_type,
        discount_value=payload.discount_value,
        threshold_amount_cents=payload.threshold_amount_cents,
        max_discount_cents=payload.max_discount_cents,
        currency=payload.currency.upper(),
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        status="draft",
        priority=payload.priority,
        stackable=payload.stackable,
        is_active=False,
        display_badge=payload.display_badge,
    )

    try:
        create_promotion_rule(session, rule)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise BackofficePromotionRuleDuplicateCodeError("promotion_code_already_exists") from exc

    return _build_rule(rule)


def _get_rule_or_raise(session: Session, promotion_code: str) -> PromotionRule:
    rule = get_promotion_rule_by_code(session, promotion_code)
    if rule is None:
        raise BackofficePromotionRuleNotFoundError("promotion_rule_not_found")
    return rule


def activate_backoffice_promotion_rule(
    session: Session,
    promotion_code: str,
) -> BackofficePromotionRule:
    rule = _get_rule_or_raise(session, promotion_code)
    now = datetime.now(UTC)
    rule.status = "active"
    rule.is_active = True
    rule.updated_at = now
    session.commit()
    return _build_rule(rule)


def deactivate_backoffice_promotion_rule(
    session: Session,
    promotion_code: str,
) -> BackofficePromotionRule:
    rule = _get_rule_or_raise(session, promotion_code)
    now = datetime.now(UTC)
    rule.status = "paused"
    rule.is_active = False
    rule.updated_at = now
    session.commit()
    return _build_rule(rule)


def _build_target(
    target: PromotionTarget,
    rule: PromotionRule,
) -> BackofficePromotionTarget:
    return BackofficePromotionTarget(
        id=target.id,
        promotion_rule_id=target.promotion_rule_id,
        promotion_code=rule.promotion_code,
        target_type=target.target_type,
        target_id=target.target_id,
        target_code=target.target_code,
        created_at=target.created_at,
    )


def get_backoffice_promotion_targets(session: Session) -> BackofficePromotionTargetsResponse:
    targets = [_build_target(target, rule) for target, rule in list_promotion_target_rows(session)]
    return BackofficePromotionTargetsResponse(count=len(targets), promotion_targets=targets)


def create_backoffice_promotion_target(
    session: Session,
    promotion_code: str,
    payload: BackofficePromotionTargetCreateRequest,
) -> BackofficePromotionTarget:
    rule = _get_rule_or_raise(session, promotion_code)

    if payload.target_type != "all_store" and not payload.target_code and payload.target_id is None:
        raise BackofficePromotionTargetInvalidError("promotion_target_required")

    target = PromotionTarget(
        promotion_rule_id=rule.id,
        target_type=payload.target_type,
        target_id=payload.target_id,
        target_code=payload.target_code,
    )

    try:
        create_promotion_target(session, target)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise BackofficePromotionTargetDuplicateError("promotion_target_already_exists") from exc

    return _build_target(target, rule)


def create_backoffice_coupon(
    session: Session,
    promotion_code: str,
    payload: BackofficeCouponCreateRequest,
) -> BackofficeCoupon:
    if (
        payload.ends_at is not None
        and payload.starts_at is not None
        and payload.ends_at <= payload.starts_at
    ):
        raise BackofficeCouponInvalidRangeError("coupon_effective_range_invalid")

    rule = _get_rule_or_raise(session, promotion_code)

    if get_coupon_by_code(session, payload.coupon_code) is not None:
        raise BackofficeCouponDuplicateCodeError("coupon_code_already_exists")

    coupon = Coupon(
        coupon_code=payload.coupon_code,
        coupon_name=payload.coupon_name,
        promotion_rule_id=rule.id,
        coupon_type=payload.coupon_type,
        total_limit=payload.total_limit,
        per_customer_limit=payload.per_customer_limit,
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        status="draft",
        is_active=False,
    )

    try:
        create_coupon(session, coupon)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise BackofficeCouponDuplicateCodeError("coupon_code_already_exists") from exc

    return _build_coupon(coupon, rule)


def activate_backoffice_coupon(session: Session, coupon_code: str) -> BackofficeCoupon:
    coupon_row = get_coupon_row_by_code(session, coupon_code)
    if coupon_row is None:
        raise BackofficeCouponNotFoundError("coupon_not_found")

    coupon, rule = coupon_row
    now = datetime.now(UTC)
    coupon.status = "active"
    coupon.is_active = True
    coupon.updated_at = now
    session.commit()
    return _build_coupon(coupon, rule)


def deactivate_backoffice_coupon(session: Session, coupon_code: str) -> BackofficeCoupon:
    coupon_row = get_coupon_row_by_code(session, coupon_code)
    if coupon_row is None:
        raise BackofficeCouponNotFoundError("coupon_not_found")

    coupon, rule = coupon_row
    now = datetime.now(UTC)
    coupon.status = "paused"
    coupon.is_active = False
    coupon.updated_at = now
    session.commit()
    return _build_coupon(coupon, rule)


def _build_coupon(coupon: Coupon, rule: PromotionRule) -> BackofficeCoupon:
    return BackofficeCoupon(
        id=coupon.id,
        coupon_code=coupon.coupon_code,
        coupon_name=coupon.coupon_name,
        promotion_rule_id=coupon.promotion_rule_id,
        promotion_code=rule.promotion_code,
        coupon_type=coupon.coupon_type,
        total_limit=coupon.total_limit,
        per_customer_limit=coupon.per_customer_limit,
        starts_at=coupon.starts_at,
        ends_at=coupon.ends_at,
        status=coupon.status,
        is_active=coupon.is_active,
        created_at=coupon.created_at,
        updated_at=coupon.updated_at,
    )


def get_backoffice_coupons(session: Session) -> BackofficeCouponsResponse:
    coupons = [_build_coupon(coupon, rule) for coupon, rule in list_coupon_rows(session)]
    return BackofficeCouponsResponse(count=len(coupons), coupons=coupons)


def _apply_discount(rule: PromotionRule, price_cents: int) -> tuple[int, int]:
    if rule.discount_type == "percentage":
        discount = price_cents * rule.discount_value // 100
    elif rule.discount_type == "amount_off":
        discount = rule.discount_value
    elif rule.discount_type == "threshold_amount":
        if rule.threshold_amount_cents is not None and price_cents < rule.threshold_amount_cents:
            discount = 0
        else:
            discount = rule.discount_value
    elif rule.discount_type == "fixed_price":
        discount = max(price_cents - rule.discount_value, 0)
    else:
        discount = 0

    if rule.max_discount_cents is not None:
        discount = min(discount, rule.max_discount_cents)

    discount = min(discount, price_cents)
    return price_cents - discount, discount


def get_backoffice_promotion_preview(
    session: Session,
    promotion_code: str,
) -> BackofficePromotionPreviewResponse:
    rule = _get_rule_or_raise(session, promotion_code)
    rows = list_active_price_rows_for_preview(session, rule)

    offer_map: dict[str, BackofficePromotionPreviewOffer] = {}
    group_map: dict[str, set[str]] = {}

    for offer, price, group in rows:
        group_codes = group_map.setdefault(offer.offer_code, set())
        if group is not None:
            group_codes.add(group.group_code)

        if offer.offer_code in offer_map:
            continue

        final_price, discount = _apply_discount(rule, price.price_cents)
        badge = rule.display_badge or rule.promotion_name

        offer_map[offer.offer_code] = BackofficePromotionPreviewOffer(
            offer_code=offer.offer_code,
            title=offer.title,
            offer_type=offer.offer_type,
            group_codes=[],
            base_price_cents=price.price_cents,
            final_price_cents=final_price,
            discount_cents=discount,
            promotion_badges=[badge],
        )

    offers: list[BackofficePromotionPreviewOffer] = []
    for offer_code, preview in offer_map.items():
        offers.append(
            preview.model_copy(update={"group_codes": sorted(group_map.get(offer_code, set()))})
        )

    blocking_reasons: list[str] = []
    if not offers:
        blocking_reasons.append("promotion_rule_matches_no_offer")

    return BackofficePromotionPreviewResponse(
        promotion_code=rule.promotion_code,
        promotion_name=rule.promotion_name,
        matched_offer_count=len(offers),
        offers=offers,
        blocking_reasons=blocking_reasons,
    )
