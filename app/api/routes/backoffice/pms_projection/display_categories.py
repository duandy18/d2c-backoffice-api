"""PMS display category projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.display_categories import (
    PmsDisplayCategoriesProjectionResponse,
)
from app.domains.pms_projection.contracts.sync_actions import (
    PmsProjectionSyncScopeResponse,
)
from app.domains.pms_projection.services.display_categories import (
    get_pms_display_category_projections,
)
from app.domains.pms_projection.services.sync_actions import sync_pms_projection_scope

router = APIRouter()


@router.get("/display-categories", response_model=PmsDisplayCategoriesProjectionResponse)
def pms_projection_display_categories(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsDisplayCategoriesProjectionResponse:
    return get_pms_display_category_projections(session)


@router.post("/display-categories/sync", response_model=PmsProjectionSyncScopeResponse)
def pms_projection_display_categories_sync(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProjectionSyncScopeResponse:
    return sync_pms_projection_scope(session, scope="display_categories")


__all__ = ["router"]
