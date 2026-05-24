"""PMS item content projection repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.item_contents import PmsItemContentProjection


def list_item_content_projections(session: Session) -> list[PmsItemContentProjection]:
    statement = select(PmsItemContentProjection).order_by(
        PmsItemContentProjection.pms_item_id,
        PmsItemContentProjection.pms_content_id,
    )
    return list(session.scalars(statement).all())


__all__ = ["list_item_content_projections"]
