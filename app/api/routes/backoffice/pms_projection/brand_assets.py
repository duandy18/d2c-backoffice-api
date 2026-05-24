"""PMS brand asset projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.brand_assets import PmsBrandAssetsProjectionResponse
from app.domains.pms_projection.contracts.sync_actions import (
    PmsProjectionSyncScopeResponse,
)
from app.domains.pms_projection.services.brand_assets import get_pms_brand_asset_projections
from app.domains.pms_projection.services.sync_actions import sync_pms_projection_scope

router = APIRouter()


@router.get("/brand-assets", response_model=PmsBrandAssetsProjectionResponse)
def pms_projection_brand_assets(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsBrandAssetsProjectionResponse:
    return get_pms_brand_asset_projections(session)


@router.post("/brand-assets/sync", response_model=PmsProjectionSyncScopeResponse)
def pms_projection_brand_assets_sync(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProjectionSyncScopeResponse:
    return sync_pms_projection_scope(session, scope="brand_assets")


__all__ = ["router"]
