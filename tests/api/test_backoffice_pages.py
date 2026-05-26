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

    assert payload["count"] >= 80

    assert page_by_code["d2c.backoffice.operations"]["title"] == "经营首页"

    assert "d2c.backoffice.product_management" not in page_by_code
    assert "d2c.backoffice.product_center" not in page_by_code
    assert "d2c.backoffice.product_center.listed_products" not in page_by_code
    assert "d2c.backoffice.product_center.listed_products.center" not in page_by_code
    assert "d2c.backoffice.product_center.listed_products.skus" not in page_by_code
    assert "d2c.backoffice.product_center.listed_products.categories" not in page_by_code
    assert "d2c.backoffice.product_center.listed_products.units" not in page_by_code

    assert "d2c.backoffice.price_management" not in page_by_code
    assert "d2c.backoffice.price_management.pricing" not in page_by_code
    assert "d2c.backoffice.price_management.pricing.price_lists" not in page_by_code
    assert "d2c.backoffice.price_management.pricing.sku_prices" not in page_by_code

    merchant_product_center = page_by_code["d2c.backoffice.merchant_product_center"]
    assert merchant_product_center["title"] == "商家商品中心"
    assert merchant_product_center["parent_code"] is None
    assert merchant_product_center["level"] == 1
    assert merchant_product_center["route_path"] == "/merchant-products"
    assert merchant_product_center["component_key"] == "offers.center"
    assert merchant_product_center["implementation_status"] == "ready"
    assert merchant_product_center["data_status"] == "connected"

    assert page_by_code["d2c.backoffice.supply_sources"]["title"] == "供应链来源"
    assert page_by_code["d2c.backoffice.supply_sources"]["parent_code"] is None
    assert page_by_code["d2c.backoffice.supply_sources"]["level"] == 1
    assert (
        page_by_code["d2c.backoffice.supply_sources.products"]["component_key"]
        == "pms_projection.products"
    )
    assert (
        page_by_code["d2c.backoffice.supply_sources.sku_codes"]["title"]
        == "SKU 编码来源"
    )
    assert (
        page_by_code["d2c.backoffice.supply_sources.units"]["title"]
        == "包装单位来源"
    )
    assert (
        page_by_code["d2c.backoffice.supply_sources.barcodes"]["component_key"]
        == "pms_projection.barcodes"
    )

    assert page_by_code["d2c.backoffice.page_decoration"]["title"] == "页面装修"
    assert page_by_code["d2c.backoffice.page_decoration"]["component_key"] == (
        "layout.group"
    )
    assert page_by_code["d2c.backoffice.page_decoration"]["implementation_status"] == (
        "ready"
    )
    assert "d2c.backoffice.page_decoration.overview_group" not in page_by_code
    assert "d2c.backoffice.page_decoration.page_architecture" not in page_by_code
    assert "d2c.backoffice.page_decoration.rules" not in page_by_code
    assert "d2c.backoffice.page_decoration.release" not in page_by_code

    assert page_by_code["d2c.backoffice.page_decoration.home"]["title"] == "首页装修"
    assert page_by_code["d2c.backoffice.page_decoration.home"]["level"] == 2
    assert page_by_code["d2c.backoffice.page_decoration.home"]["component_key"] == (
        "client_presentation.overview"
    )
    assert page_by_code["d2c.backoffice.page_decoration.content"]["title"] == (
        "区块与货架"
    )
    assert page_by_code["d2c.backoffice.page_decoration.data_bindings"]["level"] == 2
    assert page_by_code["d2c.backoffice.page_decoration.data_bindings"][
        "parent_code"
    ] == "d2c.backoffice.page_decoration"
    assert page_by_code["d2c.backoffice.page_decoration.advanced"]["title"] == (
        "高级配置"
    )
    assert page_by_code["d2c.backoffice.page_decoration.advanced"]["level"] == 2
    assert page_by_code["d2c.backoffice.page_decoration.block_types"][
        "parent_code"
    ] == "d2c.backoffice.page_decoration.advanced"
    assert page_by_code["d2c.backoffice.page_decoration.layouts"][
        "parent_code"
    ] == "d2c.backoffice.page_decoration.advanced"
    assert page_by_code["d2c.backoffice.page_decoration.actions"][
        "parent_code"
    ] == "d2c.backoffice.page_decoration.advanced"

    assert "d2c.backoffice.page_decoration.preview" not in page_by_code
    assert "d2c.backoffice.page_decoration.validation" not in page_by_code
    assert "d2c.backoffice.page_decoration.publish" not in page_by_code
    assert page_by_code["d2c.backoffice.publish_center"]["title"] == "发布中心"
    assert page_by_code["d2c.backoffice.publish_center"]["level"] == 1
    assert (
        page_by_code["d2c.backoffice.publish_center.validation"]["component_key"]
        == "client_presentation.validation"
    )
    assert (
        page_by_code["d2c.backoffice.publish_center.preview"]["component_key"]
        == "client_presentation.preview"
    )
    assert page_by_code["d2c.backoffice.publish_center.runtime"]["title"] == (
        "Runtime 同步状态"
    )
    assert (
        page_by_code["d2c.backoffice.publish_center.runtime"]["component_key"]
        == "client_presentation.publish"
    )

    assert (
        page_by_code["d2c.backoffice.marketing.coupons.customer_usage"]["data_status"]
        == "connected"
    )
    assert (
        page_by_code["d2c.backoffice.orders_fulfillment.orders.list"][
            "implementation_status"
        ]
        == "planned"
    )
    assert (
        page_by_code["d2c.backoffice.analytics.funnel.checkout_to_paid"]["data_status"]
        == "placeholder"
    )
    assert (
        page_by_code["d2c.backoffice.system.pages.registry"]["component_key"]
        == "system.pages.registry"
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
    assert root_titles == [
        "经营首页",
        "商家商品中心",
        "页面装修",
        "营销中心",
        "发布中心",
        "供应链来源",
        "订单与履约",
        "顾客运营",
        "数据分析",
        "店铺设置",
        "系统管理",
    ]

    assert "商品管理" not in root_titles
    assert "商品中心" not in root_titles
    assert "价格管理" not in root_titles
    assert "客户端表现配置" not in root_titles

    merchant_product_center = next(
        page for page in payload["pages"] if page["title"] == "商家商品中心"
    )
    assert merchant_product_center["component_key"] == "offers.center"
    assert merchant_product_center["route_path"] == "/merchant-products"
    assert merchant_product_center["children"] == []

    decoration_root = next(page for page in payload["pages"] if page["title"] == "页面装修")
    decoration_groups = {page["title"]: page for page in decoration_root["children"]}
    assert {
        "首页装修",
        "区块与货架",
        "数据绑定",
        "高级配置",
    }.issubset(decoration_groups)
    assert "预览与发布" not in decoration_groups
    assert "页面结构" not in decoration_groups
    assert "展示规则" not in decoration_groups

    assert decoration_groups["首页装修"]["component_key"] == (
        "client_presentation.overview"
    )
    assert decoration_groups["数据绑定"]["component_key"] == (
        "client_presentation.data_bindings"
    )

    content_pages = {
        page["title"]: page for page in decoration_groups["区块与货架"]["children"]
    }
    assert content_pages["区块实例"]["component_key"] == "client_presentation.blocks"
    assert content_pages["货架坑位"]["component_key"] == "client_presentation.positions"
    assert "数据源绑定" not in content_pages
    assert "区块类型" not in content_pages

    advanced_pages = {
        page["title"]: page for page in decoration_groups["高级配置"]["children"]
    }
    assert advanced_pages["展示渠道"]["component_key"] == "client_presentation.surfaces"
    assert advanced_pages["顾客端页面"]["component_key"] == "client_presentation.pages"
    assert advanced_pages["页面区域"]["component_key"] == "client_presentation.regions"
    assert advanced_pages["区块类型"]["component_key"] == (
        "client_presentation.block_types"
    )
    assert advanced_pages["展示规则"]["component_key"] == "client_presentation.layouts"
    assert advanced_pages["可见性规则"]["component_key"] == (
        "client_presentation.visibility"
    )
    assert advanced_pages["交互与埋点"]["component_key"] == "client_presentation.actions"

    marketing_root = next(page for page in payload["pages"] if page["title"] == "营销中心")
    marketing_groups = {page["title"]: page for page in marketing_root["children"]}

    assert {"促销管理", "优惠券管理"}.issubset(marketing_groups)

    publish_root = next(page for page in payload["pages"] if page["title"] == "发布中心")
    publish_pages = {page["title"]: page for page in publish_root["children"]}
    assert publish_pages["发布检查"]["component_key"] == (
        "client_presentation.validation"
    )
    assert publish_pages["顾客端预览"]["component_key"] == (
        "client_presentation.preview"
    )
    assert publish_pages["Runtime 同步状态"]["component_key"] == (
        "client_presentation.publish"
    )

    supply_root = next(page for page in payload["pages"] if page["title"] == "供应链来源")
    supply_pages = {page["title"]: page for page in supply_root["children"]}

    assert supply_pages["PMS 商品来源"]["component_key"] == "pms_projection.products"
    assert supply_pages["PMS 商品来源"]["route_path"] == "/supply-sources/products"
    assert supply_pages["SKU 编码来源"]["component_key"] == "pms_projection.sku_codes"
    assert supply_pages["包装单位来源"]["component_key"] == "pms_projection.units"
    assert supply_pages["条码来源"]["component_key"] == "pms_projection.barcodes"
