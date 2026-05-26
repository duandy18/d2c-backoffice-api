"""reorganize backoffice merchant navigation

Revision ID: 0027_bo_nav_reorg
Revises: 0026_ret_pms_disp
Create Date: 2026-05-26
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0027_bo_nav_reorg"
down_revision: str | None = "0026_ret_pms_disp"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Reorganize merchant-facing backoffice page registry.

    This migration only changes backoffice navigation metadata. It does not
    change business API contracts, component keys, or runtime owner tables.
    Merchant-facing labels move from technical PMS Projection / Offer wording
    toward D2C operating-console wording.
    """

    # 商品管理 -> 商品中心
    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_center',
            title = '商品中心',
            route_path = '/product-center',
            icon = 'box',
            sort_order = 20,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_management';
        """
    )

    # D2C 商品配置 -> 上架商品管理
    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_center.listed_products',
            parent_code = 'd2c.backoffice.product_center',
            title = '上架商品管理',
            route_path = '/product-center/listed-products',
            icon = 'box',
            sort_order = 10,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_management.catalog';
        """
    )

    # Offer 商品中心 -> 上架商品中心
    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_center.listed_products.center',
            parent_code = 'd2c.backoffice.product_center.listed_products',
            title = '上架商品中心',
            route_path = '/product-center/listed-products/center',
            component_key = 'offers.center',
            icon = 'box',
            sort_order = 10,
            implementation_status = 'ready',
            data_status = 'connected',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_management.offers.center';
        """
    )

    # Keep existing catalog-related placeholders under the new 上架商品管理 group.
    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_center.listed_products.skus',
            parent_code = 'd2c.backoffice.product_center.listed_products',
            route_path = '/product-center/listed-products/skus',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_management.catalog.skus';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_center.listed_products.categories',
            parent_code = 'd2c.backoffice.product_center.listed_products',
            route_path = '/product-center/listed-products/categories',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_management.catalog.categories';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_center.listed_products.units',
            parent_code = 'd2c.backoffice.product_center.listed_products',
            route_path = '/product-center/listed-products/units',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_management.catalog.units';
        """
    )

    # PMS 主数据投影 -> 供应链来源
    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.supply_sources',
            parent_code = NULL,
            level = 1,
            title = '供应链来源',
            route_path = '/supply-sources',
            component_key = 'layout.group',
            icon = 'pages',
            sort_order = 35,
            implementation_status = 'ready',
            data_status = 'connected',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_management.pms_master_projection';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.supply_sources.products',
            parent_code = 'd2c.backoffice.supply_sources',
            level = 2,
            title = 'PMS 商品来源',
            route_path = '/supply-sources/products',
            component_key = 'pms_projection.products',
            sort_order = 10,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_management.pms_master_projection.products';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.supply_sources.sku_codes',
            parent_code = 'd2c.backoffice.supply_sources',
            level = 2,
            title = 'SKU 编码来源',
            route_path = '/supply-sources/sku-codes',
            component_key = 'pms_projection.sku_codes',
            sort_order = 20,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_management.pms_master_projection.sku_codes';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.supply_sources.units',
            parent_code = 'd2c.backoffice.supply_sources',
            level = 2,
            title = '包装单位来源',
            route_path = '/supply-sources/units',
            component_key = 'pms_projection.units',
            sort_order = 30,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_management.pms_master_projection.units';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.supply_sources.barcodes',
            parent_code = 'd2c.backoffice.supply_sources',
            level = 2,
            title = '条码来源',
            route_path = '/supply-sources/barcodes',
            component_key = 'pms_projection.barcodes',
            sort_order = 40,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_management.pms_master_projection.barcodes';
        """
    )

    # 客户端表现配置 -> 页面装修
    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration',
            title = '页面装修',
            route_path = '/page-decoration',
            icon = 'pages',
            sort_order = 40,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.overview_group',
            parent_code = 'd2c.backoffice.page_decoration',
            route_path = '/page-decoration/overview',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.overview_group';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.overview',
            parent_code = 'd2c.backoffice.page_decoration.overview_group',
            title = '装修总览',
            route_path = '/page-decoration/overview/dashboard',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.overview';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.page_architecture',
            parent_code = 'd2c.backoffice.page_decoration',
            title = '页面结构',
            route_path = '/page-decoration/page-architecture',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.page_architecture';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.surfaces',
            parent_code = 'd2c.backoffice.page_decoration.page_architecture',
            title = '展示渠道',
            route_path = '/page-decoration/page-architecture/surfaces',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.surfaces';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.pages',
            parent_code = 'd2c.backoffice.page_decoration.page_architecture',
            title = '顾客端页面',
            route_path = '/page-decoration/page-architecture/pages',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.pages';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.regions',
            parent_code = 'd2c.backoffice.page_decoration.page_architecture',
            route_path = '/page-decoration/page-architecture/regions',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.regions';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.content',
            parent_code = 'd2c.backoffice.page_decoration',
            title = '区块与货架',
            route_path = '/page-decoration/content',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.content';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.block_types',
            parent_code = 'd2c.backoffice.page_decoration.content',
            route_path = '/page-decoration/content/block-types',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.block_types';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.blocks',
            parent_code = 'd2c.backoffice.page_decoration.content',
            route_path = '/page-decoration/content/blocks',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.blocks';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.positions',
            parent_code = 'd2c.backoffice.page_decoration.content',
            title = '货架坑位',
            route_path = '/page-decoration/content/positions',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.positions';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.data_bindings',
            parent_code = 'd2c.backoffice.page_decoration.content',
            route_path = '/page-decoration/content/data-bindings',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.data_bindings';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.rules',
            parent_code = 'd2c.backoffice.page_decoration',
            title = '展示规则',
            route_path = '/page-decoration/rules',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.rules';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.layouts',
            parent_code = 'd2c.backoffice.page_decoration.rules',
            route_path = '/page-decoration/rules/layouts',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.layouts';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.visibility',
            parent_code = 'd2c.backoffice.page_decoration.rules',
            route_path = '/page-decoration/rules/visibility',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.visibility';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.actions',
            parent_code = 'd2c.backoffice.page_decoration.rules',
            route_path = '/page-decoration/rules/actions',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.actions';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.release',
            parent_code = 'd2c.backoffice.page_decoration',
            title = '预览与发布',
            route_path = '/page-decoration/release',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.release';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.preview',
            parent_code = 'd2c.backoffice.page_decoration.release',
            title = '顾客端预览',
            route_path = '/page-decoration/release/preview',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.preview';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.validation',
            parent_code = 'd2c.backoffice.page_decoration.release',
            title = '发布校验',
            route_path = '/page-decoration/release/validation',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.validation';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.publish',
            parent_code = 'd2c.backoffice.page_decoration.release',
            title = '运行状态',
            route_path = '/page-decoration/release/publish',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.client_presentation.publish';
        """
    )


def downgrade() -> None:
    """Restore the previous merchant navigation labels and route paths."""

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.publish',
            parent_code = 'd2c.backoffice.client_presentation.release',
            title = '发布运行',
            route_path = '/client-presentation/release/publish',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.publish';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.validation',
            parent_code = 'd2c.backoffice.client_presentation.release',
            title = '契约校验',
            route_path = '/client-presentation/release/validation',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.validation';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.preview',
            parent_code = 'd2c.backoffice.client_presentation.release',
            title = '客户端预览',
            route_path = '/client-presentation/release/preview',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.preview';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.release',
            parent_code = 'd2c.backoffice.client_presentation',
            title = '预览与发布',
            route_path = '/client-presentation/release',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.release';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.actions',
            parent_code = 'd2c.backoffice.client_presentation.rules',
            route_path = '/client-presentation/rules/actions',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.actions';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.visibility',
            parent_code = 'd2c.backoffice.client_presentation.rules',
            route_path = '/client-presentation/rules/visibility',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.visibility';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.layouts',
            parent_code = 'd2c.backoffice.client_presentation.rules',
            route_path = '/client-presentation/rules/layouts',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.layouts';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.rules',
            parent_code = 'd2c.backoffice.client_presentation',
            title = '渲染与规则',
            route_path = '/client-presentation/rules',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.rules';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.data_bindings',
            parent_code = 'd2c.backoffice.client_presentation.content',
            route_path = '/client-presentation/content/data-bindings',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.data_bindings';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.positions',
            parent_code = 'd2c.backoffice.client_presentation.content',
            title = '内容坑位',
            route_path = '/client-presentation/content/positions',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.positions';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.blocks',
            parent_code = 'd2c.backoffice.client_presentation.content',
            route_path = '/client-presentation/content/blocks',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.blocks';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.block_types',
            parent_code = 'd2c.backoffice.client_presentation.content',
            route_path = '/client-presentation/content/block-types',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.block_types';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.content',
            parent_code = 'd2c.backoffice.client_presentation',
            title = '区块与内容',
            route_path = '/client-presentation/content',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.content';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.regions',
            parent_code = 'd2c.backoffice.client_presentation.page_architecture',
            route_path = '/client-presentation/page-architecture/regions',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.regions';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.pages',
            parent_code = 'd2c.backoffice.client_presentation.page_architecture',
            title = '页面模型',
            route_path = '/client-presentation/page-architecture/pages',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.pages';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.surfaces',
            parent_code = 'd2c.backoffice.client_presentation.page_architecture',
            title = '客户端渠道',
            route_path = '/client-presentation/page-architecture/surfaces',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.surfaces';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.page_architecture',
            parent_code = 'd2c.backoffice.client_presentation',
            title = '页面架构',
            route_path = '/client-presentation/page-architecture',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.page_architecture';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.overview',
            parent_code = 'd2c.backoffice.client_presentation.overview_group',
            title = '表现总览',
            route_path = '/client-presentation/overview/dashboard',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.overview';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation.overview_group',
            parent_code = 'd2c.backoffice.client_presentation',
            route_path = '/client-presentation/overview',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.overview_group';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.client_presentation',
            title = '客户端表现配置',
            route_path = '/client-presentation',
            icon = 'pages',
            sort_order = 40,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_management.pms_master_projection.barcodes',
            parent_code = 'd2c.backoffice.product_management.pms_master_projection',
            level = 3,
            title = '条码投影',
            route_path = '/product-management/pms-master-projection/barcodes',
            component_key = 'pms_projection.barcodes',
            sort_order = 40,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.supply_sources.barcodes';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_management.pms_master_projection.units',
            parent_code = 'd2c.backoffice.product_management.pms_master_projection',
            level = 3,
            title = '单位投影',
            route_path = '/product-management/pms-master-projection/units',
            component_key = 'pms_projection.units',
            sort_order = 30,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.supply_sources.units';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_management.pms_master_projection.sku_codes',
            parent_code = 'd2c.backoffice.product_management.pms_master_projection',
            level = 3,
            title = 'SKU 编码投影',
            route_path = '/product-management/pms-master-projection/sku-codes',
            component_key = 'pms_projection.sku_codes',
            sort_order = 20,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.supply_sources.sku_codes';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_management.pms_master_projection.products',
            parent_code = 'd2c.backoffice.product_management.pms_master_projection',
            level = 3,
            title = '商品投影',
            route_path = '/product-management/pms-master-projection/products',
            component_key = 'pms_projection.products',
            sort_order = 10,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.supply_sources.products';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_management.pms_master_projection',
            parent_code = 'd2c.backoffice.product_management',
            level = 2,
            title = 'PMS 主数据投影',
            route_path = '/product-management/pms-master-projection',
            component_key = 'layout.group',
            icon = 'pages',
            sort_order = 10,
            implementation_status = 'ready',
            data_status = 'connected',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.supply_sources';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_management.catalog.units',
            parent_code = 'd2c.backoffice.product_management.catalog',
            route_path = '/product-management/catalog/units',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_center.listed_products.units';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_management.catalog.categories',
            parent_code = 'd2c.backoffice.product_management.catalog',
            route_path = '/product-management/catalog/categories',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_center.listed_products.categories';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_management.catalog.skus',
            parent_code = 'd2c.backoffice.product_management.catalog',
            route_path = '/product-management/catalog/skus',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_center.listed_products.skus';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_management.offers.center',
            parent_code = 'd2c.backoffice.product_management.catalog',
            title = 'Offer 商品中心',
            route_path = '/product-management/offers',
            component_key = 'offers.center',
            icon = 'box',
            sort_order = 10,
            implementation_status = 'ready',
            data_status = 'connected',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_center.listed_products.center';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_management.catalog',
            parent_code = 'd2c.backoffice.product_management',
            title = 'D2C 商品配置',
            route_path = '/product-management/catalog',
            icon = 'box',
            sort_order = 30,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_center.listed_products';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_management',
            title = '商品管理',
            route_path = '/product-management',
            icon = 'box',
            sort_order = 20,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_center';
        """
    )
