"""PMS item content projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.item_contents import (
    PmsItemContentsProjectionResponse,
)
from app.domains.pms_projection.services.item_contents import (
    get_pms_item_content_projections,
)

router = APIRouter()


@router.get("/item-contents", response_model=PmsItemContentsProjectionResponse)
def pms_projection_item_contents(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsItemContentsProjectionResponse:
    return get_pms_item_content_projections(session)


__all__ = ["router"]
