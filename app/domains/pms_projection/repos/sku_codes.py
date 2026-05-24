"""PMS SKU code projection repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.sku_codes import PmsSkuCodeProjection


def list_sku_code_projections(session: Session) -> list[PmsSkuCodeProjection]:
    statement = select(PmsSkuCodeProjection).order_by(
        PmsSkuCodeProjection.pms_item_id,
        PmsSkuCodeProjection.is_primary.desc(),
        PmsSkuCodeProjection.pms_sku_code_id,
    )
    return list(session.scalars(statement).all())


__all__ = ["list_sku_code_projections"]
