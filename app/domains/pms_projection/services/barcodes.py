"""PMS barcode projection service."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.barcodes import (
    PmsBarcodeProjectionContract,
    PmsBarcodeProjectionsResponse,
)
from app.domains.pms_projection.models.barcodes import PmsBarcodeProjection
from app.domains.pms_projection.repos.barcodes import list_barcode_projections


def _build_barcode(row: PmsBarcodeProjection) -> PmsBarcodeProjectionContract:
    return PmsBarcodeProjectionContract(
        id=row.id,
        pms_barcode_id=row.pms_barcode_id,
        pms_item_id=row.pms_item_id,
        pms_item_uom_id=row.pms_item_uom_id,
        barcode=row.barcode,
        symbology=row.symbology,
        active=row.active,
        is_primary=row.is_primary,
        uom=row.uom,
        uom_name=row.uom_name,
        ratio_to_base=row.ratio_to_base,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_barcode_projections(session: Session) -> PmsBarcodeProjectionsResponse:
    rows = [_build_barcode(row) for row in list_barcode_projections(session)]
    return PmsBarcodeProjectionsResponse(count=len(rows), barcodes=rows)


__all__ = ["get_pms_barcode_projections"]
