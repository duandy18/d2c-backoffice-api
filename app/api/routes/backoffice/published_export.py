"""Backoffice read-v1 published export routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.published_export.contracts.published_export_contract import (
    PublishedCatalogExportResponse,
    PublishedCouponsExportResponse,
    PublishedExportHealthResponse,
    PublishedPricesExportResponse,
    PublishedPromotionsExportResponse,
)
from app.domains.published_export.services.published_export_service import (
    get_published_catalog_export,
    get_published_coupons_export,
    get_published_export_health,
    get_published_prices_export,
    get_published_promotions_export,
)

router = APIRouter(
    prefix="/backoffice/read/v1/published",
    tags=["backoffice-read-v1-published"],
)
SessionDep = Annotated[Session, Depends(get_session)]


def require_service_client(
    x_service_client: Annotated[str | None, Header(alias="X-Service-Client")] = None,
) -> None:
    if x_service_client != "d2c-service":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="service_client_required",
        )


ServiceClientDep = Annotated[None, Depends(require_service_client)]


@router.get("/health", response_model=PublishedExportHealthResponse)
def published_export_health(_: ServiceClientDep) -> PublishedExportHealthResponse:
    return get_published_export_health()


@router.get("/catalog", response_model=PublishedCatalogExportResponse)
def published_catalog_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedCatalogExportResponse:
    return get_published_catalog_export(session, publish_version)


@router.get("/prices", response_model=PublishedPricesExportResponse)
def published_prices_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedPricesExportResponse:
    return get_published_prices_export(session, publish_version)


@router.get("/promotions", response_model=PublishedPromotionsExportResponse)
def published_promotions_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedPromotionsExportResponse:
    return get_published_promotions_export(session, publish_version)


@router.get("/coupons", response_model=PublishedCouponsExportResponse)
def published_coupons_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedCouponsExportResponse:
    return get_published_coupons_export(session, publish_version)
