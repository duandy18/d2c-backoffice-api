"""PMS SKU code projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.sku_codes import PmsSkuCodeProjectionsResponse
from app.domains.pms_projection.contracts.sync_actions import (
    PmsProjectionSyncScopeResponse,
)
from app.domains.pms_projection.services.sku_codes import get_pms_sku_code_projections
from app.domains.pms_projection.services.sync_actions import sync_pms_projection_scope

router = APIRouter()


@router.get("/sku-codes", response_model=PmsSkuCodeProjectionsResponse)
def pms_projection_sku_codes(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsSkuCodeProjectionsResponse:
    return get_pms_sku_code_projections(session)


@router.post("/sku-codes/sync", response_model=PmsProjectionSyncScopeResponse)
def pms_projection_sku_codes_sync(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProjectionSyncScopeResponse:
    return sync_pms_projection_scope(session, scope="sku_codes")


__all__ = ["router"]
