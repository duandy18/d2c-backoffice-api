from __future__ import annotations

from sqlalchemy import inspect

from app.core.config import load_settings
from app.core.database import create_db_engine


def test_published_snapshot_terminal_tables_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)
        table_names = set(inspector.get_table_names())

        assert {
            "d2c_published_groups",
            "d2c_published_offers",
            "d2c_published_offer_components",
            "d2c_published_offer_prices",
            "d2c_published_offer_positions",
            "d2c_published_promotion_rules",
            "d2c_published_promotion_targets",
            "d2c_published_coupons",
        }.issubset(table_names)
    finally:
        engine.dispose()


def test_published_snapshot_terminal_columns_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)

        group_columns = {column["name"] for column in inspector.get_columns("d2c_published_groups")}
        offer_columns = {column["name"] for column in inspector.get_columns("d2c_published_offers")}
        component_columns = {
            column["name"] for column in inspector.get_columns("d2c_published_offer_components")
        }
        price_columns = {
            column["name"] for column in inspector.get_columns("d2c_published_offer_prices")
        }
        position_columns = {
            column["name"] for column in inspector.get_columns("d2c_published_offer_positions")
        }
        rule_columns = {
            column["name"] for column in inspector.get_columns("d2c_published_promotion_rules")
        }
        target_columns = {
            column["name"] for column in inspector.get_columns("d2c_published_promotion_targets")
        }
        coupon_columns = {
            column["name"] for column in inspector.get_columns("d2c_published_coupons")
        }

        assert {"publish_version", "group_code", "group_name", "group_kind"}.issubset(group_columns)
        assert {"publish_version", "offer_code", "offer_type", "title"}.issubset(offer_columns)
        assert {
            "publish_version",
            "offer_code",
            "component_no",
            "pms_item_id",
            "sku_code",
            "quantity",
        }.issubset(component_columns)
        assert {"publish_version", "offer_code", "price_code", "price_cents"}.issubset(
            price_columns
        )
        assert {"publish_version", "position_code", "group_code", "offer_code"}.issubset(
            position_columns
        )
        assert {
            "publish_version",
            "promotion_code",
            "promotion_name",
            "threshold_amount_cents",
        }.issubset(rule_columns)
        assert {"publish_version", "promotion_code", "target_type"}.issubset(target_columns)
        assert {"publish_version", "coupon_code", "coupon_name", "promotion_code"}.issubset(
            coupon_columns
        )
    finally:
        engine.dispose()

def test_published_storefront_section_position_snapshot_columns_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)
        table_names = set(inspector.get_table_names())

        assert "d2c_published_storefront_section_positions" in table_names

        columns = {
            column["name"]
            for column in inspector.get_columns("d2c_published_storefront_section_positions")
        }
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
        }.issubset(columns)
    finally:
        engine.dispose()
