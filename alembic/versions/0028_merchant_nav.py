"""reshape merchant backoffice navigation

Revision ID: 0028_merchant_nav
Revises: 0027_bo_nav_reorg
Create Date: 2026-05-26
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0028_merchant_nav"
down_revision: str | None = "0027_bo_nav_reorg"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _upsert_page(
    *,
    page_code: str,
    parent_code: str | None,
    level: int,
    title: str,
    route_path: str,
    component_key: str,
    icon: str | None,
    sort_order: int,
    implementation_status: str,
    data_status: str,
) -> None:
    parent_value = "NULL" if parent_code is None else f"'{parent_code}'"
    icon_value = "NULL" if icon is None else f"'{icon}'"

    op.execute(
        f"""
        INSERT INTO d2c_backoffice_pages (
            page_code,
            parent_code,
            level,
            title,
            route_path,
            component_key,
            icon,
            sort_order,
            is_enabled,
            is_visible,
            implementation_status,
            data_status,
            required_permission,
            created_at,
            updated_at
        )
        VALUES (
            '{page_code}',
            {parent_value},
            {level},
            '{title}',
            '{route_path}',
            '{component_key}',
            {icon_value},
            {sort_order},
            TRUE,
            TRUE,
            '{implementation_status}',
            '{data_status}',
            NULL,
            now(),
            now()
        )
        ON CONFLICT (page_code) DO UPDATE
        SET
            parent_code = EXCLUDED.parent_code,
            level = EXCLUDED.level,
            title = EXCLUDED.title,
            route_path = EXCLUDED.route_path,
            component_key = EXCLUDED.component_key,
            icon = EXCLUDED.icon,
            sort_order = EXCLUDED.sort_order,
            is_enabled = EXCLUDED.is_enabled,
            is_visible = EXCLUDED.is_visible,
            implementation_status = EXCLUDED.implementation_status,
            data_status = EXCLUDED.data_status,
            updated_at = now();
        """
    )


def upgrade() -> None:
    """Make the navigation match merchant operating workflows.

    The merchant product center becomes a first-level leaf page backed by
    offers.center. Legacy product catalog and price-center pages are removed
    from page registry because price is part of the listed-product workflow.
    """

    op.execute(
        """
        DELETE FROM d2c_backoffice_pages
        WHERE page_code IN (
            'd2c.backoffice.product_center.listed_products.center',
            'd2c.backoffice.product_center.listed_products.skus',
            'd2c.backoffice.product_center.listed_products.categories',
            'd2c.backoffice.product_center.listed_products.units',
            'd2c.backoffice.product_center.listed_products'
        );
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.merchant_product_center',
            parent_code = NULL,
            level = 1,
            title = '商家商品中心',
            route_path = '/merchant-products',
            component_key = 'offers.center',
            icon = 'box',
            sort_order = 20,
            is_enabled = TRUE,
            is_visible = TRUE,
            implementation_status = 'ready',
            data_status = 'connected',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.product_center';
        """
    )

    op.execute(
        """
        DELETE FROM d2c_backoffice_pages
        WHERE page_code IN (
            'd2c.backoffice.price_management.pricing.price_lists',
            'd2c.backoffice.price_management.pricing.sku_prices',
            'd2c.backoffice.price_management.pricing',
            'd2c.backoffice.price_management'
        );
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            sort_order = 30,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.home',
            parent_code = 'd2c.backoffice.page_decoration',
            level = 2,
            title = '首页装修',
            route_path = '/page-decoration/home',
            component_key = 'client_presentation.overview',
            icon = 'dashboard',
            sort_order = 10,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.overview';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            level = 2,
            title = '区块与货架',
            route_path = '/page-decoration/content',
            component_key = 'layout.group',
            icon = 'box',
            sort_order = 20,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.content';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration',
            level = 2,
            title = '数据绑定',
            route_path = '/page-decoration/data-bindings',
            component_key = 'client_presentation.data_bindings',
            icon = 'pages',
            sort_order = 30,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.data_bindings';
        """
    )

    _upsert_page(
        page_code="d2c.backoffice.page_decoration.advanced",
        parent_code="d2c.backoffice.page_decoration",
        level=2,
        title="高级配置",
        route_path="/page-decoration/advanced",
        component_key="layout.group",
        icon="settings",
        sort_order=40,
        implementation_status="ready",
        data_status="connected",
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.advanced',
            level = 3,
            title = '展示渠道',
            route_path = '/page-decoration/advanced/surfaces',
            sort_order = 10,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.surfaces';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.advanced',
            level = 3,
            title = '顾客端页面',
            route_path = '/page-decoration/advanced/pages',
            sort_order = 20,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.pages';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.advanced',
            level = 3,
            title = '页面区域',
            route_path = '/page-decoration/advanced/regions',
            sort_order = 30,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.regions';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.advanced',
            level = 3,
            title = '区块类型',
            route_path = '/page-decoration/advanced/block-types',
            sort_order = 40,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.block_types';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.advanced',
            level = 3,
            title = '展示规则',
            route_path = '/page-decoration/advanced/layouts',
            sort_order = 50,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.layouts';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.advanced',
            level = 3,
            title = '可见性规则',
            route_path = '/page-decoration/advanced/visibility',
            sort_order = 60,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.visibility';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.advanced',
            level = 3,
            title = '交互与埋点',
            route_path = '/page-decoration/advanced/actions',
            sort_order = 70,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.actions';
        """
    )

    _upsert_page(
        page_code="d2c.backoffice.publish_center",
        parent_code=None,
        level=1,
        title="发布中心",
        route_path="/publish-center",
        component_key="layout.group",
        icon="pages",
        sort_order=50,
        implementation_status="ready",
        data_status="connected",
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.publish_center.validation',
            parent_code = 'd2c.backoffice.publish_center',
            level = 2,
            title = '发布检查',
            route_path = '/publish-center/validation',
            component_key = 'client_presentation.validation',
            icon = 'pages',
            sort_order = 10,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.validation';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.publish_center.preview',
            parent_code = 'd2c.backoffice.publish_center',
            level = 2,
            title = '顾客端预览',
            route_path = '/publish-center/preview',
            component_key = 'client_presentation.preview',
            icon = 'pages',
            sort_order = 20,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.preview';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.publish_center.runtime',
            parent_code = 'd2c.backoffice.publish_center',
            level = 2,
            title = 'Runtime 同步状态',
            route_path = '/publish-center/runtime',
            component_key = 'client_presentation.publish',
            icon = 'pages',
            sort_order = 30,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.publish';
        """
    )

    op.execute(
        """
        DELETE FROM d2c_backoffice_pages
        WHERE page_code IN (
            'd2c.backoffice.page_decoration.overview_group',
            'd2c.backoffice.page_decoration.page_architecture',
            'd2c.backoffice.page_decoration.rules',
            'd2c.backoffice.page_decoration.release'
        );
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 40, updated_at = now()
        WHERE page_code = 'd2c.backoffice.marketing';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 60, updated_at = now()
        WHERE page_code = 'd2c.backoffice.supply_sources';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 70, updated_at = now()
        WHERE page_code = 'd2c.backoffice.orders_fulfillment';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 80, updated_at = now()
        WHERE page_code = 'd2c.backoffice.customer_ops';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 90, updated_at = now()
        WHERE page_code = 'd2c.backoffice.analytics';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 100, updated_at = now()
        WHERE page_code = 'd2c.backoffice.settings';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 110, updated_at = now()
        WHERE page_code = 'd2c.backoffice.system';
        """
    )


def downgrade() -> None:
    """Restore the previous 0027 navigation layout."""

    _upsert_page(
        page_code="d2c.backoffice.product_center.listed_products",
        parent_code="d2c.backoffice.product_center",
        level=2,
        title="上架商品管理",
        route_path="/product-center/listed-products",
        component_key="layout.group",
        icon="box",
        sort_order=10,
        implementation_status="ready",
        data_status="connected",
    )

    _upsert_page(
        page_code="d2c.backoffice.product_center.listed_products.center",
        parent_code="d2c.backoffice.product_center.listed_products",
        level=3,
        title="上架商品中心",
        route_path="/product-center/listed-products/center",
        component_key="offers.center",
        icon="box",
        sort_order=10,
        implementation_status="ready",
        data_status="connected",
    )

    _upsert_page(
        page_code="d2c.backoffice.product_center.listed_products.skus",
        parent_code="d2c.backoffice.product_center.listed_products",
        level=3,
        title="SKU 列表",
        route_path="/product-center/listed-products/skus",
        component_key="catalog.skus",
        icon="barcode",
        sort_order=20,
        implementation_status="ready",
        data_status="connected",
    )

    _upsert_page(
        page_code="d2c.backoffice.product_center.listed_products.categories",
        parent_code="d2c.backoffice.product_center.listed_products",
        level=3,
        title="类目管理",
        route_path="/product-center/listed-products/categories",
        component_key="catalog.categories",
        icon="folder",
        sort_order=30,
        implementation_status="planned",
        data_status="placeholder",
    )

    _upsert_page(
        page_code="d2c.backoffice.product_center.listed_products.units",
        parent_code="d2c.backoffice.product_center.listed_products",
        level=3,
        title="单位管理",
        route_path="/product-center/listed-products/units",
        component_key="catalog.units",
        icon="ruler",
        sort_order=40,
        implementation_status="ready",
        data_status="connected",
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.product_center',
            parent_code = NULL,
            level = 1,
            title = '商品中心',
            route_path = '/product-center',
            component_key = 'layout.group',
            icon = 'box',
            sort_order = 20,
            implementation_status = 'ready',
            data_status = 'connected',
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.merchant_product_center';
        """
    )

    _upsert_page(
        page_code="d2c.backoffice.price_management",
        parent_code=None,
        level=1,
        title="价格管理",
        route_path="/price-management",
        component_key="layout.group",
        icon="tag",
        sort_order=30,
        implementation_status="ready",
        data_status="connected",
    )

    _upsert_page(
        page_code="d2c.backoffice.price_management.pricing",
        parent_code="d2c.backoffice.price_management",
        level=2,
        title="价格管理",
        route_path="/price-management/pricing",
        component_key="layout.group",
        icon="tag",
        sort_order=10,
        implementation_status="ready",
        data_status="connected",
    )

    _upsert_page(
        page_code="d2c.backoffice.price_management.pricing.price_lists",
        parent_code="d2c.backoffice.price_management.pricing",
        level=3,
        title="价格表",
        route_path="/price-management/pricing/price-lists",
        component_key="pricing.price_lists",
        icon="tag",
        sort_order=10,
        implementation_status="ready",
        data_status="connected",
    )

    _upsert_page(
        page_code="d2c.backoffice.price_management.pricing.sku_prices",
        parent_code="d2c.backoffice.price_management.pricing",
        level=3,
        title="SKU 价格",
        route_path="/price-management/pricing/sku-prices",
        component_key="pricing.sku_prices",
        icon="tag",
        sort_order=20,
        implementation_status="ready",
        data_status="connected",
    )

    _upsert_page(
        page_code="d2c.backoffice.page_decoration.overview_group",
        parent_code="d2c.backoffice.page_decoration",
        level=2,
        title="总览",
        route_path="/page-decoration/overview",
        component_key="layout.group",
        icon="dashboard",
        sort_order=10,
        implementation_status="ready",
        data_status="connected",
    )

    _upsert_page(
        page_code="d2c.backoffice.page_decoration.page_architecture",
        parent_code="d2c.backoffice.page_decoration",
        level=2,
        title="页面结构",
        route_path="/page-decoration/page-architecture",
        component_key="layout.group",
        icon="pages",
        sort_order=20,
        implementation_status="ready",
        data_status="connected",
    )

    _upsert_page(
        page_code="d2c.backoffice.page_decoration.rules",
        parent_code="d2c.backoffice.page_decoration",
        level=2,
        title="展示规则",
        route_path="/page-decoration/rules",
        component_key="layout.group",
        icon="settings",
        sort_order=40,
        implementation_status="ready",
        data_status="connected",
    )

    _upsert_page(
        page_code="d2c.backoffice.page_decoration.release",
        parent_code="d2c.backoffice.page_decoration",
        level=2,
        title="预览与发布",
        route_path="/page-decoration/release",
        component_key="layout.group",
        icon="pages",
        sort_order=50,
        implementation_status="ready",
        data_status="connected",
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.overview',
            parent_code = 'd2c.backoffice.page_decoration.overview_group',
            level = 3,
            title = '装修总览',
            route_path = '/page-decoration/overview/dashboard',
            component_key = 'client_presentation.overview',
            icon = 'dashboard',
            sort_order = 10,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.home';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.page_architecture',
            level = 3,
            title = '展示渠道',
            route_path = '/page-decoration/page-architecture/surfaces',
            sort_order = 10,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.surfaces';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.page_architecture',
            level = 3,
            title = '顾客端页面',
            route_path = '/page-decoration/page-architecture/pages',
            sort_order = 20,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.pages';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.page_architecture',
            level = 3,
            title = '页面区域',
            route_path = '/page-decoration/page-architecture/regions',
            sort_order = 30,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.regions';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.content',
            level = 3,
            title = '区块类型',
            route_path = '/page-decoration/content/block-types',
            sort_order = 10,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.block_types';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.rules',
            level = 3,
            title = '展示规则',
            route_path = '/page-decoration/rules/layouts',
            sort_order = 10,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.layouts';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.rules',
            level = 3,
            title = '可见性规则',
            route_path = '/page-decoration/rules/visibility',
            sort_order = 20,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.visibility';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.rules',
            level = 3,
            title = '交互与埋点',
            route_path = '/page-decoration/rules/actions',
            sort_order = 30,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.actions';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            parent_code = 'd2c.backoffice.page_decoration.content',
            level = 3,
            title = '数据源绑定',
            route_path = '/page-decoration/content/data-bindings',
            sort_order = 40,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration.data_bindings';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.validation',
            parent_code = 'd2c.backoffice.page_decoration.release',
            level = 3,
            title = '发布校验',
            route_path = '/page-decoration/release/validation',
            component_key = 'client_presentation.validation',
            icon = 'pages',
            sort_order = 20,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.publish_center.validation';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.preview',
            parent_code = 'd2c.backoffice.page_decoration.release',
            level = 3,
            title = '顾客端预览',
            route_path = '/page-decoration/release/preview',
            component_key = 'client_presentation.preview',
            icon = 'pages',
            sort_order = 10,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.publish_center.preview';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            page_code = 'd2c.backoffice.page_decoration.publish',
            parent_code = 'd2c.backoffice.page_decoration.release',
            level = 3,
            title = '运行状态',
            route_path = '/page-decoration/release/publish',
            component_key = 'client_presentation.publish',
            icon = 'pages',
            sort_order = 30,
            updated_at = now()
        WHERE page_code = 'd2c.backoffice.publish_center.runtime';
        """
    )

    op.execute(
        """
        DELETE FROM d2c_backoffice_pages
        WHERE page_code IN (
            'd2c.backoffice.page_decoration.advanced',
            'd2c.backoffice.publish_center'
        );
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 35, updated_at = now()
        WHERE page_code = 'd2c.backoffice.supply_sources';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 40, updated_at = now()
        WHERE page_code = 'd2c.backoffice.page_decoration';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 50, updated_at = now()
        WHERE page_code = 'd2c.backoffice.orders_fulfillment';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 60, updated_at = now()
        WHERE page_code = 'd2c.backoffice.marketing';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 70, updated_at = now()
        WHERE page_code = 'd2c.backoffice.customer_ops';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 80, updated_at = now()
        WHERE page_code = 'd2c.backoffice.analytics';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 90, updated_at = now()
        WHERE page_code = 'd2c.backoffice.settings';
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = 100, updated_at = now()
        WHERE page_code = 'd2c.backoffice.system';
        """
    )
