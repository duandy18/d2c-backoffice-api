# ruff: noqa: E501
"""add PMS projection and listing config tables.

Revision ID: 0005_bo_listing
Revises: 0004_bo_promotions
Create Date: 2026-05-24
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0005_bo_listing"
down_revision: str | Sequence[str] | None = "0004_bo_promotions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "d2c_pms_product_projection",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("pms_item_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_sku", sa.String(length=128), nullable=False),
        sa.Column("item_name", sa.String(length=200), nullable=False),
        sa.Column("item_spec", sa.String(length=240), nullable=True),
        sa.Column("enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("supplier_id", sa.BigInteger(), nullable=True),
        sa.Column("brand_id", sa.BigInteger(), nullable=True),
        sa.Column("brand_code", sa.String(length=64), nullable=True),
        sa.Column("brand_name", sa.String(length=128), nullable=True),
        sa.Column("category_id", sa.BigInteger(), nullable=True),
        sa.Column("category_code", sa.String(length=64), nullable=True),
        sa.Column("category_name", sa.String(length=128), nullable=True),
        sa.Column("category_path_code", sa.String(length=160), nullable=True),
        sa.Column("category_level", sa.Integer(), nullable=True),
        sa.Column("category_is_leaf", sa.Boolean(), nullable=True),
        sa.Column("pms_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("synced_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pms_item_id", name="uq_d2c_pms_product_projection_item_id"),
        sa.UniqueConstraint("pms_sku", name="uq_d2c_pms_product_projection_sku"),
    )
    op.create_index(
        "ix_d2c_pms_product_projection_enabled",
        "d2c_pms_product_projection",
        ["enabled"],
    )
    op.create_index(
        "ix_d2c_pms_product_projection_category",
        "d2c_pms_product_projection",
        ["category_id", "category_code"],
    )

    op.create_table(
        "d2c_pms_unit_projection",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("pms_item_uom_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_item_id", sa.BigInteger(), nullable=False),
        sa.Column("uom", sa.String(length=32), nullable=False),
        sa.Column("uom_name", sa.String(length=80), nullable=False),
        sa.Column("display_name", sa.String(length=80), nullable=True),
        sa.Column("ratio_to_base", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("net_weight_kg", sa.Numeric(precision=18, scale=6), nullable=True),
        sa.Column("is_base", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("is_purchase_default", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("is_inbound_default", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("is_outbound_default", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("pms_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("synced_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.CheckConstraint("ratio_to_base > 0", name="ck_d2c_pms_unit_projection_ratio_positive"),
        sa.ForeignKeyConstraint(
            ["pms_item_id"],
            ["d2c_pms_product_projection.pms_item_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pms_item_uom_id", name="uq_d2c_pms_unit_projection_item_uom_id"),
    )
    op.create_index("ix_d2c_pms_unit_projection_item_id", "d2c_pms_unit_projection", ["pms_item_id"])
    op.create_index(
        "ix_d2c_pms_unit_projection_usage",
        "d2c_pms_unit_projection",
        ["is_base", "is_outbound_default"],
    )

    op.create_table(
        "d2c_pms_sku_code_projection",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("pms_sku_code_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_item_id", sa.BigInteger(), nullable=False),
        sa.Column("sku_code", sa.String(length=128), nullable=False),
        sa.Column("code_type", sa.String(length=32), nullable=False),
        sa.Column("is_primary", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("remark", sa.Text(), nullable=True),
        sa.Column("item_sku", sa.String(length=128), nullable=False),
        sa.Column("item_name", sa.String(length=200), nullable=False),
        sa.Column("item_enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("pms_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("synced_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.CheckConstraint(
            "effective_to IS NULL OR effective_from IS NULL OR effective_to > effective_from",
            name="ck_d2c_pms_sku_code_projection_effective_range_valid",
        ),
        sa.ForeignKeyConstraint(
            ["pms_item_id"],
            ["d2c_pms_product_projection.pms_item_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pms_sku_code_id", name="uq_d2c_pms_sku_code_projection_id"),
        sa.UniqueConstraint("sku_code", name="uq_d2c_pms_sku_code_projection_code"),
    )
    op.create_index(
        "ix_d2c_pms_sku_code_projection_item_id",
        "d2c_pms_sku_code_projection",
        ["pms_item_id"],
    )
    op.create_index(
        "ix_d2c_pms_sku_code_projection_primary_active",
        "d2c_pms_sku_code_projection",
        ["is_primary", "is_active"],
    )

    op.create_table(
        "d2c_pms_barcode_projection",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("pms_barcode_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_item_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_item_uom_id", sa.BigInteger(), nullable=False),
        sa.Column("barcode", sa.String(length=128), nullable=False),
        sa.Column("symbology", sa.String(length=32), nullable=True),
        sa.Column("active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("is_primary", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("uom", sa.String(length=32), nullable=False),
        sa.Column("uom_name", sa.String(length=80), nullable=False),
        sa.Column("ratio_to_base", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("pms_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("synced_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.CheckConstraint("ratio_to_base > 0", name="ck_d2c_pms_barcode_projection_ratio_positive"),
        sa.ForeignKeyConstraint(
            ["pms_item_id"],
            ["d2c_pms_product_projection.pms_item_id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["pms_item_uom_id"],
            ["d2c_pms_unit_projection.pms_item_uom_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pms_barcode_id", name="uq_d2c_pms_barcode_projection_id"),
        sa.UniqueConstraint("barcode", name="uq_d2c_pms_barcode_projection_barcode"),
    )
    op.create_index(
        "ix_d2c_pms_barcode_projection_item_id",
        "d2c_pms_barcode_projection",
        ["pms_item_id"],
    )
    op.create_index(
        "ix_d2c_pms_barcode_projection_primary_active",
        "d2c_pms_barcode_projection",
        ["is_primary", "active"],
    )

    op.create_table(
        "d2c_pms_projection_sync_runs",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("sync_scope", sa.String(length=32), nullable=False),
        sa.Column("source_service", sa.String(length=64), server_default="pms-api", nullable=False),
        sa.Column("source_base_url", sa.String(length=240), nullable=True),
        sa.Column("source_endpoint", sa.String(length=240), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("requested_by", sa.String(length=120), nullable=True),
        sa.Column("rows_fetched", sa.Integer(), server_default="0", nullable=False),
        sa.Column("rows_upserted", sa.Integer(), server_default="0", nullable=False),
        sa.Column("rows_deleted", sa.Integer(), server_default="0", nullable=False),
        sa.Column("error_code", sa.String(length=120), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("raw_summary", sa.JSON(), nullable=True),
        sa.CheckConstraint("rows_fetched >= 0", name="ck_d2c_pms_projection_sync_rows_fetched_non_negative"),
        sa.CheckConstraint("rows_upserted >= 0", name="ck_d2c_pms_projection_sync_rows_upserted_non_negative"),
        sa.CheckConstraint("rows_deleted >= 0", name="ck_d2c_pms_projection_sync_rows_deleted_non_negative"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_d2c_pms_projection_sync_runs_scope_status",
        "d2c_pms_projection_sync_runs",
        ["sync_scope", "status"],
    )

    op.create_table(
        "d2c_product_listing_configs",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("pms_item_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_sku", sa.String(length=128), nullable=False),
        sa.Column("listing_code", sa.String(length=96), nullable=False),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column("subtitle", sa.String(length=240), nullable=True),
        sa.Column("description_override", sa.Text(), nullable=True),
        sa.Column("cover_image_url", sa.Text(), nullable=True),
        sa.Column("listing_status", sa.String(length=32), server_default="draft", nullable=False),
        sa.Column("display_status", sa.String(length=32), server_default="hidden", nullable=False),
        sa.Column("sell_status", sa.String(length=32), server_default="not_sellable", nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("visible_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("visible_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_product_listing_configs_sort_order_non_negative"),
        sa.CheckConstraint(
            "visible_until IS NULL OR visible_from IS NULL OR visible_until > visible_from",
            name="ck_d2c_product_listing_configs_visible_range_valid",
        ),
        sa.ForeignKeyConstraint(
            ["pms_item_id"],
            ["d2c_pms_product_projection.pms_item_id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pms_item_id", name="uq_d2c_product_listing_configs_pms_item_id"),
        sa.UniqueConstraint("listing_code", name="uq_d2c_product_listing_configs_listing_code"),
    )
    op.create_index(
        "ix_d2c_product_listing_configs_status",
        "d2c_product_listing_configs",
        ["listing_status", "display_status", "sell_status"],
    )

    op.create_table(
        "d2c_sku_listing_configs",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("product_listing_config_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_item_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_sku_code_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_item_uom_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_barcode_id", sa.BigInteger(), nullable=True),
        sa.Column("sku_display_name", sa.String(length=200), nullable=False),
        sa.Column("sku_spec_text", sa.String(length=240), nullable=True),
        sa.Column("sku_image_url", sa.Text(), nullable=True),
        sa.Column("listing_status", sa.String(length=32), server_default="draft", nullable=False),
        sa.Column("display_status", sa.String(length=32), server_default="hidden", nullable=False),
        sa.Column("sell_status", sa.String(length=32), server_default="not_sellable", nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("visible_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("visible_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_sku_listing_configs_sort_order_non_negative"),
        sa.CheckConstraint(
            "visible_until IS NULL OR visible_from IS NULL OR visible_until > visible_from",
            name="ck_d2c_sku_listing_configs_visible_range_valid",
        ),
        sa.ForeignKeyConstraint(
            ["product_listing_config_id"],
            ["d2c_product_listing_configs.id"],
            ondelete="CASCADE",
        ),
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
        sa.UniqueConstraint(
            "pms_sku_code_id",
            "pms_item_uom_id",
            name="uq_d2c_sku_listing_configs_sku_code_uom",
        ),
    )
    op.create_index(
        "ix_d2c_sku_listing_configs_product",
        "d2c_sku_listing_configs",
        ["product_listing_config_id"],
    )
    op.create_index(
        "ix_d2c_sku_listing_configs_status",
        "d2c_sku_listing_configs",
        ["listing_status", "display_status", "sell_status"],
    )

    op.create_table(
        "d2c_price_configs",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("sku_listing_config_id", sa.BigInteger(), nullable=False),
        sa.Column("price_config_code", sa.String(length=96), nullable=False),
        sa.Column("channel", sa.String(length=32), server_default="storefront", nullable=False),
        sa.Column("currency", sa.String(length=3), server_default="USD", nullable=False),
        sa.Column("price_cents", sa.Integer(), nullable=False),
        sa.Column("compare_at_price_cents", sa.Integer(), nullable=True),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("effective_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("priority", sa.Integer(), server_default="100", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("price_cents >= 0", name="ck_d2c_price_configs_price_non_negative"),
        sa.CheckConstraint("priority >= 0", name="ck_d2c_price_configs_priority_non_negative"),
        sa.CheckConstraint(
            "compare_at_price_cents IS NULL OR compare_at_price_cents >= price_cents",
            name="ck_d2c_price_configs_compare_at_valid",
        ),
        sa.CheckConstraint(
            "effective_until IS NULL OR effective_from IS NULL OR effective_until > effective_from",
            name="ck_d2c_price_configs_effective_range_valid",
        ),
        sa.ForeignKeyConstraint(
            ["sku_listing_config_id"],
            ["d2c_sku_listing_configs.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("price_config_code", name="uq_d2c_price_configs_code"),
    )
    op.create_index(
        "ix_d2c_price_configs_sku_channel_active",
        "d2c_price_configs",
        ["sku_listing_config_id", "channel", "is_active"],
    )

    op.create_table(
        "d2c_storefront_categories",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("category_code", sa.String(length=96), nullable=False),
        sa.Column("category_name", sa.String(length=160), nullable=False),
        sa.Column("parent_category_id", sa.BigInteger(), nullable=True),
        sa.Column("level", sa.Integer(), server_default="1", nullable=False),
        sa.Column("display_status", sa.String(length=32), server_default="hidden", nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("level >= 1", name="ck_d2c_storefront_categories_level_positive"),
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_storefront_categories_sort_order_non_negative"),
        sa.ForeignKeyConstraint(
            ["parent_category_id"],
            ["d2c_storefront_categories.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category_code", name="uq_d2c_storefront_categories_code"),
    )
    op.create_index(
        "ix_d2c_storefront_categories_parent",
        "d2c_storefront_categories",
        ["parent_category_id"],
    )
    op.create_index(
        "ix_d2c_storefront_categories_display_status",
        "d2c_storefront_categories",
        ["display_status"],
    )

    op.create_table(
        "d2c_storefront_category_bindings",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("product_listing_config_id", sa.BigInteger(), nullable=False),
        sa.Column("storefront_category_id", sa.BigInteger(), nullable=False),
        sa.Column("is_primary", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_storefront_category_bindings_sort_order_non_negative"),
        sa.ForeignKeyConstraint(
            ["product_listing_config_id"],
            ["d2c_product_listing_configs.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["storefront_category_id"],
            ["d2c_storefront_categories.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "product_listing_config_id",
            "storefront_category_id",
            name="uq_d2c_storefront_category_bindings_product_category",
        ),
    )
    op.create_index(
        "ix_d2c_storefront_category_bindings_product",
        "d2c_storefront_category_bindings",
        ["product_listing_config_id"],
    )
    op.create_index(
        "ix_d2c_storefront_category_bindings_category",
        "d2c_storefront_category_bindings",
        ["storefront_category_id"],
    )

    op.create_table(
        "d2c_publish_versions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("publish_scope", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), server_default="draft", nullable=False),
        sa.Column("source", sa.String(length=32), server_default="manual", nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("published_by", sa.String(length=120), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publish_version", name="uq_d2c_publish_versions_version"),
    )
    op.create_index(
        "ix_d2c_publish_versions_scope_status",
        "d2c_publish_versions",
        ["publish_scope", "status"],
    )


def downgrade() -> None:
    op.drop_index("ix_d2c_publish_versions_scope_status", table_name="d2c_publish_versions")
    op.drop_table("d2c_publish_versions")

    op.drop_index(
        "ix_d2c_storefront_category_bindings_category",
        table_name="d2c_storefront_category_bindings",
    )
    op.drop_index(
        "ix_d2c_storefront_category_bindings_product",
        table_name="d2c_storefront_category_bindings",
    )
    op.drop_table("d2c_storefront_category_bindings")

    op.drop_index(
        "ix_d2c_storefront_categories_display_status",
        table_name="d2c_storefront_categories",
    )
    op.drop_index("ix_d2c_storefront_categories_parent", table_name="d2c_storefront_categories")
    op.drop_table("d2c_storefront_categories")

    op.drop_index("ix_d2c_price_configs_sku_channel_active", table_name="d2c_price_configs")
    op.drop_table("d2c_price_configs")

    op.drop_index("ix_d2c_sku_listing_configs_status", table_name="d2c_sku_listing_configs")
    op.drop_index("ix_d2c_sku_listing_configs_product", table_name="d2c_sku_listing_configs")
    op.drop_table("d2c_sku_listing_configs")

    op.drop_index(
        "ix_d2c_product_listing_configs_status",
        table_name="d2c_product_listing_configs",
    )
    op.drop_table("d2c_product_listing_configs")

    op.drop_index(
        "ix_d2c_pms_projection_sync_runs_scope_status",
        table_name="d2c_pms_projection_sync_runs",
    )
    op.drop_table("d2c_pms_projection_sync_runs")

    op.drop_index(
        "ix_d2c_pms_barcode_projection_primary_active",
        table_name="d2c_pms_barcode_projection",
    )
    op.drop_index(
        "ix_d2c_pms_barcode_projection_item_id",
        table_name="d2c_pms_barcode_projection",
    )
    op.drop_table("d2c_pms_barcode_projection")

    op.drop_index(
        "ix_d2c_pms_sku_code_projection_primary_active",
        table_name="d2c_pms_sku_code_projection",
    )
    op.drop_index(
        "ix_d2c_pms_sku_code_projection_item_id",
        table_name="d2c_pms_sku_code_projection",
    )
    op.drop_table("d2c_pms_sku_code_projection")

    op.drop_index(
        "ix_d2c_pms_unit_projection_usage",
        table_name="d2c_pms_unit_projection",
    )
    op.drop_index(
        "ix_d2c_pms_unit_projection_item_id",
        table_name="d2c_pms_unit_projection",
    )
    op.drop_table("d2c_pms_unit_projection")

    op.drop_index(
        "ix_d2c_pms_product_projection_category",
        table_name="d2c_pms_product_projection",
    )
    op.drop_index(
        "ix_d2c_pms_product_projection_enabled",
        table_name="d2c_pms_product_projection",
    )
    op.drop_table("d2c_pms_product_projection")
