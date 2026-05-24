"""add PMS display projection tables.

Revision ID: 0008_pms_display
Revises: 0007_content_media
Create Date: 2026-05-24
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0008_pms_display"
down_revision: str | Sequence[str] | None = "0007_content_media"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _projection_timestamps() -> list[sa.Column]:
    return [
        sa.Column("pms_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "synced_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
    ]


def upgrade() -> None:
    op.create_table(
        "d2c_pms_item_content_projection",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("pms_content_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_item_id", sa.BigInteger(), nullable=False),
        sa.Column("base_title", sa.String(length=200), nullable=True),
        sa.Column("base_description", sa.Text(), nullable=True),
        sa.Column("short_description", sa.Text(), nullable=True),
        sa.Column("spec_params", sa.JSON(), nullable=True),
        sa.Column("material_text", sa.Text(), nullable=True),
        sa.Column("ingredients_text", sa.Text(), nullable=True),
        sa.Column("dimensions_text", sa.Text(), nullable=True),
        sa.Column("weight_text", sa.Text(), nullable=True),
        sa.Column("safety_instructions", sa.Text(), nullable=True),
        sa.Column("usage_instructions", sa.Text(), nullable=True),
        sa.Column("storage_instructions", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        *_projection_timestamps(),
        sa.ForeignKeyConstraint(
            ["pms_item_id"],
            ["d2c_pms_product_projection.pms_item_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pms_content_id", name="uq_d2c_pms_item_content_pid"),
        sa.UniqueConstraint("pms_item_id", name="uq_d2c_pms_item_content_item"),
    )
    op.create_index(
        "ix_d2c_pms_item_content_status",
        "d2c_pms_item_content_projection",
        ["status"],
    )

    op.create_table(
        "d2c_pms_item_asset_projection",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("pms_asset_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_item_id", sa.BigInteger(), nullable=False),
        sa.Column("asset_type", sa.String(length=32), nullable=False),
        sa.Column("usage_type", sa.String(length=32), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("object_key", sa.Text(), nullable=True),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("alt_text", sa.String(length=240), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("raw_meta", sa.JSON(), nullable=True),
        *_projection_timestamps(),
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_pms_item_asset_sort"),
        sa.ForeignKeyConstraint(
            ["pms_item_id"],
            ["d2c_pms_product_projection.pms_item_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pms_asset_id", name="uq_d2c_pms_item_asset_pid"),
    )
    op.create_index(
        "ix_d2c_pms_item_asset_item_usage",
        "d2c_pms_item_asset_projection",
        ["pms_item_id", "usage_type", "status"],
    )
    op.create_index(
        "uq_d2c_pms_item_asset_primary",
        "d2c_pms_item_asset_projection",
        ["pms_item_id", "usage_type"],
        unique=True,
        postgresql_where=sa.text("is_primary = true AND status = 'active'"),
    )

    op.create_table(
        "d2c_pms_display_category_projection",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("pms_display_category_id", sa.BigInteger(), nullable=False),
        sa.Column("parent_id", sa.BigInteger(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("category_code", sa.String(length=64), nullable=False),
        sa.Column("category_name", sa.String(length=128), nullable=False),
        sa.Column("display_name", sa.String(length=128), nullable=True),
        sa.Column("path_code", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("is_leaf", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_projection_timestamps(),
        sa.CheckConstraint(
            "level >= 1 AND level <= 3",
            name="ck_d2c_pms_disp_cat_level",
        ),
        sa.CheckConstraint(
            "sort_order >= 0",
            name="ck_d2c_pms_disp_cat_sort",
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["d2c_pms_display_category_projection.pms_display_category_id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "pms_display_category_id",
            name="uq_d2c_pms_disp_cat_pid",
        ),
        sa.UniqueConstraint("path_code", name="uq_d2c_pms_disp_cat_path"),
    )
    op.create_index(
        "ix_d2c_pms_disp_cat_parent",
        "d2c_pms_display_category_projection",
        ["parent_id"],
    )
    op.create_index(
        "ix_d2c_pms_disp_cat_active_leaf",
        "d2c_pms_display_category_projection",
        ["is_active", "is_leaf"],
    )

    op.create_table(
        "d2c_pms_item_display_category_binding_projection",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("pms_binding_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_item_id", sa.BigInteger(), nullable=False),
        sa.Column("pms_display_category_id", sa.BigInteger(), nullable=False),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="100"),
        *_projection_timestamps(),
        sa.CheckConstraint(
            "sort_order >= 0",
            name="ck_d2c_pms_item_disp_bind_sort",
        ),
        sa.ForeignKeyConstraint(
            ["pms_item_id"],
            ["d2c_pms_product_projection.pms_item_id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["pms_display_category_id"],
            ["d2c_pms_display_category_projection.pms_display_category_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "pms_binding_id",
            name="uq_d2c_pms_item_disp_bind_pid",
        ),
        sa.UniqueConstraint(
            "pms_item_id",
            "pms_display_category_id",
            name="uq_d2c_pms_item_disp_bind_item_cat",
        ),
    )
    op.create_index(
        "ix_d2c_pms_item_disp_bind_item",
        "d2c_pms_item_display_category_binding_projection",
        ["pms_item_id"],
    )
    op.create_index(
        "ix_d2c_pms_item_disp_bind_cat",
        "d2c_pms_item_display_category_binding_projection",
        ["pms_display_category_id"],
    )
    op.create_index(
        "uq_d2c_pms_item_disp_bind_primary",
        "d2c_pms_item_display_category_binding_projection",
        ["pms_item_id"],
        unique=True,
        postgresql_where=sa.text("is_primary = true"),
    )

    op.create_table(
        "d2c_pms_brand_profile_projection",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("pms_profile_id", sa.BigInteger(), nullable=False),
        sa.Column("brand_id", sa.BigInteger(), nullable=False),
        sa.Column("display_name", sa.String(length=128), nullable=True),
        sa.Column("official_name", sa.String(length=128), nullable=True),
        sa.Column("brand_story", sa.Text(), nullable=True),
        sa.Column("country_or_region", sa.String(length=64), nullable=True),
        sa.Column("website_url", sa.Text(), nullable=True),
        sa.Column("seo_title", sa.String(length=200), nullable=True),
        sa.Column("seo_description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        *_projection_timestamps(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pms_profile_id", name="uq_d2c_pms_brand_profile_pid"),
        sa.UniqueConstraint("brand_id", name="uq_d2c_pms_brand_profile_brand"),
    )
    op.create_index(
        "ix_d2c_pms_brand_profile_status",
        "d2c_pms_brand_profile_projection",
        ["status"],
    )

    op.create_table(
        "d2c_pms_brand_asset_projection",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("pms_asset_id", sa.BigInteger(), nullable=False),
        sa.Column("brand_id", sa.BigInteger(), nullable=False),
        sa.Column("asset_type", sa.String(length=32), nullable=False),
        sa.Column("usage_type", sa.String(length=32), nullable=False),
        sa.Column("object_key", sa.Text(), nullable=True),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("alt_text", sa.String(length=240), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("raw_meta", sa.JSON(), nullable=True),
        *_projection_timestamps(),
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_pms_brand_asset_sort"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pms_asset_id", name="uq_d2c_pms_brand_asset_pid"),
    )
    op.create_index(
        "ix_d2c_pms_brand_asset_brand_usage",
        "d2c_pms_brand_asset_projection",
        ["brand_id", "usage_type", "status"],
    )
    op.create_index(
        "uq_d2c_pms_brand_asset_primary",
        "d2c_pms_brand_asset_projection",
        ["brand_id", "usage_type"],
        unique=True,
        postgresql_where=sa.text("is_primary = true AND status = 'active'"),
    )


def downgrade() -> None:
    op.drop_index("uq_d2c_pms_brand_asset_primary", table_name="d2c_pms_brand_asset_projection")
    op.drop_index("ix_d2c_pms_brand_asset_brand_usage", table_name="d2c_pms_brand_asset_projection")
    op.drop_table("d2c_pms_brand_asset_projection")

    op.drop_index("ix_d2c_pms_brand_profile_status", table_name="d2c_pms_brand_profile_projection")
    op.drop_table("d2c_pms_brand_profile_projection")

    op.drop_index(
        "uq_d2c_pms_item_disp_bind_primary",
        table_name="d2c_pms_item_display_category_binding_projection",
    )
    op.drop_index(
        "ix_d2c_pms_item_disp_bind_cat",
        table_name="d2c_pms_item_display_category_binding_projection",
    )
    op.drop_index(
        "ix_d2c_pms_item_disp_bind_item",
        table_name="d2c_pms_item_display_category_binding_projection",
    )
    op.drop_table("d2c_pms_item_display_category_binding_projection")

    op.drop_index(
        "ix_d2c_pms_disp_cat_active_leaf", table_name="d2c_pms_display_category_projection"
    )
    op.drop_index("ix_d2c_pms_disp_cat_parent", table_name="d2c_pms_display_category_projection")
    op.drop_table("d2c_pms_display_category_projection")

    op.drop_index("uq_d2c_pms_item_asset_primary", table_name="d2c_pms_item_asset_projection")
    op.drop_index("ix_d2c_pms_item_asset_item_usage", table_name="d2c_pms_item_asset_projection")
    op.drop_table("d2c_pms_item_asset_projection")

    op.drop_index("ix_d2c_pms_item_content_status", table_name="d2c_pms_item_content_projection")
    op.drop_table("d2c_pms_item_content_projection")
