"""PMS item display category binding projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.category_bindings import (
    PmsItemDisplayCategoryBindingsProjectionResponse,
)
from app.domains.pms_projection.services.category_bindings import (
    get_pms_item_display_category_binding_projections,
)

router = APIRouter()


@router.get(
    "/item-display-category-bindings",
    response_model=PmsItemDisplayCategoryBindingsProjectionResponse,
)
def pms_projection_item_display_category_bindings(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsItemDisplayCategoryBindingsProjectionResponse:
    return get_pms_item_display_category_binding_projections(session)


__all__ = ["router"]
