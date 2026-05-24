"""PMS item display category binding projection service."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.category_bindings import (
    PmsItemDisplayCategoryBindingProjectionContract,
    PmsItemDisplayCategoryBindingsProjectionResponse,
)
from app.domains.pms_projection.models.category_bindings import (
    PmsItemDisplayCategoryBindingProjection,
)
from app.domains.pms_projection.repos.category_bindings import (
    list_item_display_category_binding_projections,
)
from app.domains.pms_projection.services.display_table import build_projection_display_table


def _build_item_display_category_binding(
    row: PmsItemDisplayCategoryBindingProjection,
) -> PmsItemDisplayCategoryBindingProjectionContract:
    return PmsItemDisplayCategoryBindingProjectionContract(
        id=row.id,
        pms_binding_id=row.pms_binding_id,
        pms_item_id=row.pms_item_id,
        pms_display_category_id=row.pms_display_category_id,
        item_sku=row.item_sku,
        item_name=row.item_name,
        display_category_code=row.display_category_code,
        display_category_name=row.display_category_name,
        display_category_path_code=row.display_category_path_code,
        is_primary=row.is_primary,
        sort_order=row.sort_order,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_item_display_category_binding_projections(
    session: Session,
) -> PmsItemDisplayCategoryBindingsProjectionResponse:
    rows = [
        _build_item_display_category_binding(row)
        for row in list_item_display_category_binding_projections(session)
    ]
    return PmsItemDisplayCategoryBindingsProjectionResponse(
        count=len(rows),
        item_display_category_bindings=rows,
        **build_projection_display_table("item_display_category_bindings", rows),
    )


__all__ = ["get_pms_item_display_category_binding_projections"]
