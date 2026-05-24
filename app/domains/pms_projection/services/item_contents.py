"""PMS item content projection service."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.item_contents import (
    PmsItemContentProjectionContract,
    PmsItemContentsProjectionResponse,
)
from app.domains.pms_projection.models.item_contents import PmsItemContentProjection
from app.domains.pms_projection.repos.item_contents import list_item_content_projections


def _build_item_content(row: PmsItemContentProjection) -> PmsItemContentProjectionContract:
    return PmsItemContentProjectionContract(
        id=row.id,
        pms_content_id=row.pms_content_id,
        pms_item_id=row.pms_item_id,
        item_sku=row.item_sku,
        item_name=row.item_name,
        base_title=row.base_title,
        base_description=row.base_description,
        short_description=row.short_description,
        spec_params=row.spec_params,
        material_text=row.material_text,
        ingredients_text=row.ingredients_text,
        dimensions_text=row.dimensions_text,
        weight_text=row.weight_text,
        safety_instructions=row.safety_instructions,
        usage_instructions=row.usage_instructions,
        storage_instructions=row.storage_instructions,
        status=row.status,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_item_content_projections(session: Session) -> PmsItemContentsProjectionResponse:
    rows = [_build_item_content(row) for row in list_item_content_projections(session)]
    return PmsItemContentsProjectionResponse(count=len(rows), item_contents=rows)


__all__ = ["get_pms_item_content_projections"]
