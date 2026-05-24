"""PMS item asset projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.item_assets import PmsItemAssetsProjectionResponse
from app.domains.pms_projection.services.item_assets import get_pms_item_asset_projections

router = APIRouter()


@router.get("/item-assets", response_model=PmsItemAssetsProjectionResponse)
def pms_projection_item_assets(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsItemAssetsProjectionResponse:
    return get_pms_item_asset_projections(session)


__all__ = ["router"]
