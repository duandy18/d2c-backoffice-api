"""PMS item display category binding projection contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PmsItemDisplayCategoryBindingProjectionContract(BaseModel):
    id: int
    pms_binding_id: int
    pms_item_id: int
    pms_display_category_id: int
    item_sku: str | None
    item_name: str | None
    display_category_code: str | None
    display_category_name: str | None
    display_category_path_code: str | None
    is_primary: bool
    sort_order: int
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsItemDisplayCategoryBindingsProjectionResponse(BaseModel):
    count: int = Field(..., ge=0)
    item_display_category_bindings: list[PmsItemDisplayCategoryBindingProjectionContract]


__all__ = [
    "PmsItemDisplayCategoryBindingProjectionContract",
    "PmsItemDisplayCategoryBindingsProjectionResponse",
]
