"""register_client_presentation_pages.

Revision ID: 0021_client_pres
Revises: 0020_section_pos
Create Date: 2026-05-25
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0021_client_pres"
down_revision: str | Sequence[str] | None = "0020_section_pos"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


PAGE_ROWS = [
    {
        "page_code": "d2c.backoffice.client_presentation",
        "parent_code": None,
        "level": 1,
        "title": "客户端表现配置",
        "route_path": "/client-presentation",
        "component_key": "layout.group",
        "icon": "pages",
        "sort_order": 40,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.overview_group",
        "parent_code": "d2c.backoffice.client_presentation",
        "level": 2,
        "title": "总览",
        "route_path": "/client-presentation/overview",
        "component_key": "layout.group",
        "icon": "dashboard",
        "sort_order": 10,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.overview",
        "parent_code": "d2c.backoffice.client_presentation.overview_group",
        "level": 3,
        "title": "表现总览",
        "route_path": "/client-presentation/overview/dashboard",
        "component_key": "client_presentation.overview",
        "icon": "dashboard",
        "sort_order": 10,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.page_architecture",
        "parent_code": "d2c.backoffice.client_presentation",
        "level": 2,
        "title": "页面架构",
        "route_path": "/client-presentation/page-architecture",
        "component_key": "layout.group",
        "icon": "pages",
        "sort_order": 20,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.surfaces",
        "parent_code": "d2c.backoffice.client_presentation.page_architecture",
        "level": 3,
        "title": "客户端渠道",
        "route_path": "/client-presentation/page-architecture/surfaces",
        "component_key": "client_presentation.surfaces",
        "icon": "pages",
        "sort_order": 10,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.pages",
        "parent_code": "d2c.backoffice.client_presentation.page_architecture",
        "level": 3,
        "title": "页面模型",
        "route_path": "/client-presentation/page-architecture/pages",
        "component_key": "client_presentation.pages",
        "icon": "pages",
        "sort_order": 20,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.regions",
        "parent_code": "d2c.backoffice.client_presentation.page_architecture",
        "level": 3,
        "title": "页面区域",
        "route_path": "/client-presentation/page-architecture/regions",
        "component_key": "client_presentation.regions",
        "icon": "pages",
        "sort_order": 30,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.content",
        "parent_code": "d2c.backoffice.client_presentation",
        "level": 2,
        "title": "区块与内容",
        "route_path": "/client-presentation/content",
        "component_key": "layout.group",
        "icon": "box",
        "sort_order": 30,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.block_types",
        "parent_code": "d2c.backoffice.client_presentation.content",
        "level": 3,
        "title": "区块类型",
        "route_path": "/client-presentation/content/block-types",
        "component_key": "client_presentation.block_types",
        "icon": "box",
        "sort_order": 10,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.blocks",
        "parent_code": "d2c.backoffice.client_presentation.content",
        "level": 3,
        "title": "区块实例",
        "route_path": "/client-presentation/content/blocks",
        "component_key": "client_presentation.blocks",
        "icon": "box",
        "sort_order": 20,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.positions",
        "parent_code": "d2c.backoffice.client_presentation.content",
        "level": 3,
        "title": "内容坑位",
        "route_path": "/client-presentation/content/positions",
        "component_key": "client_presentation.positions",
        "icon": "target",
        "sort_order": 30,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.data_bindings",
        "parent_code": "d2c.backoffice.client_presentation.content",
        "level": 3,
        "title": "数据源绑定",
        "route_path": "/client-presentation/content/data-bindings",
        "component_key": "client_presentation.data_bindings",
        "icon": "pages",
        "sort_order": 40,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.rules",
        "parent_code": "d2c.backoffice.client_presentation",
        "level": 2,
        "title": "渲染与规则",
        "route_path": "/client-presentation/rules",
        "component_key": "layout.group",
        "icon": "settings",
        "sort_order": 40,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.layouts",
        "parent_code": "d2c.backoffice.client_presentation.rules",
        "level": 3,
        "title": "展示规则",
        "route_path": "/client-presentation/rules/layouts",
        "component_key": "client_presentation.layouts",
        "icon": "settings",
        "sort_order": 10,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.visibility",
        "parent_code": "d2c.backoffice.client_presentation.rules",
        "level": 3,
        "title": "可见性规则",
        "route_path": "/client-presentation/rules/visibility",
        "component_key": "client_presentation.visibility",
        "icon": "settings",
        "sort_order": 20,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.actions",
        "parent_code": "d2c.backoffice.client_presentation.rules",
        "level": 3,
        "title": "交互与埋点",
        "route_path": "/client-presentation/rules/actions",
        "component_key": "client_presentation.actions",
        "icon": "analytics",
        "sort_order": 30,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.release",
        "parent_code": "d2c.backoffice.client_presentation",
        "level": 2,
        "title": "预览与发布",
        "route_path": "/client-presentation/release",
        "component_key": "layout.group",
        "icon": "pages",
        "sort_order": 50,
        "implementation_status": "ready",
        "data_status": "connected",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.preview",
        "parent_code": "d2c.backoffice.client_presentation.release",
        "level": 3,
        "title": "客户端预览",
        "route_path": "/client-presentation/release/preview",
        "component_key": "client_presentation.preview",
        "icon": "pages",
        "sort_order": 10,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.validation",
        "parent_code": "d2c.backoffice.client_presentation.release",
        "level": 3,
        "title": "契约校验",
        "route_path": "/client-presentation/release/validation",
        "component_key": "client_presentation.validation",
        "icon": "pages",
        "sort_order": 20,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
    {
        "page_code": "d2c.backoffice.client_presentation.publish",
        "parent_code": "d2c.backoffice.client_presentation.release",
        "level": 3,
        "title": "发布运行",
        "route_path": "/client-presentation/release/publish",
        "component_key": "client_presentation.publish",
        "icon": "pages",
        "sort_order": 30,
        "implementation_status": "planned",
        "data_status": "placeholder",
        "required_permission": None,
    },
]


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
              AND sort_order >= 40
            """
        )
    )

    op.bulk_insert(pages_table, PAGE_ROWS)


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            DELETE FROM d2c_backoffice_pages
            WHERE page_code LIKE 'd2c.backoffice.client_presentation%'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_backoffice_pages
            SET sort_order = sort_order - 10
            WHERE parent_code IS NULL
              AND sort_order >= 50
            """
        )
    )
