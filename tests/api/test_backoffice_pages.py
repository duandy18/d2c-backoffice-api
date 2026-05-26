from fastapi.testclient import TestClient

from app.main import app

BACKOFFICE_HEADERS = {"X-Backoffice-Client": "d2c-backoffice"}


def test_backoffice_pages_health_requires_backoffice_client() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/pages/health")

    assert response.status_code == 401
    assert response.json() == {"detail": "backoffice_client_required"}


def test_backoffice_pages_health() -> None:
    client = TestClient(app)

    response = client.get(
        "/backoffice/pages/health",
        headers=BACKOFFICE_HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "module": "backoffice_pages",
        "surface": "merchant_navigation",
    }


def test_backoffice_pages_registry_contains_full_blueprint() -> None:
    client = TestClient(app)

    response = client.get(
        "/backoffice/pages/registry",
        headers=BACKOFFICE_HEADERS,
    )

    assert response.status_code == 200

    payload = response.json()
    page_by_code = {page["page_code"]: page for page in payload["pages"]}

    assert payload["count"] >= 92

    assert page_by_code["d2c.backoffice.operations"]["title"] == "经营首页"
    assert (
        page_by_code["d2c.backoffice.product_management.offers.center"]["implementation_status"]
        == "ready"
    )
    assert page_by_code["d2c.backoffice.product_management"]["title"] == "商品管理"
    assert page_by_code["d2c.backoffice.product_management.offers.center"]["title"] == (
        "Offer 商品中心"
    )
    assert page_by_code["d2c.backoffice.product_management.offers.center"]["component_key"] == (
        "offers.center"
    )
    assert "d2c.backoffice.product_management.catalog.products" not in page_by_code
    assert page_by_code["d2c.backoffice.price_management"]["title"] == "价格管理"
    assert (
        page_by_code["d2c.backoffice.marketing.coupons.customer_usage"]["data_status"]
        == "connected"
    )
    assert (
        page_by_code["d2c.backoffice.orders_fulfillment.orders.list"]["implementation_status"]
        == "planned"
    )
    assert (
        page_by_code["d2c.backoffice.analytics.funnel.checkout_to_paid"]["data_status"]
        == "placeholder"
    )
    assert page_by_code["d2c.backoffice.system.pages.registry"]["component_key"] == (
        "system.pages.registry"
    )

    assert page_by_code["d2c.backoffice.client_presentation"]["title"] == (
        "客户端表现配置"
    )
    assert page_by_code["d2c.backoffice.client_presentation"]["component_key"] == (
        "layout.group"
    )
    assert page_by_code["d2c.backoffice.client_presentation"]["implementation_status"] == (
        "ready"
    )
    assert page_by_code["d2c.backoffice.client_presentation.page_architecture"][
        "title"
    ] == "页面架构"
    assert page_by_code["d2c.backoffice.client_presentation.content"]["title"] == (
        "区块与内容"
    )
    assert page_by_code["d2c.backoffice.client_presentation.block_types"][
        "component_key"
    ] == "client_presentation.block_types"
    assert page_by_code["d2c.backoffice.client_presentation.blocks"]["title"] == (
        "区块实例"
    )
    assert page_by_code["d2c.backoffice.client_presentation.positions"]["title"] == (
        "内容坑位"
    )
    assert page_by_code["d2c.backoffice.client_presentation.layouts"][
        "data_status"
    ] == "placeholder"
    assert page_by_code["d2c.backoffice.client_presentation.publish"]["title"] == (
        "发布运行"
    )


def test_backoffice_pages_navigation_returns_tree() -> None:
    client = TestClient(app)

    response = client.get(
        "/backoffice/pages/navigation",
        headers=BACKOFFICE_HEADERS,
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["surface"] == "backoffice"
    assert payload["version"] == 1

    root_titles = [page["title"] for page in payload["pages"]]
    assert root_titles[:6] == [
        "经营首页",
        "商品管理",
        "价格管理",
        "客户端表现配置",
        "订单与履约",
        "营销中心",
    ]

    product_root = next(page for page in payload["pages"] if page["title"] == "商品管理")
    product_groups = {page["title"]: page for page in product_root["children"]}

    assert {"PMS 主数据投影", "D2C 商品配置"}.issubset(product_groups)
    assert "PMS 展示资料投影" not in product_groups

    master_projection_pages = {
        page["title"]: page for page in product_groups["PMS 主数据投影"]["children"]
    }
    assert master_projection_pages["商品投影"]["component_key"] == "pms_projection.products"
    assert master_projection_pages["条码投影"]["component_key"] == "pms_projection.barcodes"

    product_pages = {page["title"]: page for page in product_groups["D2C 商品配置"]["children"]}

    assert product_pages["Offer 商品中心"]["component_key"] == "offers.center"
    assert product_pages["Offer 商品中心"]["route_path"] == "/product-management/offers"
    assert product_pages["类目管理"]["implementation_status"] == "planned"

    price_root = next(page for page in payload["pages"] if page["title"] == "价格管理")
    price_groups = {page["title"]: page for page in price_root["children"]}
    assert {"价格管理"}.issubset(price_groups)
    price_pages = {page["title"]: page for page in price_groups["价格管理"]["children"]}
    assert price_pages["价格表"]["component_key"] == "pricing.price_lists"
    assert price_pages["SKU 价格"]["component_key"] == "pricing.sku_prices"

    presentation_root = next(
        page for page in payload["pages"] if page["title"] == "客户端表现配置"
    )
    presentation_groups = {page["title"]: page for page in presentation_root["children"]}
    assert {
        "总览",
        "页面架构",
        "区块与内容",
        "渲染与规则",
        "预览与发布",
    }.issubset(presentation_groups)

    architecture_pages = {
        page["title"]: page for page in presentation_groups["页面架构"]["children"]
    }
    assert architecture_pages["客户端渠道"]["component_key"] == (
        "client_presentation.surfaces"
    )
    assert architecture_pages["页面模型"]["implementation_status"] == "planned"
    assert architecture_pages["页面区域"]["data_status"] == "placeholder"

    content_pages = {
        page["title"]: page for page in presentation_groups["区块与内容"]["children"]
    }
    assert content_pages["区块类型"]["component_key"] == (
        "client_presentation.block_types"
    )
    assert content_pages["区块实例"]["component_key"] == "client_presentation.blocks"
    assert content_pages["内容坑位"]["component_key"] == "client_presentation.positions"
    assert content_pages["数据源绑定"]["component_key"] == (
        "client_presentation.data_bindings"
    )

    rule_pages = {
        page["title"]: page for page in presentation_groups["渲染与规则"]["children"]
    }
    assert rule_pages["展示规则"]["component_key"] == "client_presentation.layouts"
    assert rule_pages["可见性规则"]["component_key"] == (
        "client_presentation.visibility"
    )
    assert rule_pages["交互与埋点"]["component_key"] == "client_presentation.actions"

    release_pages = {
        page["title"]: page for page in presentation_groups["预览与发布"]["children"]
    }
    assert release_pages["客户端预览"]["component_key"] == "client_presentation.preview"
    assert release_pages["契约校验"]["component_key"] == (
        "client_presentation.validation"
    )
    assert release_pages["发布运行"]["component_key"] == "client_presentation.publish"

    marketing_root = next(page for page in payload["pages"] if page["title"] == "营销中心")
    marketing_groups = {page["title"]: page for page in marketing_root["children"]}

    assert {"促销管理", "优惠券管理"}.issubset(marketing_groups)
