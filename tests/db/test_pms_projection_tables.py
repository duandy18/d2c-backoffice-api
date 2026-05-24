from __future__ import annotations

from sqlalchemy import inspect

from app.core.config import load_settings
from app.core.database import create_db_engine


def test_pms_projection_tables_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)
        table_names = set(inspector.get_table_names())

        assert "d2c_pms_product_projection" in table_names
        assert "d2c_pms_unit_projection" in table_names
        assert "d2c_pms_sku_code_projection" in table_names
        assert "d2c_pms_barcode_projection" in table_names
        assert "d2c_pms_projection_sync_runs" in table_names
        assert "d2c_pms_brand_asset_projection" in table_names
        assert "d2c_pms_brand_profile_projection" in table_names
        assert "d2c_pms_item_display_category_binding_projection" in table_names
        assert "d2c_pms_display_category_projection" in table_names
        assert "d2c_pms_item_asset_projection" in table_names
        assert "d2c_pms_item_content_projection" in table_names
    finally:
        engine.dispose()


def test_pms_projection_core_columns_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)

        product_columns = {
            column["name"] for column in inspector.get_columns("d2c_pms_product_projection")
        }
        unit_columns = {
            column["name"] for column in inspector.get_columns("d2c_pms_unit_projection")
        }
        sku_columns = {
            column["name"] for column in inspector.get_columns("d2c_pms_sku_code_projection")
        }
        barcode_columns = {
            column["name"] for column in inspector.get_columns("d2c_pms_barcode_projection")
        }
        sync_run_columns = {
            column["name"] for column in inspector.get_columns("d2c_pms_projection_sync_runs")
        }

        assert {
            "pms_item_id",
            "pms_sku",
            "item_name",
            "brand_name",
            "category_name",
            "pms_updated_at",
            "synced_at",
            "raw_payload",
        }.issubset(product_columns)

        assert {
            "pms_item_uom_id",
            "pms_item_id",
            "uom",
            "uom_name",
            "ratio_to_base",
            "is_base",
            "is_outbound_default",
            "raw_payload",
        }.issubset(unit_columns)

        assert {
            "pms_sku_code_id",
            "pms_item_id",
            "sku_code",
            "code_type",
            "is_primary",
            "is_active",
            "item_sku",
            "item_name",
            "raw_payload",
        }.issubset(sku_columns)

        assert {
            "pms_barcode_id",
            "pms_item_id",
            "pms_item_uom_id",
            "barcode",
            "active",
            "is_primary",
            "uom",
            "uom_name",
            "raw_payload",
        }.issubset(barcode_columns)

        assert {
            "sync_scope",
            "source_service",
            "source_endpoint",
            "status",
            "rows_fetched",
            "rows_upserted",
            "rows_deleted",
            "raw_summary",
        }.issubset(sync_run_columns)
    finally:
        engine.dispose()


def test_pms_projection_constraints_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)

        product_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_pms_product_projection")
        }
        unit_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_pms_unit_projection")
        }
        sku_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_pms_sku_code_projection")
        }
        barcode_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_pms_barcode_projection")
        }

        assert "uq_d2c_pms_product_projection_item_id" in product_unique_names
        assert "uq_d2c_pms_product_projection_sku" in product_unique_names
        assert "uq_d2c_pms_unit_projection_item_uom_id" in unit_unique_names
        assert "uq_d2c_pms_sku_code_projection_id" in sku_unique_names
        assert "uq_d2c_pms_sku_code_projection_code" in sku_unique_names
        assert "uq_d2c_pms_barcode_projection_id" in barcode_unique_names
        assert "uq_d2c_pms_barcode_projection_barcode" in barcode_unique_names
    finally:
        engine.dispose()


def test_pms_display_projection_core_columns_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)

        item_content_columns = {
            column["name"] for column in inspector.get_columns("d2c_pms_item_content_projection")
        }
        item_asset_columns = {
            column["name"] for column in inspector.get_columns("d2c_pms_item_asset_projection")
        }
        display_category_columns = {
            column["name"]
            for column in inspector.get_columns("d2c_pms_display_category_projection")
        }
        binding_columns = {
            column["name"]
            for column in inspector.get_columns("d2c_pms_item_display_category_binding_projection")
        }
        brand_profile_columns = {
            column["name"] for column in inspector.get_columns("d2c_pms_brand_profile_projection")
        }
        brand_asset_columns = {
            column["name"] for column in inspector.get_columns("d2c_pms_brand_asset_projection")
        }

        assert {
            "pms_content_id",
            "pms_item_id",
            "base_title",
            "base_description",
            "spec_params",
            "status",
            "raw_payload",
        }.issubset(item_content_columns)

        assert {
            "pms_asset_id",
            "pms_item_id",
            "asset_type",
            "usage_type",
            "source_type",
            "url",
            "is_primary",
            "status",
            "raw_payload",
        }.issubset(item_asset_columns)

        assert {
            "pms_display_category_id",
            "parent_id",
            "level",
            "category_code",
            "category_name",
            "path_code",
            "is_active",
            "is_leaf",
            "raw_payload",
        }.issubset(display_category_columns)

        assert {
            "pms_binding_id",
            "pms_item_id",
            "pms_display_category_id",
            "is_primary",
            "sort_order",
            "raw_payload",
        }.issubset(binding_columns)

        assert {
            "pms_profile_id",
            "brand_id",
            "display_name",
            "brand_story",
            "seo_title",
            "status",
            "raw_payload",
        }.issubset(brand_profile_columns)

        assert {
            "pms_asset_id",
            "brand_id",
            "asset_type",
            "usage_type",
            "url",
            "is_primary",
            "status",
            "raw_payload",
        }.issubset(brand_asset_columns)
    finally:
        engine.dispose()


def test_pms_display_projection_constraints_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)

        item_content_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_pms_item_content_projection")
        }
        item_asset_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_pms_item_asset_projection")
        }
        display_category_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints(
                "d2c_pms_display_category_projection"
            )
        }
        binding_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints(
                "d2c_pms_item_display_category_binding_projection"
            )
        }
        brand_profile_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_pms_brand_profile_projection")
        }
        brand_asset_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_pms_brand_asset_projection")
        }

        assert "uq_d2c_pms_item_content_pid" in item_content_unique_names
        assert "uq_d2c_pms_item_asset_pid" in item_asset_unique_names
        assert "uq_d2c_pms_disp_cat_pid" in display_category_unique_names
        assert "uq_d2c_pms_item_disp_bind_pid" in binding_unique_names
        assert "uq_d2c_pms_brand_profile_pid" in brand_profile_unique_names
        assert "uq_d2c_pms_brand_asset_pid" in brand_asset_unique_names
    finally:
        engine.dispose()
