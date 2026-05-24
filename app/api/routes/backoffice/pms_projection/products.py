"""PMS product projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.products import PmsProductProjectionsResponse
from app.domains.pms_projection.contracts.sync_actions import (
    PmsProjectionSyncScopeResponse,
)
from app.domains.pms_projection.services.products import get_pms_product_projections
from app.domains.pms_projection.services.sync_actions import sync_pms_projection_scope

router = APIRouter()


@router.get("/products", response_model=PmsProductProjectionsResponse)
def pms_projection_products(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProductProjectionsResponse:
    return get_pms_product_projections(session)


@router.post("/products/sync", response_model=PmsProjectionSyncScopeResponse)
def pms_projection_products_sync(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProjectionSyncScopeResponse:
    return sync_pms_projection_scope(session, scope="products")


__all__ = ["router"]
