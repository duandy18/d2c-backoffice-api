"""PMS projection health route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep
from app.domains.pms_projection.contracts.health import PmsProjectionHealthResponse
from app.domains.pms_projection.services.health import get_pms_projection_health

router = APIRouter()


@router.get("/health", response_model=PmsProjectionHealthResponse)
def pms_projection_health(_: BackofficeClientDep) -> PmsProjectionHealthResponse:
    return get_pms_projection_health()


__all__ = ["router"]
