"""PMS product projection contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PmsProductProjectionContract(BaseModel):
    id: int
    pms_item_id: int
    pms_sku: str
    item_name: str
    item_spec: str | None
    enabled: bool
    supplier_id: int | None
    brand_id: int | None
    brand_code: str | None
    brand_name: str | None
    category_id: int | None
    category_code: str | None
    category_name: str | None
    category_path_code: str | None
    category_level: int | None
    category_is_leaf: bool | None
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsProductProjectionsResponse(BaseModel):
    count: int = Field(..., ge=0)
    products: list[PmsProductProjectionContract]


__all__ = ["PmsProductProjectionContract", "PmsProductProjectionsResponse"]
