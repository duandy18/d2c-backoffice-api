"""PMS product projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.products import PmsProductProjectionsResponse
from app.domains.pms_projection.services.products import get_pms_product_projections

router = APIRouter()


@router.get("/products", response_model=PmsProductProjectionsResponse)
def pms_projection_products(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProductProjectionsResponse:
    return get_pms_product_projections(session)


__all__ = ["router"]
