"""PMS unit projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.sync_actions import (
    PmsProjectionSyncScopeResponse,
)
from app.domains.pms_projection.contracts.units import PmsUnitProjectionsResponse
from app.domains.pms_projection.services.sync_actions import sync_pms_projection_scope
from app.domains.pms_projection.services.units import get_pms_unit_projections

router = APIRouter()


@router.get("/units", response_model=PmsUnitProjectionsResponse)
def pms_projection_units(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsUnitProjectionsResponse:
    return get_pms_unit_projections(session)


@router.post("/units/sync", response_model=PmsProjectionSyncScopeResponse)
def pms_projection_units_sync(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProjectionSyncScopeResponse:
    return sync_pms_projection_scope(session, scope="units")


__all__ = ["router"]
