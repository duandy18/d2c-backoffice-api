"""retire PMS display projections

Revision ID: 0026_ret_pms_disp
Revises: 0025_offer_center
Create Date: 2026-05-26
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0026_ret_pms_disp"
down_revision: str | None = "0025_offer_center"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


DISPLAY_PAGE_PREFIX = "d2c.backoffice.product_management.pms_display_projection"


def upgrade() -> None:
    op.execute(
        f"""
        DELETE FROM d2c_backoffice_pages
        WHERE page_code = '{DISPLAY_PAGE_PREFIX}'
           OR page_code LIKE '{DISPLAY_PAGE_PREFIX}.%';
        """
    )

    op.drop_table("d2c_pms_brand_asset_projection")
    op.drop_table("d2c_pms_brand_profile_projection")
    op.drop_table("d2c_pms_item_display_category_binding_projection")
    op.drop_table("d2c_pms_display_category_projection")
    op.drop_table("d2c_pms_item_asset_projection")
    op.drop_table("d2c_pms_item_content_projection")


def downgrade() -> None:
    # This migration intentionally retires the obsolete PMS display projection chain.
    # Recreate through git revert if the deprecated chain is ever needed again.
    pass
