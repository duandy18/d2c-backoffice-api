"""PMS SKU code projection contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.domains.pms_projection.contracts.display_table import PmsProjectionDisplayTable


class PmsSkuCodeProjectionContract(BaseModel):
    id: int
    pms_sku_code_id: int
    pms_item_id: int
    sku_code: str
    code_type: str
    is_primary: bool
    is_active: bool
    effective_from: datetime | None
    effective_to: datetime | None
    remark: str | None
    item_sku: str
    item_name: str
    item_enabled: bool
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsSkuCodeProjectionsResponse(PmsProjectionDisplayTable):
    count: int = Field(..., ge=0)
    sku_codes: list[PmsSkuCodeProjectionContract]


__all__ = ["PmsSkuCodeProjectionContract", "PmsSkuCodeProjectionsResponse"]
