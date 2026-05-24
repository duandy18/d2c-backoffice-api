from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

BACKOFFICE_HEADERS = {"X-Backoffice-Client": "d2c-backoffice"}
SERVICE_HEADERS = {"X-Service-Client": "d2c-service"}


def test_backoffice_catalog_routes_are_retired() -> None:
    client = TestClient(app)

    for path in (
        "/backoffice/catalog/health",
        "/backoffice/catalog/units",
        "/backoffice/catalog/price-lists",
        "/backoffice/catalog/products",
        "/backoffice/catalog/skus",
        "/backoffice/catalog/sku-prices",
    ):
        response = client.get(path, headers=BACKOFFICE_HEADERS)
        assert response.status_code == 404


def test_backoffice_current_catalog_related_surfaces_remain_available() -> None:
    client = TestClient(app)

    backoffice_paths = (
        "/backoffice/pms-projections/health",
        "/backoffice/listing/health",
        "/backoffice/pricing/health",
        "/backoffice/publish/health",
        "/backoffice/storefront-categories/health",
    )

    for path in backoffice_paths:
        response = client.get(path, headers=BACKOFFICE_HEADERS)
        assert response.status_code == 200

    published_response = client.get(
        "/backoffice/read/v1/published/health",
        headers=SERVICE_HEADERS,
    )
    assert published_response.status_code == 200
