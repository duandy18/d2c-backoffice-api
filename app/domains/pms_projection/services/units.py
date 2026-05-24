"""PMS unit projection service."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.units import (
    PmsUnitProjectionContract,
    PmsUnitProjectionsResponse,
)
from app.domains.pms_projection.models.units import PmsUnitProjection
from app.domains.pms_projection.repos.units import list_unit_projections
from app.domains.pms_projection.services.display_table import build_projection_display_table


def _build_unit(row: PmsUnitProjection) -> PmsUnitProjectionContract:
    return PmsUnitProjectionContract(
        id=row.id,
        pms_item_uom_id=row.pms_item_uom_id,
        pms_item_id=row.pms_item_id,
        uom=row.uom,
        uom_name=row.uom_name,
        display_name=row.display_name,
        ratio_to_base=row.ratio_to_base,
        net_weight_kg=row.net_weight_kg,
        is_base=row.is_base,
        is_purchase_default=row.is_purchase_default,
        is_inbound_default=row.is_inbound_default,
        is_outbound_default=row.is_outbound_default,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_unit_projections(session: Session) -> PmsUnitProjectionsResponse:
    rows = [_build_unit(row) for row in list_unit_projections(session)]
    return PmsUnitProjectionsResponse(
        count=len(rows),
        units=rows,
        **build_projection_display_table("units", rows),
    )


__all__ = ["get_pms_unit_projections"]
