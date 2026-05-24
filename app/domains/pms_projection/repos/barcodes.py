"""PMS barcode projection repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.barcodes import PmsBarcodeProjection


def list_barcode_projections(session: Session) -> list[PmsBarcodeProjection]:
    statement = select(PmsBarcodeProjection).order_by(
        PmsBarcodeProjection.pms_item_id,
        PmsBarcodeProjection.is_primary.desc(),
        PmsBarcodeProjection.pms_barcode_id,
    )
    return list(session.scalars(statement).all())


__all__ = ["list_barcode_projections"]
