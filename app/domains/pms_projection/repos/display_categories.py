"""PMS display category projection repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.display_categories import PmsDisplayCategoryProjection


def list_display_category_projections(session: Session) -> list[PmsDisplayCategoryProjection]:
    statement = select(PmsDisplayCategoryProjection).order_by(
        PmsDisplayCategoryProjection.level,
        PmsDisplayCategoryProjection.sort_order,
        PmsDisplayCategoryProjection.pms_display_category_id,
    )
    return list(session.scalars(statement).all())


__all__ = ["list_display_category_projections"]
