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
