"""Backoffice listing routes; HTTP paths are /backoffice/listing/*."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.listing.contracts.listing_contract import (
    BackofficeListingHealthResponse,
    ProductListingConfigsResponse,
    SkuListingConfigsResponse,
)
from app.domains.listing.services.listing_service import (
    get_backoffice_listing_health,
    get_product_listing_configs,
    get_sku_listing_configs,
)

router = APIRouter(prefix="/backoffice/listing", tags=["backoffice-listing"])
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


@router.get("/health", response_model=BackofficeListingHealthResponse)
def backoffice_listing_health(_: BackofficeClientDep) -> BackofficeListingHealthResponse:
    return get_backoffice_listing_health()


@router.get("/products", response_model=ProductListingConfigsResponse)
def backoffice_listing_products(
    _: BackofficeClientDep,
    session: SessionDep,
) -> ProductListingConfigsResponse:
    return get_product_listing_configs(session)


@router.get("/skus", response_model=SkuListingConfigsResponse)
def backoffice_listing_skus(
    _: BackofficeClientDep,
    session: SessionDep,
) -> SkuListingConfigsResponse:
    return get_sku_listing_configs(session)
