"""PMS product projection service."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.products import (
    PmsProductProjectionContract,
    PmsProductProjectionsResponse,
)
from app.domains.pms_projection.models.products import PmsProductProjection
from app.domains.pms_projection.repos.products import list_product_projections
from app.domains.pms_projection.services.display_table import build_projection_display_table


def _build_product(row: PmsProductProjection) -> PmsProductProjectionContract:
    return PmsProductProjectionContract(
        id=row.id,
        pms_item_id=row.pms_item_id,
        pms_sku=row.pms_sku,
        item_name=row.item_name,
        item_spec=row.item_spec,
        enabled=row.enabled,
        supplier_id=row.supplier_id,
        brand_id=row.brand_id,
        brand_code=row.brand_code,
        brand_name=row.brand_name,
        category_id=row.category_id,
        category_code=row.category_code,
        category_name=row.category_name,
        category_path_code=row.category_path_code,
        category_level=row.category_level,
        category_is_leaf=row.category_is_leaf,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_product_projections(session: Session) -> PmsProductProjectionsResponse:
    rows = [_build_product(row) for row in list_product_projections(session)]
    return PmsProductProjectionsResponse(
        count=len(rows),
        products=rows,
        **build_projection_display_table("products", rows),
    )


__all__ = ["get_pms_product_projections"]
