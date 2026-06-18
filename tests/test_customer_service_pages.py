from __future__ import annotations

from sqlalchemy import create_engine, text

from app.core.config import load_settings

EXPECTED_PAGES = {
    "d2c.backoffice.customer_service": {
        "parent_code": None,
        "level": 1,
        "title": "顾客服务",
        "route_path": "/customer-service",
        "component_key": "layout.group",
        "implementation_status": "ready",
        "data_status": "connected",
    },
    "d2c.backoffice.customer_service.support": {
        "parent_code": "d2c.backoffice.customer_service",
        "level": 2,
        "title": "客服中心",
        "route_path": "/customer-service/support",
        "component_key": "layout.group",
        "implementation_status": "ready",
        "data_status": "connected",
    },
    "d2c.backoffice.customer_service.support.overview": {
        "parent_code": "d2c.backoffice.customer_service.support",
        "level": 3,
        "title": "服务总览",
        "route_path": "/customer-service/support/overview",
        "component_key": "support.overview",
        "implementation_status": "ready",
        "data_status": "connected",
    },
    "d2c.backoffice.customer_service.support.live_sessions": {
        "parent_code": "d2c.backoffice.customer_service.support",
        "level": 3,
        "title": "在线会话",
        "route_path": "/customer-service/support/live-sessions",
        "component_key": "support.live_sessions",
        "implementation_status": "ready",
        "data_status": "connected",
    },
    "d2c.backoffice.customer_service.support.conversations": {
        "parent_code": "d2c.backoffice.customer_service.support",
        "level": 3,
        "title": "留言咨询",
        "route_path": "/customer-service/support/conversations",
        "component_key": "support.conversations",
        "implementation_status": "ready",
        "data_status": "connected",
    },
    "d2c.backoffice.customer_service.support.settings": {
        "parent_code": "d2c.backoffice.customer_service.support",
        "level": 3,
        "title": "客服设置",
        "route_path": "/customer-service/support/settings",
        "component_key": "support.settings",
        "implementation_status": "ready",
        "data_status": "connected",
    },
    "d2c.backoffice.customer_service.reviews": {
        "parent_code": "d2c.backoffice.customer_service",
        "level": 2,
        "title": "评价管理",
        "route_path": "/customer-service/reviews",
        "component_key": "layout.group",
        "implementation_status": "planned",
        "data_status": "placeholder",
    },
    "d2c.backoffice.customer_service.reviews.audit": {
        "parent_code": "d2c.backoffice.customer_service.reviews",
        "level": 3,
        "title": "评价审核",
        "route_path": "/customer-service/reviews/audit",
        "component_key": "reviews.audit",
        "implementation_status": "planned",
        "data_status": "placeholder",
    },
    "d2c.backoffice.customer_service.reviews.list": {
        "parent_code": "d2c.backoffice.customer_service.reviews",
        "level": 3,
        "title": "评价列表",
        "route_path": "/customer-service/reviews/list",
        "component_key": "reviews.list",
        "implementation_status": "planned",
        "data_status": "placeholder",
    },
    "d2c.backoffice.customer_service.reviews.replies": {
        "parent_code": "d2c.backoffice.customer_service.reviews",
        "level": 3,
        "title": "商家回复",
        "route_path": "/customer-service/reviews/replies",
        "component_key": "reviews.replies",
        "implementation_status": "planned",
        "data_status": "placeholder",
    },
    "d2c.backoffice.customer_service.reviews.rules": {
        "parent_code": "d2c.backoffice.customer_service.reviews",
        "level": 3,
        "title": "评价规则",
        "route_path": "/customer-service/reviews/rules",
        "component_key": "reviews.rules",
        "implementation_status": "planned",
        "data_status": "placeholder",
    },
    "d2c.backoffice.customer_service.after_sales": {
        "parent_code": "d2c.backoffice.customer_service",
        "level": 2,
        "title": "售后服务",
        "route_path": "/customer-service/after-sales",
        "component_key": "layout.group",
        "implementation_status": "planned",
        "data_status": "placeholder",
    },
    "d2c.backoffice.customer_service.after_sales.tickets": {
        "parent_code": "d2c.backoffice.customer_service.after_sales",
        "level": 3,
        "title": "售后工单",
        "route_path": "/customer-service/after-sales/tickets",
        "component_key": "after_sales.tickets",
        "implementation_status": "planned",
        "data_status": "placeholder",
    },
    "d2c.backoffice.customer_service.after_sales.returns": {
        "parent_code": "d2c.backoffice.customer_service.after_sales",
        "level": 3,
        "title": "退换货申请",
        "route_path": "/customer-service/after-sales/returns",
        "component_key": "after_sales.returns",
        "implementation_status": "planned",
        "data_status": "placeholder",
    },
    "d2c.backoffice.customer_service.after_sales.refunds": {
        "parent_code": "d2c.backoffice.customer_service.after_sales",
        "level": 3,
        "title": "退款处理",
        "route_path": "/customer-service/after-sales/refunds",
        "component_key": "after_sales.refunds",
        "implementation_status": "planned",
        "data_status": "placeholder",
    },
    "d2c.backoffice.customer_service.after_sales.reason_codes": {
        "parent_code": "d2c.backoffice.customer_service.after_sales",
        "level": 3,
        "title": "售后原因配置",
        "route_path": "/customer-service/after-sales/reason-codes",
        "component_key": "after_sales.reason_codes",
        "implementation_status": "planned",
        "data_status": "placeholder",
    },
}


def test_customer_service_pages_are_registered() -> None:
    engine = create_engine(load_settings().database_url)
    try:
        with engine.connect() as connection:
            rows = (
                connection.execute(
                    text(
                        """
                        SELECT
                            page_code,
                            parent_code,
                            level,
                            title,
                            route_path,
                            component_key,
                            implementation_status,
                            data_status
                        FROM d2c_backoffice_pages
                        WHERE page_code = 'd2c.backoffice.customer_service'
                           OR page_code LIKE 'd2c.backoffice.customer_service.%'
                        ORDER BY level, sort_order, page_code
                        """
                    )
                )
                .mappings()
                .all()
            )
    finally:
        engine.dispose()

    by_code = {row["page_code"]: dict(row) for row in rows}

    assert set(by_code) == set(EXPECTED_PAGES)

    for page_code, expected in EXPECTED_PAGES.items():
        row = by_code[page_code]
        for key, value in expected.items():
            assert row[key] == value


def test_customer_service_pages_do_not_use_legacy_workbench_leaf() -> None:
    engine = create_engine(load_settings().database_url)
    try:
        with engine.connect() as connection:
            count = connection.execute(
                text(
                    """
                    SELECT count(*)
                    FROM d2c_backoffice_pages
                    WHERE page_code = 'd2c.backoffice.customer_service.support.workbench'
                       OR route_path = '/customer-service/support-workbench'
                       OR component_key = 'support.workbench'
                    """
                )
            ).scalar_one()
    finally:
        engine.dispose()

    assert count == 0
