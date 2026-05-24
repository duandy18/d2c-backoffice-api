"""PMS brand asset projection contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.domains.pms_projection.contracts.display_table import PmsProjectionDisplayTable


class PmsBrandAssetProjectionContract(BaseModel):
    id: int
    pms_asset_id: int
    brand_id: int
    brand_code: str | None
    brand_name: str | None
    asset_type: str
    usage_type: str
    object_key: str | None
    url: str | None
    alt_text: str | None
    sort_order: int
    is_primary: bool
    status: str
    raw_meta: dict[str, Any] | None
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsBrandAssetsProjectionResponse(PmsProjectionDisplayTable):
    count: int = Field(..., ge=0)
    brand_assets: list[PmsBrandAssetProjectionContract]


__all__ = ["PmsBrandAssetProjectionContract", "PmsBrandAssetsProjectionResponse"]
