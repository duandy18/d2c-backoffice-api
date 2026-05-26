"""Backoffice Offer routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.offers.contracts.offer_contract import (
    BackofficeOfferComponentContract,
    BackofficeOfferComponentCreateRequest,
    BackofficeOfferComponentsResponse,
    BackofficeOfferContract,
    BackofficeOfferCreateRequest,
    BackofficeOfferPositionContract,
    BackofficeOfferPositionCreateRequest,
    BackofficeOfferPositionsResponse,
    BackofficeOfferPriceContract,
    BackofficeOfferPriceCreateRequest,
    BackofficeOfferPricesResponse,
    BackofficeOfferPublishCheckResponse,
    BackofficeOffersResponse,
)
from app.domains.offers.services.offer_service import (
    BackofficeOfferDuplicateCodeError,
    BackofficeOfferGroupNotFoundError,
    BackofficeOfferInvalidRangeError,
    BackofficeOfferNotFoundError,
    BackofficeOfferPositionDuplicateError,
    BackofficeOfferPriceDuplicateError,
    BackofficeOfferProjectionNotFoundError,
    create_backoffice_offer,
    create_backoffice_offer_component,
    create_backoffice_offer_position,
    create_backoffice_offer_price,
    get_backoffice_offer,
    get_backoffice_offer_components,
    get_backoffice_offer_positions,
    get_backoffice_offer_prices,
    get_backoffice_offer_publish_check,
    get_backoffice_offers,
)

router = APIRouter(prefix="/backoffice/offers", tags=["backoffice-offers"])
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


@router.get("", response_model=BackofficeOffersResponse)
def backoffice_offers_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeOffersResponse:
    return get_backoffice_offers(session)


@router.post("", response_model=BackofficeOfferContract, status_code=status.HTTP_201_CREATED)
def backoffice_offers_create(
    payload: BackofficeOfferCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeOfferContract:
    try:
        return create_backoffice_offer(session, payload)
    except BackofficeOfferDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except BackofficeOfferInvalidRangeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.get("/{offer_code}", response_model=BackofficeOfferContract)
def backoffice_offers_get(
    offer_code: str,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeOfferContract:
    try:
        return get_backoffice_offer(session, offer_code)
    except BackofficeOfferNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{offer_code}/components", response_model=BackofficeOfferComponentsResponse)
def backoffice_offer_components_list(
    offer_code: str,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeOfferComponentsResponse:
    try:
        return get_backoffice_offer_components(session, offer_code)
    except BackofficeOfferNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "/{offer_code}/components",
    response_model=BackofficeOfferComponentContract,
    status_code=status.HTTP_201_CREATED,
)
def backoffice_offer_components_create(
    offer_code: str,
    payload: BackofficeOfferComponentCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeOfferComponentContract:
    try:
        return create_backoffice_offer_component(session, offer_code, payload)
    except BackofficeOfferNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BackofficeOfferProjectionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{offer_code}/prices", response_model=BackofficeOfferPricesResponse)
def backoffice_offer_prices_list(
    offer_code: str,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeOfferPricesResponse:
    try:
        return get_backoffice_offer_prices(session, offer_code)
    except BackofficeOfferNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "/{offer_code}/prices",
    response_model=BackofficeOfferPriceContract,
    status_code=status.HTTP_201_CREATED,
)
def backoffice_offer_prices_create(
    offer_code: str,
    payload: BackofficeOfferPriceCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeOfferPriceContract:
    try:
        return create_backoffice_offer_price(session, offer_code, payload)
    except BackofficeOfferNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BackofficeOfferPriceDuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except BackofficeOfferInvalidRangeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.get("/{offer_code}/positions", response_model=BackofficeOfferPositionsResponse)
def backoffice_offer_positions_list(
    offer_code: str,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeOfferPositionsResponse:
    try:
        return get_backoffice_offer_positions(session, offer_code)
    except BackofficeOfferNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BackofficeOfferGroupNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "/{offer_code}/positions",
    response_model=BackofficeOfferPositionContract,
    status_code=status.HTTP_201_CREATED,
)
def backoffice_offer_positions_create(
    offer_code: str,
    payload: BackofficeOfferPositionCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeOfferPositionContract:
    try:
        return create_backoffice_offer_position(session, offer_code, payload)
    except BackofficeOfferNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BackofficeOfferGroupNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BackofficeOfferPositionDuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except BackofficeOfferInvalidRangeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.get("/{offer_code}/publish-check", response_model=BackofficeOfferPublishCheckResponse)
def backoffice_offer_publish_check(
    offer_code: str,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeOfferPublishCheckResponse:
    try:
        return get_backoffice_offer_publish_check(session, offer_code)
    except BackofficeOfferNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
