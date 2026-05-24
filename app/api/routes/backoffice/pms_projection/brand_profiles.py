"""PMS brand profile projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.brand_profiles import (
    PmsBrandProfilesProjectionResponse,
)
from app.domains.pms_projection.services.brand_profiles import (
    get_pms_brand_profile_projections,
)

router = APIRouter()


@router.get("/brand-profiles", response_model=PmsBrandProfilesProjectionResponse)
def pms_projection_brand_profiles(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsBrandProfilesProjectionResponse:
    return get_pms_brand_profile_projections(session)


__all__ = ["router"]
