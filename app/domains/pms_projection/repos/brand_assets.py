"""PMS brand asset projection repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.brand_assets import PmsBrandAssetProjection


def list_brand_asset_projections(session: Session) -> list[PmsBrandAssetProjection]:
    statement = select(PmsBrandAssetProjection).order_by(
        PmsBrandAssetProjection.brand_id,
        PmsBrandAssetProjection.usage_type,
        PmsBrandAssetProjection.sort_order,
        PmsBrandAssetProjection.pms_asset_id,
    )
    return list(session.scalars(statement).all())


__all__ = ["list_brand_asset_projections"]
