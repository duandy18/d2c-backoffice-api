from datetime import UTC, datetime

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
        now = datetime(2026, 5, 24, 14, 0, 0, tzinfo=UTC)
        return PmsProjectionSyncScopeResponse(
            scope=scope,
            endpoint="/pms/read/v1/projection-feed/items",
            source_base_url="http://pms-api.test",
            source_endpoint="/pms/read/v1/projection-feed/items",
            status="success",
            started_at=now,
            finished_at=now,
            requested_by=requested_by,
            rows_fetched=2,
            rows_upserted=2,
            rows_deleted=0,
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
    payload = response.json()
    assert payload["scope"] == "products"
    assert payload["endpoint"] == "/pms/read/v1/projection-feed/items"
    assert payload["source_base_url"] == "http://pms-api.test"
    assert payload["source_endpoint"] == "/pms/read/v1/projection-feed/items"
    assert payload["status"] == "success"
    assert payload["started_at"] == "2026-05-24T14:00:00Z"
    assert payload["finished_at"] == "2026-05-24T14:00:00Z"
    assert payload["requested_by"] == "backoffice-ui"
    assert payload["rows_fetched"] == 2
    assert payload["rows_upserted"] == 2
    assert payload["rows_deleted"] == 0
    assert payload["error_code"] is None
    assert payload["error_message"] is None
    assert seen == {"scope": "products", "requested_by": "backoffice-ui"}


def test_pms_projection_scope_sync_routes_are_registered() -> None:
    client = TestClient(app)
    expected_paths = [
        "/backoffice/pms-projections/products/sync",
        "/backoffice/pms-projections/units/sync",
        "/backoffice/pms-projections/sku-codes/sync",
        "/backoffice/pms-projections/barcodes/sync",
    ]

    for path in expected_paths:
        response = client.post(path)
        assert response.status_code == 401
        assert response.json() == {"detail": "backoffice_client_required"}


def test_pms_projection_read_apis_include_display_table_contract() -> None:
    client = TestClient(app)

    expected_paths = {
        "/backoffice/pms-projections/products": ("products", "d2c_pms_product_projection", "sku"),
        "/backoffice/pms-projections/units": ("units", "d2c_pms_unit_projection", "uom"),
        "/backoffice/pms-projections/sku-codes": (
            "sku_codes",
            "d2c_pms_sku_code_projection",
            "sku_code",
        ),
        "/backoffice/pms-projections/barcodes": (
            "barcodes",
            "d2c_pms_barcode_projection",
            "barcode",
        ),
    }

    for path, (resource, table_name, required_column_key) in expected_paths.items():
        response = client.get(path, headers=BACKOFFICE_HEADERS)

        assert response.status_code == 200
        payload = response.json()

        assert payload["resource"] == resource
        assert payload["projection_table"] == table_name
        assert isinstance(payload["columns"], list)
        assert isinstance(payload["rows"], list)

        column_keys = {column["key"] for column in payload["columns"]}
        assert required_column_key in column_keys
        assert "pms_updated_at" in column_keys
        assert "synced_at" in column_keys

        for column in payload["columns"]:
            assert set(column) == {"key", "label", "kind", "source_field"}
            assert column["key"]
            assert column["label"]
