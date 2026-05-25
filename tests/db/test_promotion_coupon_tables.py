from __future__ import annotations

from sqlalchemy import inspect

from app.core.config import load_settings
from app.core.database import create_db_engine


def test_promotion_rule_coupon_owner_tables_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)
        table_names = set(inspector.get_table_names())

        assert "d2c_promotion_rules" in table_names
        assert "d2c_promotions" not in table_names
        assert "d2c_promotion_targets" in table_names
        assert "d2c_coupons" in table_names
        assert "d2c_customer_coupons" not in table_names
    finally:
        engine.dispose()


def test_promotion_rule_coupon_owner_columns_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)

        rule_columns = {column["name"] for column in inspector.get_columns("d2c_promotion_rules")}
        target_columns = {
            column["name"] for column in inspector.get_columns("d2c_promotion_targets")
        }
        coupon_columns = {column["name"] for column in inspector.get_columns("d2c_coupons")}

        assert {
            "id",
            "promotion_code",
            "promotion_name",
            "promotion_type",
            "discount_type",
            "discount_value",
            "threshold_amount_cents",
            "status",
            "is_active",
            "display_badge",
        }.issubset(rule_columns)
        assert {
            "id",
            "promotion_rule_id",
            "target_type",
            "target_id",
            "target_code",
        }.issubset(target_columns)
        assert {
            "id",
            "coupon_code",
            "coupon_name",
            "promotion_rule_id",
            "coupon_type",
            "status",
            "is_active",
        }.issubset(coupon_columns)
    finally:
        engine.dispose()


def test_promotion_rule_coupon_owner_constraints_exist() -> None:
    engine = create_db_engine(load_settings())
    try:
        inspector = inspect(engine)

        rule_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_promotion_rules")
        }
        target_unique_names = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("d2c_promotion_targets")
        }
        coupon_unique_names = {
            constraint["name"] for constraint in inspector.get_unique_constraints("d2c_coupons")
        }

        assert "uq_d2c_promotion_rules_code" in rule_unique_names
        assert "uq_d2c_promo_targets_scope" in target_unique_names
        assert "uq_d2c_coupons_code" in coupon_unique_names

        target_fk_targets = {
            fk["referred_table"] for fk in inspector.get_foreign_keys("d2c_promotion_targets")
        }
        coupon_fk_targets = {
            fk["referred_table"] for fk in inspector.get_foreign_keys("d2c_coupons")
        }

        assert target_fk_targets == {"d2c_promotion_rules"}
        assert coupon_fk_targets == {"d2c_promotion_rules"}
    finally:
        engine.dispose()
