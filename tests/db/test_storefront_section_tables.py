from sqlalchemy import inspect

from app.core.config import load_settings
from app.core.database import create_engine


def test_storefront_section_owner_tables_exist() -> None:
    engine = create_engine(load_settings().database_url)
    try:
        table_names = set(inspect(engine).get_table_names())

        assert "d2c_storefront_sections" in table_names
        assert "d2c_storefront_section_layouts" in table_names
        assert "d2c_published_storefront_sections" in table_names
        assert "d2c_published_storefront_section_layouts" in table_names
    finally:
        engine.dispose()


def test_storefront_section_owner_columns_exist() -> None:
    engine = create_engine(load_settings().database_url)
    try:
        inspector = inspect(engine)
        section_columns = {
            column["name"] for column in inspector.get_columns("d2c_storefront_sections")
        }
        layout_columns = {
            column["name"] for column in inspector.get_columns("d2c_storefront_section_layouts")
        }

        assert {
            "section_code",
            "section_type",
            "group_id",
            "title",
            "sort_order",
            "display_status",
            "is_active",
        }.issubset(section_columns)
        assert {
            "section_id",
            "display_type",
            "columns_desktop",
            "columns_tablet",
            "columns_mobile",
            "card_size",
            "image_ratio",
            "show_promotion_badge",
            "show_sales_summary",
            "show_review_summary",
            "show_compare_price",
            "show_quantity_stepper",
            "max_items",
        }.issubset(layout_columns)
    finally:
        engine.dispose()

def test_storefront_section_position_tables_and_columns_exist() -> None:
    engine = create_engine(load_settings().database_url)
    try:
        inspector = inspect(engine)
        table_names = set(inspector.get_table_names())

        assert "d2c_storefront_section_positions" in table_names
        assert "d2c_published_storefront_section_positions" in table_names

        owner_columns = {
            column["name"]
            for column in inspector.get_columns("d2c_storefront_section_positions")
        }
        published_columns = {
            column["name"]
            for column in inspector.get_columns("d2c_published_storefront_section_positions")
        }

        assert {
            "section_id",
            "offer_id",
            "position_code",
            "sort_order",
            "position_type",
            "is_featured",
            "visible_from",
            "visible_until",
            "is_active",
            "source_type",
            "source_ref",
        }.issubset(owner_columns)
        assert {
            "publish_version",
            "section_code",
            "position_code",
            "offer_code",
            "sort_order",
            "position_type",
            "is_featured",
            "visible_from",
            "visible_until",
            "is_active",
            "published_at",
            "source_position_id",
            "raw_payload",
        }.issubset(published_columns)
    finally:
        engine.dispose()
