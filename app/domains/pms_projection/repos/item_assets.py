"""PMS item asset projection repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.item_assets import PmsItemAssetProjection


def list_item_asset_projections(session: Session) -> list[PmsItemAssetProjection]:
    statement = select(PmsItemAssetProjection).order_by(
        PmsItemAssetProjection.pms_item_id,
        PmsItemAssetProjection.usage_type,
        PmsItemAssetProjection.sort_order,
        PmsItemAssetProjection.pms_asset_id,
    )
    return list(session.scalars(statement).all())


__all__ = ["list_item_asset_projections"]
