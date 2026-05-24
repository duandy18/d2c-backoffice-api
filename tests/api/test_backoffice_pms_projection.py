from fastapi.testclient import TestClient

from app.main import app

BACKOFFICE_HEADERS = {"X-Backoffice-Client": "d2c-backoffice"}


def test_pms_projection_requires_backoffice_client() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/pms-projections/products")

    assert response.status_code == 401
    assert response.json() == {"detail": "backoffice_client_required"}


def test_pms_projection_health() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/pms-projections/health", headers=BACKOFFICE_HEADERS)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "module": "pms_projection",
        "surface": "merchant_read",
    }


def test_pms_projection_empty_lists_are_stable() -> None:
    client = TestClient(app)

    expected_paths = {
        "/backoffice/pms-projections/products": "products",
        "/backoffice/pms-projections/units": "units",
        "/backoffice/pms-projections/sku-codes": "sku_codes",
        "/backoffice/pms-projections/barcodes": "barcodes",
        "/backoffice/pms-projections/item-contents": "item_contents",
        "/backoffice/pms-projections/item-assets": "item_assets",
        "/backoffice/pms-projections/display-categories": "display_categories",
        "/backoffice/pms-projections/item-display-category-bindings": (
            "item_display_category_bindings"
        ),
        "/backoffice/pms-projections/brand-profiles": "brand_profiles",
        "/backoffice/pms-projections/brand-assets": "brand_assets",
        "/backoffice/pms-projections/sync-runs": "sync_runs",
    }

    for path, list_key in expected_paths.items():
        response = client.get(path, headers=BACKOFFICE_HEADERS)

        assert response.status_code == 200
        payload = response.json()
        assert payload["count"] >= 0
        assert list_key in payload
