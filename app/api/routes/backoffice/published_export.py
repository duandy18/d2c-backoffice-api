"""Backoffice read-v1 published export routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.published_export.contracts.published_export_contract import (
    PublishedCatalogExportResponse,
    PublishedCouponsExportResponse,
    PublishedCouponsSnapshotExportResponse,
    PublishedExportHealthResponse,
    PublishedGroupsExportResponse,
    PublishedOfferComponentsExportResponse,
    PublishedOfferPositionsExportResponse,
    PublishedOfferPricesExportResponse,
    PublishedOffersExportResponse,
    PublishedPricesExportResponse,
    PublishedPromotionRulesExportResponse,
    PublishedPromotionsExportResponse,
    PublishedPromotionTargetsExportResponse,
    PublishedStorefrontSectionLayoutsExportResponse,
    PublishedStorefrontSectionsExportResponse,
)
from app.domains.published_export.services.published_export_service import (
    get_published_catalog_export,
    get_published_coupons_export,
    get_published_export_health,
    get_published_prices_export,
    get_published_promotions_export,
)
from app.domains.published_snapshot.services.published_snapshot_service import (
    get_published_coupons_snapshot,
    get_published_groups_snapshot,
    get_published_offer_components_snapshot,
    get_published_offer_positions_snapshot,
    get_published_offer_prices_snapshot,
    get_published_offers_snapshot,
    get_published_promotion_rules_snapshot,
    get_published_promotion_targets_snapshot,
    get_published_storefront_section_layouts_snapshot,
    get_published_storefront_sections_snapshot,
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


# Legacy read-v1 exports kept until d2c-api runtime sync is moved to Offer snapshots.
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


@router.get("/snapshot/groups", response_model=PublishedGroupsExportResponse)
def published_snapshot_groups_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedGroupsExportResponse:
    return get_published_groups_snapshot(session, publish_version)


@router.get("/snapshot/offers", response_model=PublishedOffersExportResponse)
def published_snapshot_offers_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedOffersExportResponse:
    return get_published_offers_snapshot(session, publish_version)


@router.get("/snapshot/offer-components", response_model=PublishedOfferComponentsExportResponse)
def published_snapshot_offer_components_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedOfferComponentsExportResponse:
    return get_published_offer_components_snapshot(session, publish_version)


@router.get("/snapshot/offer-prices", response_model=PublishedOfferPricesExportResponse)
def published_snapshot_offer_prices_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedOfferPricesExportResponse:
    return get_published_offer_prices_snapshot(session, publish_version)


@router.get("/snapshot/offer-positions", response_model=PublishedOfferPositionsExportResponse)
def published_snapshot_offer_positions_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedOfferPositionsExportResponse:
    return get_published_offer_positions_snapshot(session, publish_version)


@router.get("/snapshot/promotion-rules", response_model=PublishedPromotionRulesExportResponse)
def published_snapshot_promotion_rules_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedPromotionRulesExportResponse:
    return get_published_promotion_rules_snapshot(session, publish_version)


@router.get("/snapshot/promotion-targets", response_model=PublishedPromotionTargetsExportResponse)
def published_snapshot_promotion_targets_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedPromotionTargetsExportResponse:
    return get_published_promotion_targets_snapshot(session, publish_version)


@router.get("/snapshot/coupons", response_model=PublishedCouponsSnapshotExportResponse)
def published_snapshot_coupons_export(
    _: ServiceClientDep,
    session: SessionDep,
    publish_version: Annotated[str | None, Query()] = None,
) -> PublishedCouponsSnapshotExportResponse:
    return get_published_coupons_snapshot(session, publish_version)


@router.get(
    "/snapshot/storefront-sections", response_model=PublishedStorefrontSectionsExportResponse
)
def published_snapshot_storefront_sections_export(
    session: SessionDep,
    _: ServiceClientDep,
    publish_version: str | None = None,
) -> PublishedStorefrontSectionsExportResponse:
    return get_published_storefront_sections_snapshot(session, publish_version)


@router.get(
    "/snapshot/storefront-section-layouts",
    response_model=PublishedStorefrontSectionLayoutsExportResponse,
)
def published_snapshot_storefront_section_layouts_export(
    session: SessionDep,
    _: ServiceClientDep,
    publish_version: str | None = None,
) -> PublishedStorefrontSectionLayoutsExportResponse:
    return get_published_storefront_section_layouts_snapshot(session, publish_version)
