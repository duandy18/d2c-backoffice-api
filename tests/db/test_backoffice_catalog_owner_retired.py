from sqlalchemy import inspect

from app.core.config import load_settings
from app.core.database import Base, create_db_engine

RETIRED_TABLES = {
    "d2c_products",
    "d2c_product_skus",
    "d2c_product_categories",
    "d2c_units",
    "d2c_price_lists",
    "d2c_sku_prices",
}


def test_legacy_backoffice_catalog_owner_tables_are_retired_from_database() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)
        table_names = set(inspector.get_table_names())

        assert RETIRED_TABLES.isdisjoint(table_names)
    finally:
        engine.dispose()


def test_legacy_backoffice_catalog_owner_tables_are_not_registered_in_orm_metadata() -> None:
    assert RETIRED_TABLES.isdisjoint(Base.metadata.tables)


def test_current_backoffice_owner_tables_remain_available() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)
        table_names = set(inspector.get_table_names())

        assert {
            "d2c_pms_product_projection",
            "d2c_pms_unit_projection",
            "d2c_pms_sku_code_projection",
            "d2c_pms_barcode_projection",
            "d2c_product_listing_configs",
            "d2c_sku_listing_configs",
            "d2c_price_configs",
            "d2c_storefront_categories",
            "d2c_storefront_category_bindings",
            "d2c_publish_versions",
        }.issubset(table_names)
    finally:
        engine.dispose()
