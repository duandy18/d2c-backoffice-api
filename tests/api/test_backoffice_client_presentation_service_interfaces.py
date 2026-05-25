from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

BACKOFFICE_HEADERS = {"X-Backoffice-Client": "d2c-backoffice"}


def test_client_presentation_preview_returns_page_protocol() -> None:
    client = TestClient(app)

    response = client.get(
        "/backoffice/client-presentation/preview",
        headers=BACKOFFICE_HEADERS,
        params={"page_code": "home", "surface_code": "web_desktop"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["page_code"] == "home"
    assert payload["surface_code"] == "web_desktop"
    assert payload["generated_from"] == "owner"

    page = payload["page"]
    assert page["page_code"] == "home"
    assert page["route_path"] == "/"
    region_by_code = {region["region_code"]: region for region in page["regions"]}
    assert "home.main" in region_by_code
    assert "offer_shelf" in region_by_code["home.main"]["allowed_block_types"]


def test_client_presentation_preview_rejects_missing_page() -> None:
    client = TestClient(app)

    response = client.get(
        "/backoffice/client-presentation/preview",
        headers=BACKOFFICE_HEADERS,
        params={"page_code": f"missing-{uuid4().hex[:8]}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "client_page_not_found"}


def test_client_presentation_validation_report_is_publishable_for_seeded_contract() -> None:
    client = TestClient(app)

    response = client.get(
        "/backoffice/client-presentation/validation-report",
        headers=BACKOFFICE_HEADERS,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["can_publish"] is True
    assert payload["blocking_issue_count"] == 0
    assert payload["checked_counts"]["pages"] >= 5
    assert payload["checked_counts"]["block_types"] >= 10
    assert payload["checked_counts"]["surfaces"] >= 3


def test_client_presentation_publish_runtime_status_counts_latest_snapshot() -> None:
    client = TestClient(app)
    publish_version = f"pub-service-iface-{uuid4().hex[:8]}"

    publish_response = client.post(
        "/backoffice/publish",
        headers=BACKOFFICE_HEADERS,
        json={
            "publish_version": publish_version,
            "published_by": "pytest",
            "note": "client presentation service interfaces",
        },
    )
    assert publish_response.status_code == 201

    status_response = client.get(
        "/backoffice/client-presentation/publish-runtime-status",
        headers=BACKOFFICE_HEADERS,
    )

    assert status_response.status_code == 200
    payload = status_response.json()
    assert payload["latest_publish_version"] == publish_version
    assert payload["runtime_sync_status"] == "backoffice_snapshot_ready"

    counts = {row["name"]: row for row in payload["snapshot_counts"]}
    assert counts["client_pages"]["owner_count"] >= 5
    assert counts["client_pages"]["latest_snapshot_count"] >= 5
    assert counts["client_surfaces"]["owner_count"] >= 3
    assert counts["client_surfaces"]["latest_snapshot_count"] >= 3
    assert counts["storefront_sections"]["latest_snapshot_count"] >= 0
