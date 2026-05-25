from sqlalchemy import inspect

from app.core.config import load_settings
from app.core.database import create_engine


def test_client_presentation_owner_and_snapshot_tables_exist() -> None:
    engine = create_engine(load_settings().database_url)
    try:
        table_names = set(inspect(engine).get_table_names())

        assert {
            "d2c_client_pages",
            "d2c_client_regions",
            "d2c_client_block_types",
            "d2c_published_client_pages",
            "d2c_published_client_regions",
            "d2c_published_client_block_types",
        }.issubset(table_names)
    finally:
        engine.dispose()


def test_client_presentation_owner_columns_exist() -> None:
    engine = create_engine(load_settings().database_url)
    try:
        inspector = inspect(engine)

        page_columns = {column["name"] for column in inspector.get_columns("d2c_client_pages")}
        region_columns = {
            column["name"] for column in inspector.get_columns("d2c_client_regions")
        }
        block_columns = {
            column["name"] for column in inspector.get_columns("d2c_client_block_types")
        }

        assert {
            "page_code",
            "page_type",
            "route_path",
            "title",
            "seo_title",
            "seo_description",
            "display_status",
            "is_active",
        }.issubset(page_columns)
        assert {
            "page_id",
            "region_code",
            "region_type",
            "allowed_block_types",
            "is_required",
            "max_blocks",
        }.issubset(region_columns)
        assert {
            "block_type",
            "display_name",
            "renderer_key",
            "data_contract_version",
            "allowed_region_types",
            "allowed_content_types",
            "layout_schema",
            "slot_schema",
            "action_schema",
            "analytics_schema",
        }.issubset(block_columns)
    finally:
        engine.dispose()


def test_client_presentation_snapshot_columns_exist() -> None:
    engine = create_engine(load_settings().database_url)
    try:
        inspector = inspect(engine)

        page_columns = {
            column["name"] for column in inspector.get_columns("d2c_published_client_pages")
        }
        region_columns = {
            column["name"] for column in inspector.get_columns("d2c_published_client_regions")
        }
        block_columns = {
            column["name"]
            for column in inspector.get_columns("d2c_published_client_block_types")
        }

        assert {"publish_version", "page_code", "page_type", "route_path"}.issubset(
            page_columns
        )
        assert {
            "publish_version",
            "page_code",
            "region_code",
            "allowed_block_types",
        }.issubset(region_columns)
        assert {
            "publish_version",
            "block_type",
            "renderer_key",
            "layout_schema",
            "slot_schema",
        }.issubset(block_columns)
    finally:
        engine.dispose()
