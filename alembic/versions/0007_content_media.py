"""split listing display content and media.

Revision ID: 0007_content_media
Revises: 0006_ret_cat
Create Date: 2026-05-24
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0007_content_media"
down_revision: str | Sequence[str] | None = "0006_ret_cat"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _timestamp_column(name: str) -> sa.Column:
    return sa.Column(
        name,
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
    )


def upgrade() -> None:
    op.create_table(
        "d2c_product_listing_contents",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("product_listing_config_id", sa.BigInteger(), nullable=False),
        sa.Column("display_title", sa.String(length=200), nullable=False),
        sa.Column("subtitle", sa.String(length=240), nullable=True),
        sa.Column("short_description", sa.Text(), nullable=True),
        sa.Column("detail_description", sa.Text(), nullable=True),
        sa.Column("seo_title", sa.String(length=200), nullable=True),
        sa.Column("seo_description", sa.Text(), nullable=True),
        sa.Column("selling_points", sa.JSON(), nullable=True),
        sa.Column("content_status", sa.String(length=32), nullable=False, server_default="active"),
        _timestamp_column("created_at"),
        _timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["product_listing_config_id"],
            ["d2c_product_listing_configs.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "product_listing_config_id",
            name="uq_d2c_product_listing_contents_product",
        ),
    )
    op.create_index(
        "ix_d2c_product_listing_contents_status",
        "d2c_product_listing_contents",
        ["content_status"],
    )

    op.create_table(
        "d2c_product_listing_media",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("product_listing_config_id", sa.BigInteger(), nullable=False),
        sa.Column("media_type", sa.String(length=32), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("pms_asset_id", sa.BigInteger(), nullable=True),
        sa.Column("object_key", sa.Text(), nullable=True),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("alt_text", sa.String(length=240), nullable=True),
        sa.Column("usage_type", sa.String(length=32), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="active"),
        _timestamp_column("created_at"),
        _timestamp_column("updated_at"),
        sa.CheckConstraint(
            "object_key IS NOT NULL OR url IS NOT NULL",
            name="ck_d2c_product_listing_media_location_present",
        ),
        sa.CheckConstraint(
            "sort_order >= 0",
            name="ck_d2c_product_listing_media_sort_order_non_negative",
        ),
        sa.ForeignKeyConstraint(
            ["product_listing_config_id"],
            ["d2c_product_listing_configs.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_d2c_product_listing_media_product",
        "d2c_product_listing_media",
        ["product_listing_config_id"],
    )
    op.create_index(
        "ix_d2c_product_listing_media_usage_primary",
        "d2c_product_listing_media",
        ["product_listing_config_id", "usage_type", "is_primary", "status"],
    )
    op.create_index(
        "ix_d2c_product_listing_media_sort",
        "d2c_product_listing_media",
        ["product_listing_config_id", "usage_type", "sort_order"],
    )

    op.execute(
        """
        INSERT INTO d2c_product_listing_contents (
          product_listing_config_id,
          display_title,
          subtitle,
          detail_description,
          content_status,
          created_at,
          updated_at
        )
        SELECT
          id,
          display_name,
          subtitle,
          description_override,
          'active',
          created_at,
          updated_at
        FROM d2c_product_listing_configs
        """
    )

    op.execute(
        """
        INSERT INTO d2c_product_listing_media (
          product_listing_config_id,
          media_type,
          source_type,
          url,
          alt_text,
          usage_type,
          sort_order,
          is_primary,
          status,
          created_at,
          updated_at
        )
        SELECT
          id,
          'image',
          'd2c_upload',
          cover_image_url,
          display_name,
          'cover',
          10,
          true,
          'active',
          created_at,
          updated_at
        FROM d2c_product_listing_configs
        WHERE cover_image_url IS NOT NULL
          AND btrim(cover_image_url) <> ''
        """
    )

    op.drop_column("d2c_sku_listing_configs", "sku_image_url")
    op.drop_column("d2c_product_listing_configs", "cover_image_url")
    op.drop_column("d2c_product_listing_configs", "description_override")
    op.drop_column("d2c_product_listing_configs", "subtitle")
    op.drop_column("d2c_product_listing_configs", "display_name")


def downgrade() -> None:
    op.add_column(
        "d2c_product_listing_configs",
        sa.Column("display_name", sa.String(length=200), nullable=True),
    )
    op.add_column(
        "d2c_product_listing_configs",
        sa.Column("subtitle", sa.String(length=240), nullable=True),
    )
    op.add_column(
        "d2c_product_listing_configs",
        sa.Column("description_override", sa.Text(), nullable=True),
    )
    op.add_column(
        "d2c_product_listing_configs",
        sa.Column("cover_image_url", sa.Text(), nullable=True),
    )
    op.add_column(
        "d2c_sku_listing_configs",
        sa.Column("sku_image_url", sa.Text(), nullable=True),
    )

    op.execute(
        """
        UPDATE d2c_product_listing_configs plc
        SET
          display_name = COALESCE(content.display_title, plc.listing_code),
          subtitle = content.subtitle,
          description_override = COALESCE(
            content.detail_description,
            content.short_description
          )
        FROM d2c_product_listing_contents content
        WHERE content.product_listing_config_id = plc.id
        """
    )
    op.execute(
        """
        UPDATE d2c_product_listing_configs plc
        SET cover_image_url = media.url
        FROM d2c_product_listing_media media
        WHERE media.product_listing_config_id = plc.id
          AND media.usage_type = 'cover'
          AND media.is_primary IS TRUE
          AND media.status = 'active'
        """
    )
    op.execute(
        """
        UPDATE d2c_product_listing_configs
        SET display_name = listing_code
        WHERE display_name IS NULL
        """
    )
    op.alter_column(
        "d2c_product_listing_configs",
        "display_name",
        existing_type=sa.String(length=200),
        nullable=False,
    )

    op.drop_index("ix_d2c_product_listing_media_sort", table_name="d2c_product_listing_media")
    op.drop_index(
        "ix_d2c_product_listing_media_usage_primary",
        table_name="d2c_product_listing_media",
    )
    op.drop_index("ix_d2c_product_listing_media_product", table_name="d2c_product_listing_media")
    op.drop_table("d2c_product_listing_media")

    op.drop_index(
        "ix_d2c_product_listing_contents_status",
        table_name="d2c_product_listing_contents",
    )
    op.drop_table("d2c_product_listing_contents")
