from __future__ import annotations

from sqlalchemy import inspect

from app.core.config import load_settings
from app.core.database import create_db_engine


def test_listing_pricing_publish_tables_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)
        table_names = set(inspector.get_table_names())

        assert "d2c_product_listing_configs" in table_names
        assert "d2c_sku_listing_configs" in table_names
        assert "d2c_price_configs" in table_names
        assert "d2c_storefront_categories" in table_names
        assert "d2c_storefront_category_bindings" in table_names
        assert "d2c_publish_versions" in table_names
    finally:
        engine.dispose()


def test_listing_pricing_publish_core_columns_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)

        product_columns = {
            column["name"] for column in inspector.get_columns("d2c_product_listing_configs")
        }
        sku_columns = {
            column["name"] for column in inspector.get_columns("d2c_sku_listing_configs")
        }
        price_columns = {column["name"] for column in inspector.get_columns("d2c_price_configs")}
        category_columns = {
            column["name"] for column in inspector.get_columns("d2c_storefront_categories")
        }
        binding_columns = {
            column["name"] for column in inspector.get_columns("d2c_storefront_category_bindings")
        }
        publish_columns = {
            column["name"] for column in inspector.get_columns("d2c_publish_versions")
        }

        assert {
            "pms_item_id",
            "pms_sku",
            "listing_code",
            "display_name",
            "listing_status",
            "display_status",
            "sell_status",
        }.issubset(product_columns)

        assert {
            "product_listing_config_id",
            "pms_item_id",
            "pms_sku_code_id",
            "pms_item_uom_id",
            "pms_barcode_id",
            "sku_display_name",
            "listing_status",
        }.issubset(sku_columns)

        assert {
            "sku_listing_config_id",
            "price_config_code",
            "channel",
            "currency",
            "price_cents",
            "compare_at_price_cents",
            "effective_from",
            "effective_until",
        }.issubset(price_columns)

        assert {
            "category_code",
            "category_name",
            "parent_category_id",
            "level",
            "display_status",
            "sort_order",
        }.issubset(category_columns)

        assert {
            "product_listing_config_id",
            "storefront_category_id",
            "is_primary",
            "sort_order",
        }.issubset(binding_columns)

        assert {
            "publish_version",
            "publish_scope",
            "status",
            "source",
            "started_at",
            "published_at",
            "published_by",
        }.issubset(publish_columns)
    finally:
        engine.dispose()


def test_listing_pricing_publish_constraints_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)

        product_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_product_listing_configs")
        }
        sku_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_sku_listing_configs")
        }
        price_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_price_configs")
        }
        category_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_storefront_categories")
        }
        binding_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_storefront_category_bindings")
        }
        publish_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_publish_versions")
        }

        assert "uq_d2c_product_listing_configs_pms_item_id" in product_unique_names
        assert "uq_d2c_product_listing_configs_listing_code" in product_unique_names
        assert "uq_d2c_sku_listing_configs_sku_code_uom" in sku_unique_names
        assert "uq_d2c_price_configs_code" in price_unique_names
        assert "uq_d2c_storefront_categories_code" in category_unique_names
        assert "uq_d2c_storefront_category_bindings_product_category" in binding_unique_names
        assert "uq_d2c_publish_versions_version" in publish_unique_names
    finally:
        engine.dispose()
