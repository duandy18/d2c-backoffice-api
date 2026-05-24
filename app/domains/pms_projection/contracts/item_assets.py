"""PMS item asset projection contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PmsItemAssetProjectionContract(BaseModel):
    id: int
    pms_asset_id: int
    pms_item_id: int
    item_sku: str | None
    item_name: str | None
    asset_type: str
    usage_type: str
    source_type: str
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


class PmsItemAssetsProjectionResponse(BaseModel):
    count: int = Field(..., ge=0)
    item_assets: list[PmsItemAssetProjectionContract]


__all__ = ["PmsItemAssetProjectionContract", "PmsItemAssetsProjectionResponse"]
