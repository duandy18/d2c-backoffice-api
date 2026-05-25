"""add_storefront_section_position_owner.

Revision ID: 0020_section_pos
Revises: 0019_storefront_sections
Create Date: 2026-05-25
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0020_section_pos"
down_revision: str | Sequence[str] | None = "0019_storefront_sections"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "d2c_storefront_section_positions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("section_id", sa.BigInteger(), nullable=False),
        sa.Column("offer_id", sa.BigInteger(), nullable=False),
        sa.Column("position_code", sa.String(length=120), nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("position_type", sa.String(length=32), server_default="manual", nullable=False),
        sa.Column("is_featured", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("visible_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("visible_until", sa.DateTime(timezone=True), nullable=True),
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
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_sec_pos_sort"),
        sa.CheckConstraint(
            "visible_until IS NULL OR visible_from IS NULL OR visible_until > visible_from",
            name="ck_d2c_sec_pos_range",
        ),
        sa.ForeignKeyConstraint(["section_id"], ["d2c_storefront_sections.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["offer_id"], ["d2c_offers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("position_code", name="uq_d2c_sec_pos_code"),
        sa.UniqueConstraint("section_id", "offer_id", name="uq_d2c_sec_pos_sec_offer"),
    )
    op.create_index(
        "ix_d2c_sec_pos_section_sort",
        "d2c_storefront_section_positions",
        ["section_id", "sort_order"],
    )
    op.create_index(
        "ix_d2c_sec_pos_offer",
        "d2c_storefront_section_positions",
        ["offer_id"],
    )

    op.create_table(
        "d2c_published_storefront_section_positions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("section_code", sa.String(length=96), nullable=False),
        sa.Column("position_code", sa.String(length=120), nullable=False),
        sa.Column("offer_code", sa.String(length=96), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("position_type", sa.String(length=32), nullable=False),
        sa.Column("is_featured", sa.Boolean(), nullable=False),
        sa.Column("visible_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("visible_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_position_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publish_version", "position_code", name="uq_d2c_pub_sec_pos_code"),
    )
    op.create_index(
        "ix_d2c_pub_sec_pos_section",
        "d2c_published_storefront_section_positions",
        ["publish_version", "section_code", "sort_order"],
    )
    op.create_index(
        "ix_d2c_pub_sec_pos_offer",
        "d2c_published_storefront_section_positions",
        ["publish_version", "offer_code"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_d2c_pub_sec_pos_offer",
        table_name="d2c_published_storefront_section_positions",
    )
    op.drop_index(
        "ix_d2c_pub_sec_pos_section",
        table_name="d2c_published_storefront_section_positions",
    )
    op.drop_table("d2c_published_storefront_section_positions")

    op.drop_index("ix_d2c_sec_pos_offer", table_name="d2c_storefront_section_positions")
    op.drop_index("ix_d2c_sec_pos_section_sort", table_name="d2c_storefront_section_positions")
    op.drop_table("d2c_storefront_section_positions")
