"""PMS projection repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.pms_projection import (
    PmsBarcodeProjection,
    PmsBrandAssetProjection,
    PmsBrandProfileProjection,
    PmsDisplayCategoryProjection,
    PmsItemAssetProjection,
    PmsItemContentProjection,
    PmsItemDisplayCategoryBindingProjection,
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


def list_item_content_projections(session: Session) -> list[PmsItemContentProjection]:
    statement = select(PmsItemContentProjection).order_by(
        PmsItemContentProjection.pms_item_id,
        PmsItemContentProjection.pms_content_id,
    )
    return list(session.scalars(statement).all())


def list_item_asset_projections(session: Session) -> list[PmsItemAssetProjection]:
    statement = select(PmsItemAssetProjection).order_by(
        PmsItemAssetProjection.pms_item_id,
        PmsItemAssetProjection.usage_type,
        PmsItemAssetProjection.sort_order,
        PmsItemAssetProjection.pms_asset_id,
    )
    return list(session.scalars(statement).all())


def list_display_category_projections(session: Session) -> list[PmsDisplayCategoryProjection]:
    statement = select(PmsDisplayCategoryProjection).order_by(
        PmsDisplayCategoryProjection.level,
        PmsDisplayCategoryProjection.sort_order,
        PmsDisplayCategoryProjection.pms_display_category_id,
    )
    return list(session.scalars(statement).all())


def list_item_display_category_binding_projections(
    session: Session,
) -> list[PmsItemDisplayCategoryBindingProjection]:
    statement = select(PmsItemDisplayCategoryBindingProjection).order_by(
        PmsItemDisplayCategoryBindingProjection.pms_item_id,
        PmsItemDisplayCategoryBindingProjection.is_primary.desc(),
        PmsItemDisplayCategoryBindingProjection.sort_order,
        PmsItemDisplayCategoryBindingProjection.pms_binding_id,
    )
    return list(session.scalars(statement).all())


def list_brand_profile_projections(session: Session) -> list[PmsBrandProfileProjection]:
    statement = select(PmsBrandProfileProjection).order_by(
        PmsBrandProfileProjection.brand_id,
        PmsBrandProfileProjection.pms_profile_id,
    )
    return list(session.scalars(statement).all())


def list_brand_asset_projections(session: Session) -> list[PmsBrandAssetProjection]:
    statement = select(PmsBrandAssetProjection).order_by(
        PmsBrandAssetProjection.brand_id,
        PmsBrandAssetProjection.usage_type,
        PmsBrandAssetProjection.sort_order,
        PmsBrandAssetProjection.pms_asset_id,
    )
    return list(session.scalars(statement).all())


def list_projection_sync_runs(session: Session) -> list[PmsProjectionSyncRun]:
    statement = select(PmsProjectionSyncRun).order_by(PmsProjectionSyncRun.id.desc())
    return list(session.scalars(statement).all())
