"""PMS display category projection service."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.display_categories import (
    PmsDisplayCategoriesProjectionResponse,
    PmsDisplayCategoryProjectionContract,
)
from app.domains.pms_projection.models.display_categories import PmsDisplayCategoryProjection
from app.domains.pms_projection.repos.display_categories import (
    list_display_category_projections,
)


def _build_display_category(
    row: PmsDisplayCategoryProjection,
) -> PmsDisplayCategoryProjectionContract:
    return PmsDisplayCategoryProjectionContract(
        id=row.id,
        pms_display_category_id=row.pms_display_category_id,
        parent_id=row.parent_id,
        level=row.level,
        category_code=row.category_code,
        category_name=row.category_name,
        display_name=row.display_name,
        path_code=row.path_code,
        description=row.description,
        image_url=row.image_url,
        sort_order=row.sort_order,
        is_active=row.is_active,
        is_leaf=row.is_leaf,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_display_category_projections(
    session: Session,
) -> PmsDisplayCategoriesProjectionResponse:
    rows = [_build_display_category(row) for row in list_display_category_projections(session)]
    return PmsDisplayCategoriesProjectionResponse(count=len(rows), display_categories=rows)


__all__ = ["get_pms_display_category_projections"]
