"""PMS projection services."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.pms_projection_contract import (
    PmsBarcodeProjectionContract,
    PmsBarcodeProjectionsResponse,
    PmsBrandAssetProjectionContract,
    PmsBrandAssetsProjectionResponse,
    PmsBrandProfileProjectionContract,
    PmsBrandProfilesProjectionResponse,
    PmsDisplayCategoriesProjectionResponse,
    PmsDisplayCategoryProjectionContract,
    PmsItemAssetProjectionContract,
    PmsItemAssetsProjectionResponse,
    PmsItemContentProjectionContract,
    PmsItemContentsProjectionResponse,
    PmsItemDisplayCategoryBindingProjectionContract,
    PmsItemDisplayCategoryBindingsProjectionResponse,
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
from app.domains.pms_projection.repos.pms_projection_repo import (
    list_barcode_projections,
    list_brand_asset_projections,
    list_brand_profile_projections,
    list_display_category_projections,
    list_item_asset_projections,
    list_item_content_projections,
    list_item_display_category_binding_projections,
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


def _build_item_content(row: PmsItemContentProjection) -> PmsItemContentProjectionContract:
    return PmsItemContentProjectionContract(
        id=row.id,
        pms_content_id=row.pms_content_id,
        pms_item_id=row.pms_item_id,
        base_title=row.base_title,
        base_description=row.base_description,
        short_description=row.short_description,
        spec_params=row.spec_params,
        material_text=row.material_text,
        ingredients_text=row.ingredients_text,
        dimensions_text=row.dimensions_text,
        weight_text=row.weight_text,
        safety_instructions=row.safety_instructions,
        usage_instructions=row.usage_instructions,
        storage_instructions=row.storage_instructions,
        status=row.status,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_item_content_projections(session: Session) -> PmsItemContentsProjectionResponse:
    rows = [_build_item_content(row) for row in list_item_content_projections(session)]
    return PmsItemContentsProjectionResponse(count=len(rows), item_contents=rows)


def _build_item_asset(row: PmsItemAssetProjection) -> PmsItemAssetProjectionContract:
    return PmsItemAssetProjectionContract(
        id=row.id,
        pms_asset_id=row.pms_asset_id,
        pms_item_id=row.pms_item_id,
        asset_type=row.asset_type,
        usage_type=row.usage_type,
        source_type=row.source_type,
        object_key=row.object_key,
        url=row.url,
        alt_text=row.alt_text,
        sort_order=row.sort_order,
        is_primary=row.is_primary,
        status=row.status,
        raw_meta=row.raw_meta,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_item_asset_projections(session: Session) -> PmsItemAssetsProjectionResponse:
    rows = [_build_item_asset(row) for row in list_item_asset_projections(session)]
    return PmsItemAssetsProjectionResponse(count=len(rows), item_assets=rows)


def _build_display_category(
    row: PmsDisplayCategoryProjection,
) -> PmsDisplayCategoryProjectionContract:
    return PmsDisplayCategoryProjectionContract(
        id=row.id,
        pms_display_category_id=row.pms_display_category_id,
        parent_id=row.parent_id,
        level=row.level,
        category_code=row.category_code,
        category_name=row.category_name,
        display_name=row.display_name,
        path_code=row.path_code,
        description=row.description,
        image_url=row.image_url,
        sort_order=row.sort_order,
        is_active=row.is_active,
        is_leaf=row.is_leaf,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_display_category_projections(
    session: Session,
) -> PmsDisplayCategoriesProjectionResponse:
    rows = [_build_display_category(row) for row in list_display_category_projections(session)]
    return PmsDisplayCategoriesProjectionResponse(count=len(rows), display_categories=rows)


def _build_item_display_category_binding(
    row: PmsItemDisplayCategoryBindingProjection,
) -> PmsItemDisplayCategoryBindingProjectionContract:
    return PmsItemDisplayCategoryBindingProjectionContract(
        id=row.id,
        pms_binding_id=row.pms_binding_id,
        pms_item_id=row.pms_item_id,
        pms_display_category_id=row.pms_display_category_id,
        is_primary=row.is_primary,
        sort_order=row.sort_order,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_item_display_category_binding_projections(
    session: Session,
) -> PmsItemDisplayCategoryBindingsProjectionResponse:
    rows = [
        _build_item_display_category_binding(row)
        for row in list_item_display_category_binding_projections(session)
    ]
    return PmsItemDisplayCategoryBindingsProjectionResponse(
        count=len(rows),
        item_display_category_bindings=rows,
    )


def _build_brand_profile(row: PmsBrandProfileProjection) -> PmsBrandProfileProjectionContract:
    return PmsBrandProfileProjectionContract(
        id=row.id,
        pms_profile_id=row.pms_profile_id,
        brand_id=row.brand_id,
        display_name=row.display_name,
        official_name=row.official_name,
        brand_story=row.brand_story,
        country_or_region=row.country_or_region,
        website_url=row.website_url,
        seo_title=row.seo_title,
        seo_description=row.seo_description,
        status=row.status,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_brand_profile_projections(session: Session) -> PmsBrandProfilesProjectionResponse:
    rows = [_build_brand_profile(row) for row in list_brand_profile_projections(session)]
    return PmsBrandProfilesProjectionResponse(count=len(rows), brand_profiles=rows)


def _build_brand_asset(row: PmsBrandAssetProjection) -> PmsBrandAssetProjectionContract:
    return PmsBrandAssetProjectionContract(
        id=row.id,
        pms_asset_id=row.pms_asset_id,
        brand_id=row.brand_id,
        asset_type=row.asset_type,
        usage_type=row.usage_type,
        object_key=row.object_key,
        url=row.url,
        alt_text=row.alt_text,
        sort_order=row.sort_order,
        is_primary=row.is_primary,
        status=row.status,
        raw_meta=row.raw_meta,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_brand_asset_projections(session: Session) -> PmsBrandAssetsProjectionResponse:
    rows = [_build_brand_asset(row) for row in list_brand_asset_projections(session)]
    return PmsBrandAssetsProjectionResponse(count=len(rows), brand_assets=rows)


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
