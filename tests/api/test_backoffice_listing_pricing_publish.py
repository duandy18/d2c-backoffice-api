from fastapi.testclient import TestClient

from app.main import app

BACKOFFICE_HEADERS = {"X-Backoffice-Client": "d2c-backoffice"}


def test_backoffice_listing_requires_backoffice_client() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/listing/products")

    assert response.status_code == 401
    assert response.json() == {"detail": "backoffice_client_required"}


def test_backoffice_listing_health() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/listing/health", headers=BACKOFFICE_HEADERS)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "module": "backoffice_listing",
        "surface": "merchant_management",
    }


def test_backoffice_listing_empty_lists_are_stable() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/listing/products", headers=BACKOFFICE_HEADERS)
    assert response.status_code == 200
    assert response.json()["count"] >= 0
    assert "products" in response.json()

    response = client.get("/backoffice/listing/skus", headers=BACKOFFICE_HEADERS)
    assert response.status_code == 200
    assert response.json()["count"] >= 0
    assert "skus" in response.json()


def test_backoffice_pricing_health_and_empty_list() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/pricing/health", headers=BACKOFFICE_HEADERS)
    assert response.status_code == 200
    assert response.json()["module"] == "backoffice_pricing"

    response = client.get("/backoffice/pricing/configs", headers=BACKOFFICE_HEADERS)
    assert response.status_code == 200
    assert response.json()["count"] >= 0
    assert "price_configs" in response.json()


def test_storefront_categories_health_and_empty_lists() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/storefront-categories/health", headers=BACKOFFICE_HEADERS)
    assert response.status_code == 200
    assert response.json()["module"] == "storefront_categories"

    response = client.get("/backoffice/storefront-categories", headers=BACKOFFICE_HEADERS)
    assert response.status_code == 200
    assert response.json()["count"] >= 0
    assert "categories" in response.json()

    response = client.get("/backoffice/storefront-categories/bindings", headers=BACKOFFICE_HEADERS)
    assert response.status_code == 200
    assert response.json()["count"] >= 0
    assert "bindings" in response.json()


def test_backoffice_publish_health_and_empty_versions() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/publish/health", headers=BACKOFFICE_HEADERS)
    assert response.status_code == 200
    assert response.json()["module"] == "backoffice_publish"

    response = client.get("/backoffice/publish/versions", headers=BACKOFFICE_HEADERS)
    assert response.status_code == 200
    assert response.json()["count"] >= 0
    assert "publish_versions" in response.json()
