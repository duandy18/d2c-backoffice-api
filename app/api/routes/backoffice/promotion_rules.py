"""Backoffice PromotionRule routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.promotions.contracts.promotion_rule_contract import (
    BackofficeCoupon,
    BackofficeCouponCreateRequest,
    BackofficeCouponsResponse,
    BackofficePromotionPreviewResponse,
    BackofficePromotionRule,
    BackofficePromotionRuleCreateRequest,
    BackofficePromotionRuleHealthResponse,
    BackofficePromotionRulesResponse,
    BackofficePromotionTarget,
    BackofficePromotionTargetCreateRequest,
    BackofficePromotionTargetsResponse,
)
from app.domains.promotions.services.promotion_rule_service import (
    BackofficeCouponDuplicateCodeError,
    BackofficeCouponInvalidRangeError,
    BackofficeCouponNotFoundError,
    BackofficePromotionRuleDuplicateCodeError,
    BackofficePromotionRuleInvalidRangeError,
    BackofficePromotionRuleNotFoundError,
    BackofficePromotionTargetDuplicateError,
    BackofficePromotionTargetInvalidError,
    activate_backoffice_coupon,
    activate_backoffice_promotion_rule,
    create_backoffice_coupon,
    create_backoffice_promotion_rule,
    create_backoffice_promotion_target,
    deactivate_backoffice_coupon,
    deactivate_backoffice_promotion_rule,
    get_backoffice_coupons,
    get_backoffice_promotion_preview,
    get_backoffice_promotion_rules,
    get_backoffice_promotion_targets,
)

router = APIRouter(prefix="/backoffice/promotion-rules", tags=["backoffice-promotion-rules"])
SessionDep = Annotated[Session, Depends(get_session)]


def require_backoffice_client(
    x_backoffice_client: Annotated[str | None, Header(alias="X-Backoffice-Client")] = None,
) -> None:
    if x_backoffice_client != "d2c-backoffice":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="backoffice_client_required",
        )


BackofficeClientDep = Annotated[None, Depends(require_backoffice_client)]


@router.get("/health", response_model=BackofficePromotionRuleHealthResponse)
def backoffice_promotion_rules_health(
    _: BackofficeClientDep,
) -> BackofficePromotionRuleHealthResponse:
    return BackofficePromotionRuleHealthResponse(
        status="ok",
        module="backoffice_promotion_rules",
        surface="merchant_management",
    )


@router.get("", response_model=BackofficePromotionRulesResponse)
def backoffice_promotion_rules_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficePromotionRulesResponse:
    return get_backoffice_promotion_rules(session)


@router.post("", response_model=BackofficePromotionRule, status_code=status.HTTP_201_CREATED)
def backoffice_promotion_rules_create(
    payload: BackofficePromotionRuleCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficePromotionRule:
    try:
        return create_backoffice_promotion_rule(session, payload)
    except BackofficePromotionRuleDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except BackofficePromotionRuleInvalidRangeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post("/{promotion_code}/activate", response_model=BackofficePromotionRule)
def backoffice_promotion_rules_activate(
    promotion_code: str,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficePromotionRule:
    try:
        return activate_backoffice_promotion_rule(session, promotion_code)
    except BackofficePromotionRuleNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{promotion_code}/deactivate", response_model=BackofficePromotionRule)
def backoffice_promotion_rules_deactivate(
    promotion_code: str,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficePromotionRule:
    try:
        return deactivate_backoffice_promotion_rule(session, promotion_code)
    except BackofficePromotionRuleNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "/{promotion_code}/targets",
    response_model=BackofficePromotionTarget,
    status_code=status.HTTP_201_CREATED,
)
def backoffice_promotion_rule_targets_create(
    promotion_code: str,
    payload: BackofficePromotionTargetCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficePromotionTarget:
    try:
        return create_backoffice_promotion_target(session, promotion_code, payload)
    except BackofficePromotionRuleNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BackofficePromotionTargetInvalidError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except BackofficePromotionTargetDuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/targets", response_model=BackofficePromotionTargetsResponse)
def backoffice_promotion_targets_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficePromotionTargetsResponse:
    return get_backoffice_promotion_targets(session)


@router.post(
    "/{promotion_code}/coupons",
    response_model=BackofficeCoupon,
    status_code=status.HTTP_201_CREATED,
)
def backoffice_promotion_rule_coupon_create(
    promotion_code: str,
    payload: BackofficeCouponCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeCoupon:
    try:
        return create_backoffice_coupon(session, promotion_code, payload)
    except BackofficePromotionRuleNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BackofficeCouponDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except BackofficeCouponInvalidRangeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.get("/coupons", response_model=BackofficeCouponsResponse)
def backoffice_coupons_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeCouponsResponse:
    return get_backoffice_coupons(session)


@router.post("/coupons/{coupon_code}/activate", response_model=BackofficeCoupon)
def backoffice_coupons_activate(
    coupon_code: str,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeCoupon:
    try:
        return activate_backoffice_coupon(session, coupon_code)
    except BackofficeCouponNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/coupons/{coupon_code}/deactivate", response_model=BackofficeCoupon)
def backoffice_coupons_deactivate(
    coupon_code: str,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeCoupon:
    try:
        return deactivate_backoffice_coupon(session, coupon_code)
    except BackofficeCouponNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{promotion_code}/preview", response_model=BackofficePromotionPreviewResponse)
def backoffice_promotion_rule_preview(
    promotion_code: str,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficePromotionPreviewResponse:
    try:
        return get_backoffice_promotion_preview(session, promotion_code)
    except BackofficePromotionRuleNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
