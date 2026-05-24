"""PMS item asset projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.item_assets import PmsItemAssetsProjectionResponse
from app.domains.pms_projection.contracts.sync_actions import (
    PmsProjectionSyncScopeResponse,
)
from app.domains.pms_projection.services.item_assets import get_pms_item_asset_projections
from app.domains.pms_projection.services.sync_actions import sync_pms_projection_scope

router = APIRouter()


@router.get("/item-assets", response_model=PmsItemAssetsProjectionResponse)
def pms_projection_item_assets(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsItemAssetsProjectionResponse:
    return get_pms_item_asset_projections(session)


@router.post("/item-assets/sync", response_model=PmsProjectionSyncScopeResponse)
def pms_projection_item_assets_sync(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProjectionSyncScopeResponse:
    return sync_pms_projection_scope(session, scope="item_assets")


__all__ = ["router"]
