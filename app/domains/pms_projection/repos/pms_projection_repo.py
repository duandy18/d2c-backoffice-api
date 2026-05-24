"""PMS projection repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.pms_projection import (
    PmsBarcodeProjection,
    PmsProductProjection,
    PmsProjectionSyncRun,
    PmsSkuCodeProjection,
    PmsUnitProjection,
)


def list_product_projections(session: Session) -> list[PmsProductProjection]:
    statement = select(PmsProductProjection).order_by(PmsProductProjection.pms_item_id)
    return list(session.scalars(statement).all())


def list_unit_projections(session: Session) -> list[PmsUnitProjection]:
    statement = select(PmsUnitProjection).order_by(
        PmsUnitProjection.pms_item_id,
        PmsUnitProjection.pms_item_uom_id,
    )
    return list(session.scalars(statement).all())


def list_sku_code_projections(session: Session) -> list[PmsSkuCodeProjection]:
    statement = select(PmsSkuCodeProjection).order_by(
        PmsSkuCodeProjection.pms_item_id,
        PmsSkuCodeProjection.is_primary.desc(),
        PmsSkuCodeProjection.pms_sku_code_id,
    )
    return list(session.scalars(statement).all())


def list_barcode_projections(session: Session) -> list[PmsBarcodeProjection]:
    statement = select(PmsBarcodeProjection).order_by(
        PmsBarcodeProjection.pms_item_id,
        PmsBarcodeProjection.is_primary.desc(),
        PmsBarcodeProjection.pms_barcode_id,
    )
    return list(session.scalars(statement).all())


def list_projection_sync_runs(session: Session) -> list[PmsProjectionSyncRun]:
    statement = select(PmsProjectionSyncRun).order_by(PmsProjectionSyncRun.id.desc())
    return list(session.scalars(statement).all())
