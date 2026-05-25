"""add_storefront_section_layout_owner.

Revision ID: 0019_storefront_sections
Revises: 0018_pub_snapshot
Create Date: 2026-05-25
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0019_storefront_sections"
down_revision: str | Sequence[str] | None = "0018_pub_snapshot"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "d2c_storefront_sections",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("section_code", sa.String(length=96), nullable=False),
        sa.Column("section_type", sa.String(length=32), nullable=False),
        sa.Column("group_id", sa.BigInteger(), nullable=True),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("subtitle", sa.String(length=240), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("display_status", sa.String(length=32), server_default="visible", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
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
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_sections_sort"),
        sa.ForeignKeyConstraint(["group_id"], ["d2c_groups.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("section_code", name="uq_d2c_sections_code"),
    )
    op.create_index(
        "ix_d2c_sections_group_sort", "d2c_storefront_sections", ["group_id", "sort_order"]
    )
    op.create_index(
        "ix_d2c_sections_status",
        "d2c_storefront_sections",
        ["section_type", "display_status", "is_active"],
    )

    op.create_table(
        "d2c_storefront_section_layouts",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("section_id", sa.BigInteger(), nullable=False),
        sa.Column("display_type", sa.String(length=32), nullable=False),
        sa.Column("columns_desktop", sa.Integer(), server_default="4", nullable=False),
        sa.Column("columns_tablet", sa.Integer(), server_default="2", nullable=False),
        sa.Column("columns_mobile", sa.Integer(), server_default="1", nullable=False),
        sa.Column("card_size", sa.String(length=32), server_default="standard", nullable=False),
        sa.Column("image_ratio", sa.String(length=16), server_default="1:1", nullable=False),
        sa.Column("show_promotion_badge", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("show_sales_summary", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("show_review_summary", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("show_compare_price", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("show_quantity_stepper", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("max_items", sa.Integer(), nullable=True),
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
        sa.CheckConstraint("columns_desktop > 0", name="ck_d2c_section_layout_desktop_cols"),
        sa.CheckConstraint("columns_tablet > 0", name="ck_d2c_section_layout_tablet_cols"),
        sa.CheckConstraint("columns_mobile > 0", name="ck_d2c_section_layout_mobile_cols"),
        sa.CheckConstraint(
            "max_items IS NULL OR max_items > 0", name="ck_d2c_section_layout_max_items"
        ),
        sa.ForeignKeyConstraint(["section_id"], ["d2c_storefront_sections.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("section_id", name="uq_d2c_section_layouts_section"),
    )
    op.create_index(
        "ix_d2c_section_layouts_display", "d2c_storefront_section_layouts", ["display_type"]
    )

    op.create_table(
        "d2c_published_storefront_sections",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("section_code", sa.String(length=96), nullable=False),
        sa.Column("section_type", sa.String(length=32), nullable=False),
        sa.Column("group_code", sa.String(length=96), nullable=True),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("subtitle", sa.String(length=240), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("display_status", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("source_section_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publish_version", "section_code", name="uq_d2c_pub_sections_code"),
    )
    op.create_index(
        "ix_d2c_pub_sections_group_sort",
        "d2c_published_storefront_sections",
        ["publish_version", "group_code", "sort_order"],
    )

    op.create_table(
        "d2c_published_storefront_section_layouts",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("section_code", sa.String(length=96), nullable=False),
        sa.Column("display_type", sa.String(length=32), nullable=False),
        sa.Column("columns_desktop", sa.Integer(), nullable=False),
        sa.Column("columns_tablet", sa.Integer(), nullable=False),
        sa.Column("columns_mobile", sa.Integer(), nullable=False),
        sa.Column("card_size", sa.String(length=32), nullable=False),
        sa.Column("image_ratio", sa.String(length=16), nullable=False),
        sa.Column("show_promotion_badge", sa.Boolean(), nullable=False),
        sa.Column("show_sales_summary", sa.Boolean(), nullable=False),
        sa.Column("show_review_summary", sa.Boolean(), nullable=False),
        sa.Column("show_compare_price", sa.Boolean(), nullable=False),
        sa.Column("show_quantity_stepper", sa.Boolean(), nullable=False),
        sa.Column("max_items", sa.Integer(), nullable=True),
        sa.Column("source_layout_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "publish_version", "section_code", name="uq_d2c_pub_section_layouts_code"
        ),
    )
    op.create_index(
        "ix_d2c_pub_section_layouts_display",
        "d2c_published_storefront_section_layouts",
        ["publish_version", "display_type"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_d2c_pub_section_layouts_display",
        table_name="d2c_published_storefront_section_layouts",
    )
    op.drop_table("d2c_published_storefront_section_layouts")

    op.drop_index("ix_d2c_pub_sections_group_sort", table_name="d2c_published_storefront_sections")
    op.drop_table("d2c_published_storefront_sections")

    op.drop_index("ix_d2c_section_layouts_display", table_name="d2c_storefront_section_layouts")
    op.drop_table("d2c_storefront_section_layouts")

    op.drop_index("ix_d2c_sections_status", table_name="d2c_storefront_sections")
    op.drop_index("ix_d2c_sections_group_sort", table_name="d2c_storefront_sections")
    op.drop_table("d2c_storefront_sections")
