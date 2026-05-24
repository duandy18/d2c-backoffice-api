"""PMS projection sync run route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.sync_runs import PmsProjectionSyncRunsResponse
from app.domains.pms_projection.services.sync_runs import get_pms_projection_sync_runs

router = APIRouter()


@router.get("/sync-runs", response_model=PmsProjectionSyncRunsResponse)
def pms_projection_sync_runs(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProjectionSyncRunsResponse:
    return get_pms_projection_sync_runs(session)


__all__ = ["router"]
