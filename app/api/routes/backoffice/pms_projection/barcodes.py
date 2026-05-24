"""PMS barcode projection route."""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection.deps import BackofficeClientDep, SessionDep
from app.domains.pms_projection.contracts.barcodes import PmsBarcodeProjectionsResponse
from app.domains.pms_projection.contracts.sync_actions import (
    PmsProjectionSyncScopeResponse,
)
from app.domains.pms_projection.services.barcodes import get_pms_barcode_projections
from app.domains.pms_projection.services.sync_actions import sync_pms_projection_scope

router = APIRouter()


@router.get("/barcodes", response_model=PmsBarcodeProjectionsResponse)
def pms_projection_barcodes(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsBarcodeProjectionsResponse:
    return get_pms_barcode_projections(session)


@router.post("/barcodes/sync", response_model=PmsProjectionSyncScopeResponse)
def pms_projection_barcodes_sync(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProjectionSyncScopeResponse:
    return sync_pms_projection_scope(session, scope="barcodes")


__all__ = ["router"]
