"""PMS display category projection contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PmsDisplayCategoryProjectionContract(BaseModel):
    id: int
    pms_display_category_id: int
    parent_id: int | None
    level: int
    category_code: str
    category_name: str
    display_name: str | None
    path_code: str
    description: str | None
    image_url: str | None
    sort_order: int
    is_active: bool
    is_leaf: bool
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsDisplayCategoriesProjectionResponse(BaseModel):
    count: int = Field(..., ge=0)
    display_categories: list[PmsDisplayCategoryProjectionContract]


__all__ = ["PmsDisplayCategoriesProjectionResponse", "PmsDisplayCategoryProjectionContract"]
