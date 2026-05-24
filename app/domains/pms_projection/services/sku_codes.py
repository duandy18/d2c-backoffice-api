"""PMS SKU code projection service."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.sku_codes import (
    PmsSkuCodeProjectionContract,
    PmsSkuCodeProjectionsResponse,
)
from app.domains.pms_projection.models.sku_codes import PmsSkuCodeProjection
from app.domains.pms_projection.repos.sku_codes import list_sku_code_projections
from app.domains.pms_projection.services.display_table import build_projection_display_table


def _build_sku_code(row: PmsSkuCodeProjection) -> PmsSkuCodeProjectionContract:
    return PmsSkuCodeProjectionContract(
        id=row.id,
        pms_sku_code_id=row.pms_sku_code_id,
        pms_item_id=row.pms_item_id,
        sku_code=row.sku_code,
        code_type=row.code_type,
        is_primary=row.is_primary,
        is_active=row.is_active,
        effective_from=row.effective_from,
        effective_to=row.effective_to,
        remark=row.remark,
        item_sku=row.item_sku,
        item_name=row.item_name,
        item_enabled=row.item_enabled,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_sku_code_projections(session: Session) -> PmsSkuCodeProjectionsResponse:
    rows = [_build_sku_code(row) for row in list_sku_code_projections(session)]
    return PmsSkuCodeProjectionsResponse(
        count=len(rows),
        sku_codes=rows,
        **build_projection_display_table("sku_codes", rows),
    )


__all__ = ["get_pms_sku_code_projections"]
