"""PMS item content projection contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.domains.pms_projection.contracts.display_table import PmsProjectionDisplayTable


class PmsItemContentProjectionContract(BaseModel):
    id: int
    pms_content_id: int
    pms_item_id: int
    item_sku: str | None
    item_name: str | None
    base_title: str | None
    base_description: str | None
    short_description: str | None
    spec_params: dict[str, Any] | list[Any] | None
    material_text: str | None
    ingredients_text: str | None
    dimensions_text: str | None
    weight_text: str | None
    safety_instructions: str | None
    usage_instructions: str | None
    storage_instructions: str | None
    status: str
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsItemContentsProjectionResponse(PmsProjectionDisplayTable):
    count: int = Field(..., ge=0)
    item_contents: list[PmsItemContentProjectionContract]


__all__ = ["PmsItemContentProjectionContract", "PmsItemContentsProjectionResponse"]
