"""PMS unit projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.units import PmsUnitProjectionsResponse
from app.domains.pms_projection.services.units import get_pms_unit_projections

router = APIRouter()


@router.get("/units", response_model=PmsUnitProjectionsResponse)
def pms_projection_units(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsUnitProjectionsResponse:
    return get_pms_unit_projections(session)


__all__ = ["router"]
