"""PMS barcode projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.barcodes import PmsBarcodeProjectionsResponse
from app.domains.pms_projection.services.barcodes import get_pms_barcode_projections

router = APIRouter()


@router.get("/barcodes", response_model=PmsBarcodeProjectionsResponse)
def pms_projection_barcodes(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsBarcodeProjectionsResponse:
    return get_pms_barcode_projections(session)


__all__ = ["router"]
