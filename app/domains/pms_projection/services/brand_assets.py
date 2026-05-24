"""PMS brand asset projection service."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.brand_assets import (
    PmsBrandAssetProjectionContract,
    PmsBrandAssetsProjectionResponse,
)
from app.domains.pms_projection.models.brand_assets import PmsBrandAssetProjection
from app.domains.pms_projection.repos.brand_assets import list_brand_asset_projections


def _build_brand_asset(row: PmsBrandAssetProjection) -> PmsBrandAssetProjectionContract:
    return PmsBrandAssetProjectionContract(
        id=row.id,
        pms_asset_id=row.pms_asset_id,
        brand_id=row.brand_id,
        brand_code=row.brand_code,
        brand_name=row.brand_name,
        asset_type=row.asset_type,
        usage_type=row.usage_type,
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


def get_pms_brand_asset_projections(session: Session) -> PmsBrandAssetsProjectionResponse:
    rows = [_build_brand_asset(row) for row in list_brand_asset_projections(session)]
    return PmsBrandAssetsProjectionResponse(count=len(rows), brand_assets=rows)


__all__ = ["get_pms_brand_asset_projections"]
