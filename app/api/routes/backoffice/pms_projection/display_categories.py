"""PMS display category projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.display_categories import (
    PmsDisplayCategoriesProjectionResponse,
)
from app.domains.pms_projection.services.display_categories import (
    get_pms_display_category_projections,
)

router = APIRouter()


@router.get("/display-categories", response_model=PmsDisplayCategoriesProjectionResponse)
def pms_projection_display_categories(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsDisplayCategoriesProjectionResponse:
    return get_pms_display_category_projections(session)


__all__ = ["router"]
