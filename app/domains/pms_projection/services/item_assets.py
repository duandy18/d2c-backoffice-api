"""PMS item asset projection service."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.item_assets import (
    PmsItemAssetProjectionContract,
    PmsItemAssetsProjectionResponse,
)
from app.domains.pms_projection.models.item_assets import PmsItemAssetProjection
from app.domains.pms_projection.repos.item_assets import list_item_asset_projections
from app.domains.pms_projection.services.display_table import build_projection_display_table


def _build_item_asset(row: PmsItemAssetProjection) -> PmsItemAssetProjectionContract:
    return PmsItemAssetProjectionContract(
        id=row.id,
        pms_asset_id=row.pms_asset_id,
        pms_item_id=row.pms_item_id,
        item_sku=row.item_sku,
        item_name=row.item_name,
        asset_type=row.asset_type,
        usage_type=row.usage_type,
        source_type=row.source_type,
        object_key=row.object_key,
        url=row.url,
        alt_text=row.alt_text,
        sort_order=row.sort_order,
        is_primary=row.is_primary,
        status=row.status,
        raw_meta=row.raw_meta,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_item_asset_projections(session: Session) -> PmsItemAssetsProjectionResponse:
    rows = [_build_item_asset(row) for row in list_item_asset_projections(session)]
    return PmsItemAssetsProjectionResponse(
        count=len(rows),
        item_assets=rows,
        **build_projection_display_table("item_assets", rows),
    )


__all__ = ["get_pms_item_asset_projections"]
