"""register offer center page

Revision ID: 0025_offer_center
Revises: 0024_demo_seed
Create Date: 2026-05-26
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0025_offer_center"
down_revision: str | None = "0024_demo_seed"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


OLD_PAGE_CODE = "d2c.backoffice.product_management.catalog.products"
NEW_PAGE_CODE = "d2c.backoffice.product_management.offers.center"


def upgrade() -> None:
    op.execute(
        f"""
        UPDATE d2c_backoffice_pages
        SET
            page_code = '{NEW_PAGE_CODE}',
            title = 'Offer 商品中心',
            route_path = '/product-management/offers',
            component_key = 'offers.center',
            implementation_status = 'ready',
            data_status = 'connected',
            updated_at = now()
        WHERE page_code = '{OLD_PAGE_CODE}';
        """
    )


def downgrade() -> None:
    op.execute(
        f"""
        UPDATE d2c_backoffice_pages
        SET
            page_code = '{OLD_PAGE_CODE}',
            title = '商品列表',
            route_path = '/product-management/catalog/products',
            component_key = 'catalog.products',
            implementation_status = 'ready',
            data_status = 'connected',
            updated_at = now()
        WHERE page_code = '{NEW_PAGE_CODE}';
        """
    )
