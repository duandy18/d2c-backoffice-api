"""PMS unit projection repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.units import PmsUnitProjection


def list_unit_projections(session: Session) -> list[PmsUnitProjection]:
    statement = select(PmsUnitProjection).order_by(
        PmsUnitProjection.pms_item_id,
        PmsUnitProjection.pms_item_uom_id,
    )
    return list(session.scalars(statement).all())


__all__ = ["list_unit_projections"]
