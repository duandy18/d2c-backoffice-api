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

    assert payload["count"] >= 78

    assert page_by_code["d2c.backoffice.operations"]["title"] == "经营首页"
    assert (
        page_by_code["d2c.backoffice.product_management.catalog.products"]["implementation_status"]
        == "ready"
    )
    assert page_by_code["d2c.backoffice.product_management"]["title"] == "商品管理"
    assert page_by_code["d2c.backoffice.price_management"]["title"] == "价格管理"
    assert (
        page_by_code[
            "d2c.backoffice.product_management.pms_display_projection.item_contents"
        ]["component_key"]
        == "pms_projection.item_contents"
    )
    assert (
        page_by_code[
            "d2c.backoffice.product_management.pms_display_projection.brand_assets"
        ]["data_status"]
        == "connected"
    )
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
    assert root_titles[:5] == ["经营首页", "商品管理", "价格管理", "订单与履约", "营销中心"]

    product_root = next(page for page in payload["pages"] if page["title"] == "商品管理")
    product_groups = {page["title"]: page for page in product_root["children"]}

    assert {"PMS 主数据投影", "PMS 展示资料投影", "D2C 商品配置"}.issubset(
        product_groups
    )

    master_projection_pages = {
        page["title"]: page for page in product_groups["PMS 主数据投影"]["children"]
    }
    assert master_projection_pages["商品投影"]["component_key"] == "pms_projection.products"
    assert master_projection_pages["条码投影"]["component_key"] == "pms_projection.barcodes"

    display_projection_pages = {
        page["title"]: page for page in product_groups["PMS 展示资料投影"]["children"]
    }
    assert display_projection_pages["商品标准内容"]["component_key"] == (
        "pms_projection.item_contents"
    )
    assert display_projection_pages["品牌标准素材"]["component_key"] == (
        "pms_projection.brand_assets"
    )

    product_pages = {page["title"]: page for page in product_groups["D2C 商品配置"]["children"]}

    assert product_pages["商品列表"]["component_key"] == "catalog.products"
    assert product_pages["类目管理"]["implementation_status"] == "planned"

    price_root = next(page for page in payload["pages"] if page["title"] == "价格管理")
    price_groups = {page["title"]: page for page in price_root["children"]}
    assert {"价格管理"}.issubset(price_groups)
    price_pages = {page["title"]: page for page in price_groups["价格管理"]["children"]}
    assert price_pages["价格表"]["component_key"] == "pricing.price_lists"
    assert price_pages["SKU 价格"]["component_key"] == "pricing.sku_prices"

    marketing_root = next(page for page in payload["pages"] if page["title"] == "营销中心")
    marketing_groups = {page["title"]: page for page in marketing_root["children"]}

    assert {"促销管理", "优惠券管理"}.issubset(marketing_groups)
