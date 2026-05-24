"""Backoffice pricing routes; HTTP paths are /backoffice/pricing/*."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.pricing.contracts.price_config_contract import (
    BackofficePricingHealthResponse,
    PriceConfigsResponse,
)
from app.domains.pricing.services.price_config_service import (
    get_backoffice_pricing_health,
    get_price_configs,
)

router = APIRouter(prefix="/backoffice/pricing", tags=["backoffice-pricing"])
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


@router.get("/health", response_model=BackofficePricingHealthResponse)
def backoffice_pricing_health(_: BackofficeClientDep) -> BackofficePricingHealthResponse:
    return get_backoffice_pricing_health()


@router.get("/configs", response_model=PriceConfigsResponse)
def backoffice_price_configs(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PriceConfigsResponse:
    return get_price_configs(session)
