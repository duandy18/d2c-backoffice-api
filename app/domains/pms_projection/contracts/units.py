"""PMS unit projection contracts."""

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class PmsUnitProjectionContract(BaseModel):
    id: int
    pms_item_uom_id: int
    pms_item_id: int
    uom: str
    uom_name: str
    display_name: str | None
    ratio_to_base: Decimal
    net_weight_kg: Decimal | None
    is_base: bool
    is_purchase_default: bool
    is_inbound_default: bool
    is_outbound_default: bool
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsUnitProjectionsResponse(BaseModel):
    count: int = Field(..., ge=0)
    units: list[PmsUnitProjectionContract]


__all__ = ["PmsUnitProjectionContract", "PmsUnitProjectionsResponse"]
