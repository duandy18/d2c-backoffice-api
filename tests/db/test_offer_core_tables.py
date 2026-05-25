from __future__ import annotations

from sqlalchemy import inspect, text

from app.core.config import load_settings
from app.core.database import create_db_engine


def test_offer_core_tables_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)
        table_names = set(inspector.get_table_names())

        assert {
            "d2c_groups",
            "d2c_offers",
            "d2c_offer_components",
            "d2c_offer_prices",
            "d2c_offer_positions",
        }.issubset(table_names)
    finally:
        engine.dispose()


def test_offer_core_columns_and_seed_groups_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)

        group_columns = {column["name"] for column in inspector.get_columns("d2c_groups")}
        offer_columns = {column["name"] for column in inspector.get_columns("d2c_offers")}
        component_columns = {
            column["name"] for column in inspector.get_columns("d2c_offer_components")
        }
        price_columns = {column["name"] for column in inspector.get_columns("d2c_offer_prices")}
        position_columns = {
            column["name"] for column in inspector.get_columns("d2c_offer_positions")
        }

        assert {
            "group_code",
            "group_name",
            "group_kind",
            "sort_order",
            "display_status",
            "is_active",
            "source_type",
        }.issubset(group_columns)
        assert {
            "offer_code",
            "offer_type",
            "title",
            "image_url",
            "display_status",
            "sell_status",
            "publish_status",
        }.issubset(offer_columns)
        assert {
            "offer_id",
            "component_no",
            "pms_item_id",
            "pms_sku_code_id",
            "pms_item_uom_id",
            "quantity",
        }.issubset(component_columns)
        assert {"offer_id", "price_code", "price_cents", "currency", "is_active"}.issubset(
            price_columns
        )
        assert {
            "position_code",
            "group_id",
            "offer_id",
            "sort_order",
            "position_source",
            "is_active",
        }.issubset(position_columns)

        with engine.connect() as connection:
            rows = (
                connection.execute(
                    text(
                        """
                    SELECT group_code
                    FROM d2c_groups
                    ORDER BY sort_order
                    """
                    )
                )
                .mappings()
                .all()
            )

        group_codes = {row["group_code"] for row in rows}
        assert {
            "all",
            "cat_food",
            "cat_litter",
            "cat_canned",
            "cat_treats",
            "cat_supplies",
            "new_arrivals",
            "hot_rank",
            "bundles",
        }.issubset(group_codes)
    finally:
        engine.dispose()
