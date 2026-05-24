"""PMS brand asset projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.brand_assets import PmsBrandAssetsProjectionResponse
from app.domains.pms_projection.services.brand_assets import get_pms_brand_asset_projections

router = APIRouter()


@router.get("/brand-assets", response_model=PmsBrandAssetsProjectionResponse)
def pms_projection_brand_assets(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsBrandAssetsProjectionResponse:
    return get_pms_brand_asset_projections(session)


__all__ = ["router"]
