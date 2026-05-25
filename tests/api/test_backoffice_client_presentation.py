from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

BACKOFFICE_HEADERS = {"X-Backoffice-Client": "d2c-backoffice"}
SERVICE_HEADERS = {"X-Service-Client": "d2c-service"}


def unique_code(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


def test_client_presentation_requires_backoffice_client() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/client-presentation/pages")

    assert response.status_code == 401
    assert response.json() == {"detail": "backoffice_client_required"}


def test_client_presentation_lists_seeded_foundation() -> None:
    client = TestClient(app)

    pages_response = client.get(
        "/backoffice/client-presentation/pages",
        headers=BACKOFFICE_HEADERS,
    )
    regions_response = client.get(
        "/backoffice/client-presentation/regions",
        headers=BACKOFFICE_HEADERS,
    )
    block_types_response = client.get(
        "/backoffice/client-presentation/block-types",
        headers=BACKOFFICE_HEADERS,
    )

    assert pages_response.status_code == 200
    assert regions_response.status_code == 200
    assert block_types_response.status_code == 200

    pages = {row["page_code"]: row for row in pages_response.json()["pages"]}
    regions = {row["region_code"]: row for row in regions_response.json()["regions"]}
    block_types = {row["block_type"]: row for row in block_types_response.json()["block_types"]}

    assert pages["home"]["route_path"] == "/"
    assert regions["home.main"]["page_code"] == "home"
    assert "offer_shelf" in regions["home.main"]["allowed_block_types"]
    assert block_types["offer_shelf"]["renderer_key"] == "storefront.offer_shelf"
    assert "offer" in block_types["offer_shelf"]["allowed_content_types"]


def test_client_presentation_create_page_region_and_block_type() -> None:
    client = TestClient(app)
    page_code = unique_code("client-page")
    region_code = unique_code("client-region")
    block_type = unique_code("client-block").lower()

    page_response = client.post(
        "/backoffice/client-presentation/pages",
        headers=BACKOFFICE_HEADERS,
        json={
            "page_code": page_code,
            "page_type": "landing",
            "route_path": f"/landing/{page_code}",
            "title": "测试落地页",
            "description": "pytest client page",
            "sort_order": 99,
            "display_status": "visible",
            "is_active": True,
            "source_type": "manual",
        },
    )
    assert page_response.status_code == 201
    assert page_response.json()["page_code"] == page_code

    region_response = client.post(
        f"/backoffice/client-presentation/pages/{page_code}/regions",
        headers=BACKOFFICE_HEADERS,
        json={
            "region_code": region_code,
            "region_type": "main",
            "title": "测试区域",
            "description": "pytest client region",
            "sort_order": 1,
            "is_required": True,
            "max_blocks": 3,
            "allowed_block_types": ["hero_banner", "offer_shelf"],
            "display_status": "visible",
            "is_active": True,
            "source_type": "manual",
        },
    )
    assert region_response.status_code == 201
    assert region_response.json()["page_code"] == page_code
    assert region_response.json()["allowed_block_types"] == ["hero_banner", "offer_shelf"]

    block_response = client.post(
        "/backoffice/client-presentation/block-types",
        headers=BACKOFFICE_HEADERS,
        json={
            "block_type": block_type,
            "display_name": "测试区块类型",
            "description": "pytest block type",
            "renderer_key": f"storefront.{block_type}",
            "data_contract_version": "v1",
            "allowed_region_types": ["main"],
            "allowed_content_types": ["offer"],
            "layout_schema": {"required": ["display_type"]},
            "slot_schema": {"slots": ["positions"]},
            "action_schema": {"actions": ["open_offer"]},
            "analytics_schema": {"events": ["impression", "click"]},
            "display_status": "visible",
            "is_active": True,
            "source_type": "manual",
        },
    )
    assert block_response.status_code == 201
    assert block_response.json()["block_type"] == block_type


def test_client_presentation_publish_exports_foundation_snapshots() -> None:
    client = TestClient(app)
    publish_version = unique_code("pub-client-pres")

    publish_response = client.post(
        "/backoffice/publish",
        headers=BACKOFFICE_HEADERS,
        json={
            "publish_version": publish_version,
            "published_by": "pytest",
            "note": "client presentation foundation snapshot",
        },
    )
    assert publish_response.status_code == 201

    pages_response = client.get(
        "/backoffice/read/v1/published/snapshot/client-pages",
        headers=SERVICE_HEADERS,
        params={"publish_version": publish_version},
    )
    regions_response = client.get(
        "/backoffice/read/v1/published/snapshot/client-regions",
        headers=SERVICE_HEADERS,
        params={"publish_version": publish_version},
    )
    block_types_response = client.get(
        "/backoffice/read/v1/published/snapshot/client-block-types",
        headers=SERVICE_HEADERS,
        params={"publish_version": publish_version},
    )

    assert pages_response.status_code == 200
    assert regions_response.status_code == 200
    assert block_types_response.status_code == 200

    pages = {row["page_code"]: row for row in pages_response.json()["pages"]}
    regions = {row["region_code"]: row for row in regions_response.json()["regions"]}
    block_types = {
        row["block_type"]: row for row in block_types_response.json()["block_types"]
    }

    assert pages["home"]["route_path"] == "/"
    assert regions["home.main"]["page_code"] == "home"
    assert block_types["offer_shelf"]["renderer_key"] == "storefront.offer_shelf"
