"""register customer service backoffice pages

Revision ID: 0033_customer_service_pages
Revises: 0029_cp_blocks
Create Date: 2026-05-29
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0033_customer_service_pages"
down_revision: str | Sequence[str] | None = "0029_cp_blocks"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


PAGE_ROWS = [
    {
        "page_code": "d2c.backoffice.customer_service",
        "parent_code": None,
        "level": 1,
        "title": "顾客服务",
        "route_path": "/customer-service",
        "component_key": "layout.group",
        "icon": "support",
        "sort_order": 50,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.support",
        "parent_code": "d2c.backoffice.customer_service",
        "level": 2,
        "title": "客服中心",
        "route_path": "/customer-service/support",
        "component_key": "layout.group",
        "icon": "support",
        "sort_order": 10,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.support.overview",
        "parent_code": "d2c.backoffice.customer_service.support",
        "level": 3,
        "title": "服务总览",
        "route_path": "/customer-service/support/overview",
        "component_key": "support.overview",
        "icon": "dashboard",
        "sort_order": 10,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.support.live_sessions",
        "parent_code": "d2c.backoffice.customer_service.support",
        "level": 3,
        "title": "在线会话",
        "route_path": "/customer-service/support/live-sessions",
        "component_key": "support.live_sessions",
        "icon": "support",
        "sort_order": 20,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.support.conversations",
        "parent_code": "d2c.backoffice.customer_service.support",
        "level": 3,
        "title": "留言咨询",
        "route_path": "/customer-service/support/conversations",
        "component_key": "support.conversations",
        "icon": "support",
        "sort_order": 30,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.support.settings",
        "parent_code": "d2c.backoffice.customer_service.support",
        "level": 3,
        "title": "客服设置",
        "route_path": "/customer-service/support/settings",
        "component_key": "support.settings",
        "icon": "settings",
        "sort_order": 40,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.reviews",
        "parent_code": "d2c.backoffice.customer_service",
        "level": 2,
        "title": "评价管理",
        "route_path": "/customer-service/reviews",
        "component_key": "layout.group",
        "icon": "reviews",
        "sort_order": 20,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.reviews.audit",
        "parent_code": "d2c.backoffice.customer_service.reviews",
        "level": 3,
        "title": "评价审核",
        "route_path": "/customer-service/reviews/audit",
        "component_key": "reviews.audit",
        "icon": "reviews",
        "sort_order": 10,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.reviews.list",
        "parent_code": "d2c.backoffice.customer_service.reviews",
        "level": 3,
        "title": "评价列表",
        "route_path": "/customer-service/reviews/list",
        "component_key": "reviews.list",
        "icon": "reviews",
        "sort_order": 20,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.reviews.replies",
        "parent_code": "d2c.backoffice.customer_service.reviews",
        "level": 3,
        "title": "商家回复",
        "route_path": "/customer-service/reviews/replies",
        "component_key": "reviews.replies",
        "icon": "reviews",
        "sort_order": 30,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.reviews.rules",
        "parent_code": "d2c.backoffice.customer_service.reviews",
        "level": 3,
        "title": "评价规则",
        "route_path": "/customer-service/reviews/rules",
        "component_key": "reviews.rules",
        "icon": "settings",
        "sort_order": 40,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.after_sales",
        "parent_code": "d2c.backoffice.customer_service",
        "level": 2,
        "title": "售后服务",
        "route_path": "/customer-service/after-sales",
        "component_key": "layout.group",
        "icon": "support",
        "sort_order": 30,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.after_sales.tickets",
        "parent_code": "d2c.backoffice.customer_service.after_sales",
        "level": 3,
        "title": "售后工单",
        "route_path": "/customer-service/after-sales/tickets",
        "component_key": "after_sales.tickets",
        "icon": "support",
        "sort_order": 10,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.after_sales.returns",
        "parent_code": "d2c.backoffice.customer_service.after_sales",
        "level": 3,
        "title": "退换货申请",
        "route_path": "/customer-service/after-sales/returns",
        "component_key": "after_sales.returns",
        "icon": "support",
        "sort_order": 20,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.after_sales.refunds",
        "parent_code": "d2c.backoffice.customer_service.after_sales",
        "level": 3,
        "title": "退款处理",
        "route_path": "/customer-service/after-sales/refunds",
        "component_key": "after_sales.refunds",
        "icon": "payment",
        "sort_order": 30,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.customer_service.after_sales.reason_codes",
        "parent_code": "d2c.backoffice.customer_service.after_sales",
        "level": 3,
        "title": "售后原因配置",
        "route_path": "/customer-service/after-sales/reason-codes",
        "component_key": "after_sales.reason_codes",
        "icon": "settings",
        "sort_order": 40,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
]


def _upsert_page(row: dict[str, object]) -> None:
    op.execute(
        sa.text(
            """
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
                :page_code,
                :parent_code,
                :level,
                :title,
                :route_path,
                :component_key,
                :icon,
                :sort_order,
                true,
                true,
                :implementation_status,
                :data_status,
                :required_permission,
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
                required_permission = EXCLUDED.required_permission,
                updated_at = now()
            """
        ).bindparams(**row)
    )


def upgrade() -> None:
    """Register the merchant-facing customer service page tree."""

    op.execute(
        """
        DELETE FROM d2c_backoffice_pages
        WHERE page_code IN (
            'd2c.backoffice.customer_service.support.workbench',
            'd2c.backoffice.customer_service.support_workbench'
        )
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = sort_order + 10,
            updated_at = now()
        WHERE parent_code IS NULL
          AND sort_order >= 50
          AND page_code <> 'd2c.backoffice.customer_service'
        """
    )

    for row in PAGE_ROWS:
        _upsert_page(row)

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET
            sort_order = CASE page_code
                WHEN 'd2c.backoffice.operations' THEN 10
                WHEN 'd2c.backoffice.merchant_product_center' THEN 20
                WHEN 'd2c.backoffice.page_decoration' THEN 30
                WHEN 'd2c.backoffice.marketing' THEN 40
                WHEN 'd2c.backoffice.customer_service' THEN 50
                WHEN 'd2c.backoffice.publish_center' THEN 60
                WHEN 'd2c.backoffice.supply_sources' THEN 70
                WHEN 'd2c.backoffice.orders_fulfillment' THEN 80
                WHEN 'd2c.backoffice.customer_ops' THEN 90
                WHEN 'd2c.backoffice.analytics' THEN 100
                WHEN 'd2c.backoffice.settings' THEN 110
                WHEN 'd2c.backoffice.system' THEN 120
                ELSE sort_order
            END,
            updated_at = now()
        WHERE parent_code IS NULL
          AND page_code IN (
              'd2c.backoffice.operations',
              'd2c.backoffice.merchant_product_center',
              'd2c.backoffice.page_decoration',
              'd2c.backoffice.marketing',
              'd2c.backoffice.customer_service',
              'd2c.backoffice.publish_center',
              'd2c.backoffice.supply_sources',
              'd2c.backoffice.orders_fulfillment',
              'd2c.backoffice.customer_ops',
              'd2c.backoffice.analytics',
              'd2c.backoffice.settings',
              'd2c.backoffice.system'
          )
        """
    )


def downgrade() -> None:
    """Remove the customer service page tree."""

    op.execute(
        """
        DELETE FROM d2c_backoffice_pages
        WHERE page_code = 'd2c.backoffice.customer_service'
           OR page_code LIKE 'd2c.backoffice.customer_service.%'
        """
    )

    op.execute(
        """
        UPDATE d2c_backoffice_pages
        SET sort_order = sort_order - 10,
            updated_at = now()
        WHERE parent_code IS NULL
          AND sort_order >= 60
        """
    )
