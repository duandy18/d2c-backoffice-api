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

    assert "d2c.backoffice.product_management" not in page_by_code
    assert "d2c.backoffice.product_management.offers.center" not in page_by_code
    assert "d2c.backoffice.product_management.pms_master_projection" not in page_by_code
    assert "d2c.backoffice.client_presentation" not in page_by_code

    assert page_by_code["d2c.backoffice.product_center"]["title"] == "商品中心"
    assert page_by_code["d2c.backoffice.product_center"]["route_path"] == "/product-center"
    assert page_by_code["d2c.backoffice.product_center"]["component_key"] == "layout.group"

    assert (
        page_by_code["d2c.backoffice.product_center.listed_products.center"][
            "implementation_status"
        ]
        == "ready"
    )
    assert (
        page_by_code["d2c.backoffice.product_center.listed_products.center"]["title"]
        == "上架商品中心"
    )
    assert (
        page_by_code["d2c.backoffice.product_center.listed_products.center"][
            "route_path"
        ]
        == "/product-center/listed-products/center"
    )
    assert (
        page_by_code["d2c.backoffice.product_center.listed_products.center"][
            "component_key"
        ]
        == "offers.center"
    )
    assert "d2c.backoffice.product_management.catalog.products" not in page_by_code

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

    assert page_by_code["d2c.backoffice.price_management"]["title"] == "价格管理"
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

    assert page_by_code["d2c.backoffice.page_decoration"]["title"] == "页面装修"
    assert page_by_code["d2c.backoffice.page_decoration"]["component_key"] == (
        "layout.group"
    )
    assert page_by_code["d2c.backoffice.page_decoration"]["implementation_status"] == (
        "ready"
    )
    assert page_by_code["d2c.backoffice.page_decoration.page_architecture"][
        "title"
    ] == "页面结构"
    assert page_by_code["d2c.backoffice.page_decoration.content"]["title"] == (
        "区块与货架"
    )
    assert page_by_code["d2c.backoffice.page_decoration.block_types"][
        "component_key"
    ] == "client_presentation.block_types"
    assert page_by_code["d2c.backoffice.page_decoration.blocks"]["title"] == (
        "区块实例"
    )
    assert page_by_code["d2c.backoffice.page_decoration.positions"]["title"] == (
        "货架坑位"
    )
    assert page_by_code["d2c.backoffice.page_decoration.layouts"][
        "data_status"
    ] == "placeholder"
    assert page_by_code["d2c.backoffice.page_decoration.preview"]["title"] == (
        "顾客端预览"
    )
    assert page_by_code["d2c.backoffice.page_decoration.validation"]["title"] == (
        "发布校验"
    )
    assert page_by_code["d2c.backoffice.page_decoration.publish"]["title"] == (
        "运行状态"
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
    assert root_titles[:7] == [
        "经营首页",
        "商品中心",
        "价格管理",
        "供应链来源",
        "页面装修",
        "订单与履约",
        "营销中心",
    ]

    assert "商品管理" not in root_titles
    assert "客户端表现配置" not in root_titles

    product_root = next(page for page in payload["pages"] if page["title"] == "商品中心")
    product_groups = {page["title"]: page for page in product_root["children"]}

    assert {"上架商品管理"}.issubset(product_groups)
    assert "PMS 主数据投影" not in product_groups
    assert "PMS 展示资料投影" not in product_groups

    product_pages = {page["title"]: page for page in product_groups["上架商品管理"]["children"]}

    assert product_pages["上架商品中心"]["component_key"] == "offers.center"
    assert (
        product_pages["上架商品中心"]["route_path"]
        == "/product-center/listed-products/center"
    )
    assert product_pages["类目管理"]["implementation_status"] == "planned"

    supply_root = next(page for page in payload["pages"] if page["title"] == "供应链来源")
    supply_pages = {page["title"]: page for page in supply_root["children"]}

    assert supply_pages["PMS 商品来源"]["component_key"] == "pms_projection.products"
    assert supply_pages["PMS 商品来源"]["route_path"] == "/supply-sources/products"
    assert supply_pages["SKU 编码来源"]["component_key"] == "pms_projection.sku_codes"
    assert supply_pages["包装单位来源"]["component_key"] == "pms_projection.units"
    assert supply_pages["条码来源"]["component_key"] == "pms_projection.barcodes"

    price_root = next(page for page in payload["pages"] if page["title"] == "价格管理")
    price_groups = {page["title"]: page for page in price_root["children"]}
    assert {"价格管理"}.issubset(price_groups)
    price_pages = {page["title"]: page for page in price_groups["价格管理"]["children"]}
    assert price_pages["价格表"]["component_key"] == "pricing.price_lists"
    assert price_pages["SKU 价格"]["component_key"] == "pricing.sku_prices"

    decoration_root = next(page for page in payload["pages"] if page["title"] == "页面装修")
    decoration_groups = {page["title"]: page for page in decoration_root["children"]}
    assert {
        "总览",
        "页面结构",
        "区块与货架",
        "展示规则",
        "预览与发布",
    }.issubset(decoration_groups)

    architecture_pages = {
        page["title"]: page for page in decoration_groups["页面结构"]["children"]
    }
    assert architecture_pages["展示渠道"]["component_key"] == (
        "client_presentation.surfaces"
    )
    assert architecture_pages["顾客端页面"]["implementation_status"] == "planned"
    assert architecture_pages["页面区域"]["data_status"] == "placeholder"

    content_pages = {
        page["title"]: page for page in decoration_groups["区块与货架"]["children"]
    }
    assert content_pages["区块类型"]["component_key"] == (
        "client_presentation.block_types"
    )
    assert content_pages["区块实例"]["component_key"] == "client_presentation.blocks"
    assert content_pages["货架坑位"]["component_key"] == "client_presentation.positions"
    assert content_pages["数据源绑定"]["component_key"] == (
        "client_presentation.data_bindings"
    )

    rule_pages = {
        page["title"]: page for page in decoration_groups["展示规则"]["children"]
    }
    assert rule_pages["展示规则"]["component_key"] == "client_presentation.layouts"
    assert rule_pages["可见性规则"]["component_key"] == (
        "client_presentation.visibility"
    )
    assert rule_pages["交互与埋点"]["component_key"] == "client_presentation.actions"

    release_pages = {
        page["title"]: page for page in decoration_groups["预览与发布"]["children"]
    }
    assert release_pages["顾客端预览"]["component_key"] == "client_presentation.preview"
    assert release_pages["发布校验"]["component_key"] == (
        "client_presentation.validation"
    )
    assert release_pages["运行状态"]["component_key"] == "client_presentation.publish"

    marketing_root = next(page for page in payload["pages"] if page["title"] == "营销中心")
    marketing_groups = {page["title"]: page for page in marketing_root["children"]}

    assert {"促销管理", "优惠券管理"}.issubset(marketing_groups)
