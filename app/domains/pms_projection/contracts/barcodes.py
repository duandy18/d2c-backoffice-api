"""PMS barcode projection contracts."""

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field

from app.domains.pms_projection.contracts.display_table import PmsProjectionDisplayTable


class PmsBarcodeProjectionContract(BaseModel):
    id: int
    pms_barcode_id: int
    pms_item_id: int
    pms_item_uom_id: int
    barcode: str
    symbology: str | None
    active: bool
    is_primary: bool
    uom: str
    uom_name: str
    ratio_to_base: Decimal
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsBarcodeProjectionsResponse(PmsProjectionDisplayTable):
    count: int = Field(..., ge=0)
    barcodes: list[PmsBarcodeProjectionContract]


__all__ = ["PmsBarcodeProjectionContract", "PmsBarcodeProjectionsResponse"]
