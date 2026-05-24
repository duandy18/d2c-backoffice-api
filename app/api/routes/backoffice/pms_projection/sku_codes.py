"""PMS SKU code projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.sku_codes import PmsSkuCodeProjectionsResponse
from app.domains.pms_projection.services.sku_codes import get_pms_sku_code_projections

router = APIRouter()


@router.get("/sku-codes", response_model=PmsSkuCodeProjectionsResponse)
def pms_projection_sku_codes(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsSkuCodeProjectionsResponse:
    return get_pms_sku_code_projections(session)


__all__ = ["router"]
