"""split_product_and_pricing_pages.

Revision ID: 0014_page_split
Revises: 0008_pms_display
Create Date: 2026-05-24
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0014_page_split"
down_revision: str | Sequence[str] | None = "0008_pms_display"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


PMS_PAGES = [
    {
        "page_code": "d2c.backoffice.product_management.pms_master_projection",
        "parent_code": "d2c.backoffice.product_management",
        "level": 2,
        "title": "PMS 主数据投影",
        "route_path": "/product-management/pms-master-projection",
        "component_key": "layout.group",
        "icon": "pages",
        "sort_order": 10,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.product_management.pms_master_projection.products",
        "parent_code": "d2c.backoffice.product_management.pms_master_projection",
        "level": 3,
        "title": "商品投影",
        "route_path": "/product-management/pms-master-projection/products",
        "component_key": "pms_projection.products",
        "icon": "box",
        "sort_order": 10,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.product_management.pms_master_projection.sku_codes",
        "parent_code": "d2c.backoffice.product_management.pms_master_projection",
        "level": 3,
        "title": "SKU 编码投影",
        "route_path": "/product-management/pms-master-projection/sku-codes",
        "component_key": "pms_projection.sku_codes",
        "icon": "barcode",
        "sort_order": 20,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.product_management.pms_master_projection.units",
        "parent_code": "d2c.backoffice.product_management.pms_master_projection",
        "level": 3,
        "title": "单位投影",
        "route_path": "/product-management/pms-master-projection/units",
        "component_key": "pms_projection.units",
        "icon": "ruler",
        "sort_order": 30,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.product_management.pms_master_projection.barcodes",
        "parent_code": "d2c.backoffice.product_management.pms_master_projection",
        "level": 3,
        "title": "条码投影",
        "route_path": "/product-management/pms-master-projection/barcodes",
        "component_key": "pms_projection.barcodes",
        "icon": "barcode",
        "sort_order": 40,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.product_management.pms_display_projection",
        "parent_code": "d2c.backoffice.product_management",
        "level": 2,
        "title": "PMS 展示资料投影",
        "route_path": "/product-management/pms-display-projection",
        "component_key": "layout.group",
        "icon": "pages",
        "sort_order": 20,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.product_management.pms_display_projection.item_contents",
        "parent_code": "d2c.backoffice.product_management.pms_display_projection",
        "level": 3,
        "title": "商品标准内容",
        "route_path": "/product-management/pms-display-projection/item-contents",
        "component_key": "pms_projection.item_contents",
        "icon": "pages",
        "sort_order": 10,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.product_management.pms_display_projection.item_assets",
        "parent_code": "d2c.backoffice.product_management.pms_display_projection",
        "level": 3,
        "title": "商品标准素材",
        "route_path": "/product-management/pms-display-projection/item-assets",
        "component_key": "pms_projection.item_assets",
        "icon": "pages",
        "sort_order": 20,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.product_management.pms_display_projection.display_categories",
        "parent_code": "d2c.backoffice.product_management.pms_display_projection",
        "level": 3,
        "title": "标准展示分类",
        "route_path": "/product-management/pms-display-projection/display-categories",
        "component_key": "pms_projection.display_categories",
        "icon": "folder",
        "sort_order": 30,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.product_management.pms_display_projection.category_bindings",
        "parent_code": "d2c.backoffice.product_management.pms_display_projection",
        "level": 3,
        "title": "商品展示分类绑定",
        "route_path": "/product-management/pms-display-projection/category-bindings",
        "component_key": "pms_projection.category_bindings",
        "icon": "folder",
        "sort_order": 40,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.product_management.pms_display_projection.brand_profiles",
        "parent_code": "d2c.backoffice.product_management.pms_display_projection",
        "level": 3,
        "title": "品牌展示资料",
        "route_path": "/product-management/pms-display-projection/brand-profiles",
        "component_key": "pms_projection.brand_profiles",
        "icon": "box",
        "sort_order": 50,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.product_management.pms_display_projection.brand_assets",
        "parent_code": "d2c.backoffice.product_management.pms_display_projection",
        "level": 3,
        "title": "品牌标准素材",
        "route_path": "/product-management/pms-display-projection/brand-assets",
        "component_key": "pms_projection.brand_assets",
        "icon": "pages",
        "sort_order": 60,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
]

PRICE_ROOT = {
    "page_code": "d2c.backoffice.price_management",
    "parent_code": None,
    "level": 1,
    "title": "价格管理",
    "route_path": "/price-management",
    "component_key": "layout.group",
    "icon": "tag",
    "sort_order": 30,
    "implementation_status": "ready",
    "data_status": "connected",
    "required_permission": None,
}


def _page_table() -> sa.Table:
    return sa.table(
        "d2c_backoffice_pages",
        sa.column("page_code", sa.String),
        sa.column("parent_code", sa.String),
        sa.column("level", sa.Integer),
        sa.column("title", sa.String),
        sa.column("route_path", sa.String),
        sa.column("component_key", sa.String),
        sa.column("icon", sa.String),
        sa.column("sort_order", sa.Integer),
        sa.column("implementation_status", sa.String),
        sa.column("data_status", sa.String),
        sa.column("required_permission", sa.String),
    )


def upgrade() -> None:
    pages_table = _page_table()

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET sort_order = sort_order + 10
            WHERE parent_code IS NULL
              AND sort_order >= 30
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.product_management',
              title = '商品管理',
              route_path = '/product-management',
              sort_order = 20,
              implementation_status = 'ready',
              data_status = 'connected'
            WHERE page_code = 'd2c.backoffice.catalog_pricing'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.product_management.catalog',
              parent_code = 'd2c.backoffice.product_management',
              title = 'D2C 商品配置',
              route_path = '/product-management/catalog',
              sort_order = 30,
              implementation_status = 'ready',
              data_status = 'connected'
            WHERE page_code = 'd2c.backoffice.catalog_pricing.catalog'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.product_management.catalog.products',
              parent_code = 'd2c.backoffice.product_management.catalog',
              route_path = '/product-management/catalog/products'
            WHERE page_code = 'd2c.backoffice.catalog_pricing.catalog.products'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.product_management.catalog.skus',
              parent_code = 'd2c.backoffice.product_management.catalog',
              route_path = '/product-management/catalog/skus'
            WHERE page_code = 'd2c.backoffice.catalog_pricing.catalog.skus'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.product_management.catalog.categories',
              parent_code = 'd2c.backoffice.product_management.catalog',
              route_path = '/product-management/catalog/categories'
            WHERE page_code = 'd2c.backoffice.catalog_pricing.catalog.categories'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.product_management.catalog.units',
              parent_code = 'd2c.backoffice.product_management.catalog',
              route_path = '/product-management/catalog/units'
            WHERE page_code = 'd2c.backoffice.catalog_pricing.catalog.units'
            """
        )
    )

    op.bulk_insert(pages_table, [PRICE_ROOT])

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.price_management.pricing',
              parent_code = 'd2c.backoffice.price_management',
              route_path = '/price-management/pricing',
              sort_order = 10
            WHERE page_code = 'd2c.backoffice.catalog_pricing.pricing'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.price_management.pricing.price_lists',
              parent_code = 'd2c.backoffice.price_management.pricing',
              route_path = '/price-management/pricing/price-lists'
            WHERE page_code = 'd2c.backoffice.catalog_pricing.pricing.price_lists'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.price_management.pricing.sku_prices',
              parent_code = 'd2c.backoffice.price_management.pricing',
              route_path = '/price-management/pricing/sku-prices'
            WHERE page_code = 'd2c.backoffice.catalog_pricing.pricing.sku_prices'
            """
        )
    )

    op.bulk_insert(pages_table, PMS_PAGES)


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            DELETE FROM d2c_backoffice_pages
            WHERE page_code LIKE 'd2c.backoffice.product_management.pms_%'
               OR page_code = 'd2c.backoffice.price_management'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.catalog_pricing.pricing',
              parent_code = 'd2c.backoffice.catalog_pricing',
              route_path = '/catalog-pricing/pricing',
              sort_order = 20
            WHERE page_code = 'd2c.backoffice.price_management.pricing'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.catalog_pricing.pricing.price_lists',
              parent_code = 'd2c.backoffice.catalog_pricing.pricing',
              route_path = '/catalog-pricing/pricing/price-lists'
            WHERE page_code = 'd2c.backoffice.price_management.pricing.price_lists'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.catalog_pricing.pricing.sku_prices',
              parent_code = 'd2c.backoffice.catalog_pricing.pricing',
              route_path = '/catalog-pricing/pricing/sku-prices'
            WHERE page_code = 'd2c.backoffice.price_management.pricing.sku_prices'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.catalog_pricing.catalog',
              parent_code = 'd2c.backoffice.catalog_pricing',
              title = '商品管理',
              route_path = '/catalog-pricing/catalog',
              sort_order = 10
            WHERE page_code = 'd2c.backoffice.product_management.catalog'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.catalog_pricing.catalog.products',
              parent_code = 'd2c.backoffice.catalog_pricing.catalog',
              route_path = '/catalog-pricing/catalog/products'
            WHERE page_code = 'd2c.backoffice.product_management.catalog.products'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.catalog_pricing.catalog.skus',
              parent_code = 'd2c.backoffice.catalog_pricing.catalog',
              route_path = '/catalog-pricing/catalog/skus'
            WHERE page_code = 'd2c.backoffice.product_management.catalog.skus'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.catalog_pricing.catalog.categories',
              parent_code = 'd2c.backoffice.catalog_pricing.catalog',
              route_path = '/catalog-pricing/catalog/categories'
            WHERE page_code = 'd2c.backoffice.product_management.catalog.categories'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.catalog_pricing.catalog.units',
              parent_code = 'd2c.backoffice.catalog_pricing.catalog',
              route_path = '/catalog-pricing/catalog/units'
            WHERE page_code = 'd2c.backoffice.product_management.catalog.units'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET
              page_code = 'd2c.backoffice.catalog_pricing',
              title = '商品与价格',
              route_path = '/catalog-pricing',
              sort_order = 20
            WHERE page_code = 'd2c.backoffice.product_management'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET sort_order = sort_order - 10
            WHERE parent_code IS NULL
              AND sort_order >= 40
            """
        )
    )
