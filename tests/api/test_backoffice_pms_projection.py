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


def test_pms_projection_scope_sync_requires_backoffice_client() -> None:
    client = TestClient(app)

    response = client.post("/backoffice/pms-projections/products/sync")

    assert response.status_code == 401
    assert response.json() == {"detail": "backoffice_client_required"}


def test_pms_projection_scope_sync_invokes_products_sync(monkeypatch) -> None:
    from app.api.routes.backoffice.pms_projection import products
    from app.domains.pms_projection.contracts.sync_actions import (
        PmsProjectionSyncScopeResponse,
    )

    seen: dict[str, str] = {}

    def fake_sync_scope(session, *, scope: str, requested_by: str = "backoffice-ui"):
        seen["scope"] = scope
        seen["requested_by"] = requested_by
        return PmsProjectionSyncScopeResponse(
            scope=scope,
            endpoint="/pms/read/v1/projection-feed/items",
            status="success",
            rows_fetched=2,
            rows_upserted=2,
            error_code=None,
            error_message=None,
        )

    monkeypatch.setattr(products, "sync_pms_projection_scope", fake_sync_scope)

    client = TestClient(app)
    response = client.post(
        "/backoffice/pms-projections/products/sync",
        headers=BACKOFFICE_HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == {
        "scope": "products",
        "endpoint": "/pms/read/v1/projection-feed/items",
        "status": "success",
        "rows_fetched": 2,
        "rows_upserted": 2,
        "error_code": None,
        "error_message": None,
    }
    assert seen == {"scope": "products", "requested_by": "backoffice-ui"}


def test_pms_projection_scope_sync_routes_are_registered() -> None:
    client = TestClient(app)
    expected_paths = [
        "/backoffice/pms-projections/products/sync",
        "/backoffice/pms-projections/units/sync",
        "/backoffice/pms-projections/sku-codes/sync",
        "/backoffice/pms-projections/barcodes/sync",
        "/backoffice/pms-projections/item-contents/sync",
        "/backoffice/pms-projections/item-assets/sync",
        "/backoffice/pms-projections/display-categories/sync",
        "/backoffice/pms-projections/item-display-category-bindings/sync",
        "/backoffice/pms-projections/brand-profiles/sync",
        "/backoffice/pms-projections/brand-assets/sync",
    ]

    for path in expected_paths:
        response = client.post(path)
        assert response.status_code == 401
        assert response.json() == {"detail": "backoffice_client_required"}
