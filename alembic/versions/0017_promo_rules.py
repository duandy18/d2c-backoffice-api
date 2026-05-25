"""promote_promotion_rules_terminal_model.

Revision ID: 0017_promo_rules
Revises: 0016_offer_core
Create Date: 2026-05-25
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0017_promo_rules"
down_revision: str | Sequence[str] | None = "0016_offer_core"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_index("ix_d2c_promotion_targets_target", table_name="d2c_promotion_targets")
    op.drop_index("ix_d2c_promotion_targets_promotion_id", table_name="d2c_promotion_targets")
    op.drop_table("d2c_promotion_targets")

    op.drop_index("ix_d2c_coupons_status", table_name="d2c_coupons")
    op.drop_index("ix_d2c_coupons_promotion_id", table_name="d2c_coupons")
    op.drop_index("ix_d2c_coupons_code", table_name="d2c_coupons")
    op.drop_table("d2c_coupons")

    op.drop_index("ix_d2c_promotions_type", table_name="d2c_promotions")
    op.drop_index("ix_d2c_promotions_status", table_name="d2c_promotions")
    op.drop_index("ix_d2c_promotions_code", table_name="d2c_promotions")
    op.drop_index("ix_d2c_promotions_active_range", table_name="d2c_promotions")
    op.drop_table("d2c_promotions")

    op.create_table(
        "d2c_promotion_rules",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("promotion_code", sa.String(length=64), nullable=False),
        sa.Column("promotion_name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("promotion_type", sa.String(length=32), nullable=False),
        sa.Column("discount_type", sa.String(length=32), nullable=False),
        sa.Column("discount_value", sa.Integer(), nullable=False),
        sa.Column("threshold_amount_cents", sa.Integer(), nullable=True),
        sa.Column("max_discount_cents", sa.Integer(), nullable=True),
        sa.Column("currency", sa.String(length=3), server_default="USD", nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), server_default="draft", nullable=False),
        sa.Column("priority", sa.Integer(), server_default="100", nullable=False),
        sa.Column("stackable", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("display_badge", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("discount_value > 0", name="ck_d2c_promo_rules_discount"),
        sa.CheckConstraint(
            "discount_type <> 'percentage' OR discount_value <= 100",
            name="ck_d2c_promo_rules_pct",
        ),
        sa.CheckConstraint(
            "threshold_amount_cents IS NULL OR threshold_amount_cents >= 0",
            name="ck_d2c_promo_rules_threshold",
        ),
        sa.CheckConstraint(
            "max_discount_cents IS NULL OR max_discount_cents >= 0",
            name="ck_d2c_promo_rules_max_discount",
        ),
        sa.CheckConstraint(
            "ends_at IS NULL OR starts_at IS NULL OR ends_at > starts_at",
            name="ck_d2c_promo_rules_range",
        ),
        sa.CheckConstraint("priority >= 0", name="ck_d2c_promo_rules_priority"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("promotion_code", name="uq_d2c_promotion_rules_code"),
    )
    op.create_index("ix_d2c_promo_rules_code", "d2c_promotion_rules", ["promotion_code"])
    op.create_index("ix_d2c_promo_rules_status", "d2c_promotion_rules", ["status"])
    op.create_index("ix_d2c_promo_rules_type", "d2c_promotion_rules", ["promotion_type"])
    op.create_index(
        "ix_d2c_promo_rules_active_range",
        "d2c_promotion_rules",
        ["is_active", "starts_at", "ends_at"],
    )

    op.create_table(
        "d2c_promotion_targets",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("promotion_rule_id", sa.BigInteger(), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_id", sa.BigInteger(), nullable=True),
        sa.Column("target_code", sa.String(length=96), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "target_type = 'all_store' OR target_id IS NOT NULL OR target_code IS NOT NULL",
            name="ck_d2c_promo_targets_present",
        ),
        sa.ForeignKeyConstraint(
            ["promotion_rule_id"],
            ["d2c_promotion_rules.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "promotion_rule_id",
            "target_type",
            "target_id",
            "target_code",
            name="uq_d2c_promo_targets_scope",
        ),
    )
    op.create_index("ix_d2c_promo_targets_rule", "d2c_promotion_targets", ["promotion_rule_id"])
    op.create_index(
        "ix_d2c_promo_targets_target",
        "d2c_promotion_targets",
        ["target_type", "target_id", "target_code"],
    )

    op.create_table(
        "d2c_coupons",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("coupon_code", sa.String(length=64), nullable=False),
        sa.Column("coupon_name", sa.String(length=160), nullable=False),
        sa.Column("promotion_rule_id", sa.BigInteger(), nullable=False),
        sa.Column("coupon_type", sa.String(length=32), nullable=False),
        sa.Column("total_limit", sa.Integer(), nullable=True),
        sa.Column("per_customer_limit", sa.Integer(), nullable=True),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), server_default="draft", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "total_limit IS NULL OR total_limit > 0",
            name="ck_d2c_coupons_total_limit_positive",
        ),
        sa.CheckConstraint(
            "per_customer_limit IS NULL OR per_customer_limit > 0",
            name="ck_d2c_coupons_per_customer_limit_positive",
        ),
        sa.CheckConstraint(
            "ends_at IS NULL OR starts_at IS NULL OR ends_at > starts_at",
            name="ck_d2c_coupons_effective_range_valid",
        ),
        sa.ForeignKeyConstraint(
            ["promotion_rule_id"],
            ["d2c_promotion_rules.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("coupon_code", name="uq_d2c_coupons_code"),
    )
    op.create_index("ix_d2c_coupons_code", "d2c_coupons", ["coupon_code"])
    op.create_index("ix_d2c_coupons_status", "d2c_coupons", ["status"])
    op.create_index("ix_d2c_coupons_rule", "d2c_coupons", ["promotion_rule_id"])


def downgrade() -> None:
    op.drop_index("ix_d2c_coupons_rule", table_name="d2c_coupons")
    op.drop_index("ix_d2c_coupons_status", table_name="d2c_coupons")
    op.drop_index("ix_d2c_coupons_code", table_name="d2c_coupons")
    op.drop_table("d2c_coupons")

    op.drop_index("ix_d2c_promo_targets_target", table_name="d2c_promotion_targets")
    op.drop_index("ix_d2c_promo_targets_rule", table_name="d2c_promotion_targets")
    op.drop_table("d2c_promotion_targets")

    op.drop_index("ix_d2c_promo_rules_active_range", table_name="d2c_promotion_rules")
    op.drop_index("ix_d2c_promo_rules_type", table_name="d2c_promotion_rules")
    op.drop_index("ix_d2c_promo_rules_status", table_name="d2c_promotion_rules")
    op.drop_index("ix_d2c_promo_rules_code", table_name="d2c_promotion_rules")
    op.drop_table("d2c_promotion_rules")

    op.create_table(
        "d2c_promotions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("promotion_code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("promotion_type", sa.String(length=32), nullable=False),
        sa.Column("discount_type", sa.String(length=32), nullable=False),
        sa.Column("discount_value", sa.Integer(), nullable=False),
        sa.Column("scope_type", sa.String(length=32), nullable=False),
        sa.Column("min_order_amount_cents", sa.Integer(), nullable=True),
        sa.Column("max_discount_cents", sa.Integer(), nullable=True),
        sa.Column("currency", sa.String(length=3), server_default="USD", nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), server_default="draft", nullable=False),
        sa.Column("priority", sa.Integer(), server_default="100", nullable=False),
        sa.Column("stackable", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("promotion_code", name="uq_d2c_promotions_code"),
    )
    op.create_index("ix_d2c_promotions_code", "d2c_promotions", ["promotion_code"])
    op.create_index("ix_d2c_promotions_status", "d2c_promotions", ["status"])
    op.create_index("ix_d2c_promotions_type", "d2c_promotions", ["promotion_type"])
    op.create_index(
        "ix_d2c_promotions_active_range",
        "d2c_promotions",
        ["is_active", "starts_at", "ends_at"],
    )

    op.create_table(
        "d2c_promotion_targets",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("promotion_id", sa.BigInteger(), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_id", sa.BigInteger(), nullable=True),
        sa.Column("target_code", sa.String(length=96), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["promotion_id"], ["d2c_promotions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "promotion_id",
            "target_type",
            "target_id",
            "target_code",
            name="uq_d2c_promotion_targets_scope",
        ),
    )
    op.create_index(
        "ix_d2c_promotion_targets_promotion_id",
        "d2c_promotion_targets",
        ["promotion_id"],
    )
    op.create_index(
        "ix_d2c_promotion_targets_target",
        "d2c_promotion_targets",
        ["target_type", "target_id", "target_code"],
    )

    op.create_table(
        "d2c_coupons",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("coupon_code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("promotion_id", sa.BigInteger(), nullable=False),
        sa.Column("coupon_type", sa.String(length=32), nullable=False),
        sa.Column("total_limit", sa.Integer(), nullable=True),
        sa.Column("per_customer_limit", sa.Integer(), nullable=True),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), server_default="draft", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["promotion_id"], ["d2c_promotions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("coupon_code", name="uq_d2c_coupons_code"),
    )
    op.create_index("ix_d2c_coupons_code", "d2c_coupons", ["coupon_code"])
    op.create_index("ix_d2c_coupons_promotion_id", "d2c_coupons", ["promotion_id"])
    op.create_index("ix_d2c_coupons_status", "d2c_coupons", ["status"])
