"""PMS product projection repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.products import PmsProductProjection


def list_product_projections(session: Session) -> list[PmsProductProjection]:
    statement = select(PmsProductProjection).order_by(PmsProductProjection.pms_item_id)
    return list(session.scalars(statement).all())


__all__ = ["list_product_projections"]
