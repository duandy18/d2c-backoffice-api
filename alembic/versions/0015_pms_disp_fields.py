"""add_pms_display_projection_fields.

Revision ID: 0015_pms_disp_fields
Revises: 0014_page_split
Create Date: 2026-05-24
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0015_pms_disp_fields"
down_revision: str | Sequence[str] | None = "0014_page_split"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "d2c_pms_item_content_projection",
        sa.Column("item_sku", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "d2c_pms_item_content_projection",
        sa.Column("item_name", sa.String(length=200), nullable=True),
    )

    op.add_column(
        "d2c_pms_item_asset_projection",
        sa.Column("item_sku", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "d2c_pms_item_asset_projection",
        sa.Column("item_name", sa.String(length=200), nullable=True),
    )

    op.add_column(
        "d2c_pms_item_display_category_binding_projection",
        sa.Column("item_sku", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "d2c_pms_item_display_category_binding_projection",
        sa.Column("item_name", sa.String(length=200), nullable=True),
    )
    op.add_column(
        "d2c_pms_item_display_category_binding_projection",
        sa.Column("display_category_code", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "d2c_pms_item_display_category_binding_projection",
        sa.Column("display_category_name", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "d2c_pms_item_display_category_binding_projection",
        sa.Column("display_category_path_code", sa.String(length=255), nullable=True),
    )

    op.add_column(
        "d2c_pms_brand_profile_projection",
        sa.Column("brand_code", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "d2c_pms_brand_profile_projection",
        sa.Column("brand_name", sa.String(length=128), nullable=True),
    )

    op.add_column(
        "d2c_pms_brand_asset_projection",
        sa.Column("brand_code", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "d2c_pms_brand_asset_projection",
        sa.Column("brand_name", sa.String(length=128), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("d2c_pms_brand_asset_projection", "brand_name")
    op.drop_column("d2c_pms_brand_asset_projection", "brand_code")

    op.drop_column("d2c_pms_brand_profile_projection", "brand_name")
    op.drop_column("d2c_pms_brand_profile_projection", "brand_code")

    op.drop_column(
        "d2c_pms_item_display_category_binding_projection",
        "display_category_path_code",
    )
    op.drop_column(
        "d2c_pms_item_display_category_binding_projection",
        "display_category_name",
    )
    op.drop_column(
        "d2c_pms_item_display_category_binding_projection",
        "display_category_code",
    )
    op.drop_column("d2c_pms_item_display_category_binding_projection", "item_name")
    op.drop_column("d2c_pms_item_display_category_binding_projection", "item_sku")

    op.drop_column("d2c_pms_item_asset_projection", "item_name")
    op.drop_column("d2c_pms_item_asset_projection", "item_sku")

    op.drop_column("d2c_pms_item_content_projection", "item_name")
    op.drop_column("d2c_pms_item_content_projection", "item_sku")
