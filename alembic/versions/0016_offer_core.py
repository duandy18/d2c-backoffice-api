"""add_offer_group_position_terminal_models.

Revision ID: 0016_offer_core
Revises: 0015_pms_disp_fields
Create Date: 2026-05-25
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0016_offer_core"
down_revision: str | Sequence[str] | None = "0015_pms_disp_fields"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


DEFAULT_GROUPS = (
    ("all", "全部商品", "all", 10, "system"),
    ("cat_food", "猫粮", "category", 20, "manual"),
    ("cat_litter", "猫砂", "category", 30, "manual"),
    ("cat_canned", "猫罐头", "category", 40, "manual"),
    ("cat_treats", "猫条", "category", 50, "manual"),
    ("cat_supplies", "猫用品", "category", 60, "manual"),
    ("new_arrivals", "新品上线", "new_arrival", 70, "manual"),
    ("hot_rank", "热销排行", "hot_rank", 80, "manual"),
    ("bundles", "组合套餐", "bundle", 90, "manual"),
)


def upgrade() -> None:
    op.create_table(
        "d2c_groups",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("group_code", sa.String(length=96), nullable=False),
        sa.Column("group_name", sa.String(length=160), nullable=False),
        sa.Column("group_kind", sa.String(length=32), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("display_status", sa.String(length=32), server_default="visible", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("source_type", sa.String(length=32), server_default="manual", nullable=False),
        sa.Column("source_ref", sa.String(length=160), nullable=True),
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
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_groups_sort"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("group_code", name="uq_d2c_groups_code"),
    )
    op.create_index(
        "ix_d2c_groups_kind_status",
        "d2c_groups",
        ["group_kind", "display_status", "is_active"],
    )
    op.create_index("ix_d2c_groups_sort", "d2c_groups", ["sort_order"])

    op.create_table(
        "d2c_offers",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("offer_code", sa.String(length=96), nullable=False),
        sa.Column("offer_type", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("subtitle", sa.String(length=240), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("display_status", sa.String(length=32), server_default="hidden", nullable=False),
        sa.Column(
            "sell_status", sa.String(length=32), server_default="not_sellable", nullable=False
        ),
        sa.Column("publish_status", sa.String(length=32), server_default="draft", nullable=False),
        sa.Column("source_type", sa.String(length=32), server_default="manual", nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("visible_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("visible_until", sa.DateTime(timezone=True), nullable=True),
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
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_offers_sort"),
        sa.CheckConstraint(
            "visible_until IS NULL OR visible_from IS NULL OR visible_until > visible_from",
            name="ck_d2c_offers_visible_range",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("offer_code", name="uq_d2c_offers_code"),
    )
    op.create_index(
        "ix_d2c_offers_type_status",
        "d2c_offers",
        ["offer_type", "display_status", "sell_status"],
    )
    op.create_index("ix_d2c_offers_publish_status", "d2c_offers", ["publish_status"])

    op.create_table(
        "d2c_offer_components",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("offer_id", sa.BigInteger(), nullable=False),
        sa.Column("component_no", sa.Integer(), nullable=False),
        sa.Column("pms_item_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_sku", sa.String(length=128), nullable=False),
        sa.Column("pms_sku_code_id", sa.BigInteger(), nullable=False),
        sa.Column("sku_code", sa.String(length=128), nullable=False),
        sa.Column("pms_item_uom_id", sa.BigInteger(), nullable=False),
        sa.Column("uom_code", sa.String(length=32), nullable=False),
        sa.Column("uom_name", sa.String(length=80), nullable=False),
        sa.Column("pms_barcode_id", sa.BigInteger(), nullable=True),
        sa.Column("barcode", sa.String(length=128), nullable=True),
        sa.Column("quantity", sa.Numeric(18, 6), nullable=False),
        sa.Column("component_role", sa.String(length=32), server_default="primary", nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("required", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
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
        sa.CheckConstraint("quantity > 0", name="ck_d2c_offer_components_qty"),
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_offer_components_sort"),
        sa.ForeignKeyConstraint(["offer_id"], ["d2c_offers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["pms_item_id"],
            ["d2c_pms_product_projection.pms_item_id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["pms_sku_code_id"],
            ["d2c_pms_sku_code_projection.pms_sku_code_id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["pms_item_uom_id"],
            ["d2c_pms_unit_projection.pms_item_uom_id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["pms_barcode_id"],
            ["d2c_pms_barcode_projection.pms_barcode_id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("offer_id", "component_no", name="uq_d2c_offer_components_no"),
    )
    op.create_index("ix_d2c_offer_components_offer", "d2c_offer_components", ["offer_id"])
    op.create_index("ix_d2c_offer_components_pms_item", "d2c_offer_components", ["pms_item_id"])

    op.create_table(
        "d2c_offer_prices",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("offer_id", sa.BigInteger(), nullable=False),
        sa.Column("price_code", sa.String(length=96), nullable=False),
        sa.Column("channel", sa.String(length=32), server_default="storefront", nullable=False),
        sa.Column("currency", sa.String(length=3), server_default="USD", nullable=False),
        sa.Column("price_cents", sa.Integer(), nullable=False),
        sa.Column("compare_at_price_cents", sa.Integer(), nullable=True),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("effective_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("priority", sa.Integer(), server_default="100", nullable=False),
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
        sa.CheckConstraint("price_cents >= 0", name="ck_d2c_offer_prices_price"),
        sa.CheckConstraint("priority >= 0", name="ck_d2c_offer_prices_priority"),
        sa.CheckConstraint(
            "compare_at_price_cents IS NULL OR compare_at_price_cents >= price_cents",
            name="ck_d2c_offer_prices_compare",
        ),
        sa.CheckConstraint(
            "effective_until IS NULL OR effective_from IS NULL OR effective_until > effective_from",
            name="ck_d2c_offer_prices_range",
        ),
        sa.ForeignKeyConstraint(["offer_id"], ["d2c_offers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("price_code", name="uq_d2c_offer_prices_code"),
    )
    op.create_index(
        "ix_d2c_offer_prices_offer_active",
        "d2c_offer_prices",
        ["offer_id", "channel", "is_active"],
    )

    op.create_table(
        "d2c_offer_positions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("position_code", sa.String(length=120), nullable=False),
        sa.Column("group_id", sa.BigInteger(), nullable=False),
        sa.Column("offer_id", sa.BigInteger(), nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("position_source", sa.String(length=32), server_default="manual", nullable=False),
        sa.Column("is_featured", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("visible_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("visible_until", sa.DateTime(timezone=True), nullable=True),
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
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_offer_positions_sort"),
        sa.CheckConstraint(
            "visible_until IS NULL OR visible_from IS NULL OR visible_until > visible_from",
            name="ck_d2c_offer_positions_range",
        ),
        sa.ForeignKeyConstraint(["group_id"], ["d2c_groups.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["offer_id"], ["d2c_offers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("position_code", name="uq_d2c_offer_positions_code"),
        sa.UniqueConstraint("group_id", "offer_id", name="uq_d2c_offer_positions_group_offer"),
    )
    op.create_index(
        "ix_d2c_offer_positions_group_sort",
        "d2c_offer_positions",
        ["group_id", "sort_order"],
    )
    op.create_index("ix_d2c_offer_positions_offer", "d2c_offer_positions", ["offer_id"])

    groups_table = sa.table(
        "d2c_groups",
        sa.column("group_code", sa.String),
        sa.column("group_name", sa.String),
        sa.column("group_kind", sa.String),
        sa.column("sort_order", sa.Integer),
        sa.column("display_status", sa.String),
        sa.column("is_active", sa.Boolean),
        sa.column("source_type", sa.String),
    )
    op.bulk_insert(
        groups_table,
        [
            {
                "group_code": code,
                "group_name": name,
                "group_kind": kind,
                "sort_order": sort_order,
                "display_status": "visible",
                "is_active": True,
                "source_type": source_type,
            }
            for code, name, kind, sort_order, source_type in DEFAULT_GROUPS
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_d2c_offer_positions_offer", table_name="d2c_offer_positions")
    op.drop_index("ix_d2c_offer_positions_group_sort", table_name="d2c_offer_positions")
    op.drop_table("d2c_offer_positions")

    op.drop_index("ix_d2c_offer_prices_offer_active", table_name="d2c_offer_prices")
    op.drop_table("d2c_offer_prices")

    op.drop_index("ix_d2c_offer_components_pms_item", table_name="d2c_offer_components")
    op.drop_index("ix_d2c_offer_components_offer", table_name="d2c_offer_components")
    op.drop_table("d2c_offer_components")

    op.drop_index("ix_d2c_offers_publish_status", table_name="d2c_offers")
    op.drop_index("ix_d2c_offers_type_status", table_name="d2c_offers")
    op.drop_table("d2c_offers")

    op.drop_index("ix_d2c_groups_sort", table_name="d2c_groups")
    op.drop_index("ix_d2c_groups_kind_status", table_name="d2c_groups")
    op.drop_table("d2c_groups")
