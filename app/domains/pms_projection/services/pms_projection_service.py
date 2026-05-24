"""PMS projection services."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.pms_projection_contract import (
    PmsBarcodeProjectionContract,
    PmsBarcodeProjectionsResponse,
    PmsProductProjectionContract,
    PmsProductProjectionsResponse,
    PmsProjectionHealthResponse,
    PmsProjectionSyncRunContract,
    PmsProjectionSyncRunsResponse,
    PmsSkuCodeProjectionContract,
    PmsSkuCodeProjectionsResponse,
    PmsUnitProjectionContract,
    PmsUnitProjectionsResponse,
)
from app.domains.pms_projection.models.pms_projection import (
    PmsBarcodeProjection,
    PmsProductProjection,
    PmsProjectionSyncRun,
    PmsSkuCodeProjection,
    PmsUnitProjection,
)
from app.domains.pms_projection.repos.pms_projection_repo import (
    list_barcode_projections,
    list_product_projections,
    list_projection_sync_runs,
    list_sku_code_projections,
    list_unit_projections,
)


def get_pms_projection_health() -> PmsProjectionHealthResponse:
    return PmsProjectionHealthResponse(
        status="ok",
        module="pms_projection",
        surface="merchant_read",
    )


def _build_product(row: PmsProductProjection) -> PmsProductProjectionContract:
    return PmsProductProjectionContract(
        id=row.id,
        pms_item_id=row.pms_item_id,
        pms_sku=row.pms_sku,
        item_name=row.item_name,
        item_spec=row.item_spec,
        enabled=row.enabled,
        supplier_id=row.supplier_id,
        brand_id=row.brand_id,
        brand_code=row.brand_code,
        brand_name=row.brand_name,
        category_id=row.category_id,
        category_code=row.category_code,
        category_name=row.category_name,
        category_path_code=row.category_path_code,
        category_level=row.category_level,
        category_is_leaf=row.category_is_leaf,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_product_projections(session: Session) -> PmsProductProjectionsResponse:
    rows = [_build_product(row) for row in list_product_projections(session)]
    return PmsProductProjectionsResponse(count=len(rows), products=rows)


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
    return PmsUnitProjectionsResponse(count=len(rows), units=rows)


def _build_sku_code(row: PmsSkuCodeProjection) -> PmsSkuCodeProjectionContract:
    return PmsSkuCodeProjectionContract(
        id=row.id,
        pms_sku_code_id=row.pms_sku_code_id,
        pms_item_id=row.pms_item_id,
        sku_code=row.sku_code,
        code_type=row.code_type,
        is_primary=row.is_primary,
        is_active=row.is_active,
        effective_from=row.effective_from,
        effective_to=row.effective_to,
        remark=row.remark,
        item_sku=row.item_sku,
        item_name=row.item_name,
        item_enabled=row.item_enabled,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_sku_code_projections(session: Session) -> PmsSkuCodeProjectionsResponse:
    rows = [_build_sku_code(row) for row in list_sku_code_projections(session)]
    return PmsSkuCodeProjectionsResponse(count=len(rows), sku_codes=rows)


def _build_barcode(row: PmsBarcodeProjection) -> PmsBarcodeProjectionContract:
    return PmsBarcodeProjectionContract(
        id=row.id,
        pms_barcode_id=row.pms_barcode_id,
        pms_item_id=row.pms_item_id,
        pms_item_uom_id=row.pms_item_uom_id,
        barcode=row.barcode,
        symbology=row.symbology,
        active=row.active,
        is_primary=row.is_primary,
        uom=row.uom,
        uom_name=row.uom_name,
        ratio_to_base=row.ratio_to_base,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_barcode_projections(session: Session) -> PmsBarcodeProjectionsResponse:
    rows = [_build_barcode(row) for row in list_barcode_projections(session)]
    return PmsBarcodeProjectionsResponse(count=len(rows), barcodes=rows)


def _build_sync_run(row: PmsProjectionSyncRun) -> PmsProjectionSyncRunContract:
    return PmsProjectionSyncRunContract(
        id=row.id,
        sync_scope=row.sync_scope,
        source_service=row.source_service,
        source_base_url=row.source_base_url,
        source_endpoint=row.source_endpoint,
        status=row.status,
        started_at=row.started_at,
        finished_at=row.finished_at,
        requested_by=row.requested_by,
        rows_fetched=row.rows_fetched,
        rows_upserted=row.rows_upserted,
        rows_deleted=row.rows_deleted,
        error_code=row.error_code,
        error_message=row.error_message,
        raw_summary=row.raw_summary,
    )


def get_pms_projection_sync_runs(session: Session) -> PmsProjectionSyncRunsResponse:
    rows = [_build_sync_run(row) for row in list_projection_sync_runs(session)]
    return PmsProjectionSyncRunsResponse(count=len(rows), sync_runs=rows)
