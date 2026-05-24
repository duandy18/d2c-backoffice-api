"""PMS item display category binding projection repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.category_bindings import (
    PmsItemDisplayCategoryBindingProjection,
)


def list_item_display_category_binding_projections(
    session: Session,
) -> list[PmsItemDisplayCategoryBindingProjection]:
    statement = select(PmsItemDisplayCategoryBindingProjection).order_by(
        PmsItemDisplayCategoryBindingProjection.pms_item_id,
        PmsItemDisplayCategoryBindingProjection.is_primary.desc(),
        PmsItemDisplayCategoryBindingProjection.sort_order,
        PmsItemDisplayCategoryBindingProjection.pms_binding_id,
    )
    return list(session.scalars(statement).all())


__all__ = ["list_item_display_category_binding_projections"]
