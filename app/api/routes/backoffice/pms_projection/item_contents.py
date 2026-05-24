"""PMS item content projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.item_contents import (
    PmsItemContentsProjectionResponse,
)
from app.domains.pms_projection.contracts.sync_actions import (
    PmsProjectionSyncScopeResponse,
)
from app.domains.pms_projection.services.item_contents import (
    get_pms_item_content_projections,
)
from app.domains.pms_projection.services.sync_actions import sync_pms_projection_scope

router = APIRouter()


@router.get("/item-contents", response_model=PmsItemContentsProjectionResponse)
def pms_projection_item_contents(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsItemContentsProjectionResponse:
    return get_pms_item_content_projections(session)


@router.post("/item-contents/sync", response_model=PmsProjectionSyncScopeResponse)
def pms_projection_item_contents_sync(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProjectionSyncScopeResponse:
    return sync_pms_projection_scope(session, scope="item_contents")


__all__ = ["router"]
