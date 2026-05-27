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


def test_client_presentation_pc_web_home_draft_returns_aggregated_contract() -> None:
    client = TestClient(app)

    response = client.get(
        "/backoffice/client-presentation/pc-web/pages/home/draft",
        headers=BACKOFFICE_HEADERS,
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["surface_code"] == "web_desktop"
    assert payload["page_code"] == "home"
    assert payload["generated_from"] == "owner"

    summary = payload["summary"]
    assert summary["surface_code"] == "web_desktop"
    assert summary["page_code"] == "home"
    assert summary["region_count"] >= 4
    assert summary["region_block_count"] >= 5
    assert summary["active_region_block_count"] >= 5
    assert summary["visible_region_block_count"] >= 5
    assert summary["validation_blocking_issue_count"] == 0
    assert summary["runtime_sync_status"] == "backoffice_snapshot_ready"

    assert payload["validation"]["can_publish"] is True
    assert payload["runtime_status"]["runtime_sync_status"] == "backoffice_snapshot_ready"

    page = payload["page"]
    assert page["page_code"] == "home"
    assert page["route_path"] == "/"

    region_by_code = {region["region_code"]: region for region in page["regions"]}
    assert "home.main" in region_by_code

    block_by_code = {block["block_code"]: block for block in region_by_code["home.main"]["blocks"]}
    assert "home.title.main" in block_by_code
    assert "home.ad.main" in block_by_code
    assert "home.category.nav" in block_by_code
    assert "home.offer_shelf.cat_litter" in block_by_code
    assert "home.promotion.weekend" in block_by_code
    assert block_by_code["home.title.main"]["renderer_key"] == "pc_web.title"


def test_pc_web_home_planner_options_separates_inputs_choices_and_system_fields() -> None:
    client = TestClient(app)

    response = client.get(
        "/backoffice/client-presentation/pc-web/pages/home/planner-options",
        headers=BACKOFFICE_HEADERS,
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["surface_code"] == "web_desktop"
    assert payload["page_code"] == "home"

    region_types = {row["region_type"]: row for row in payload["region_types"]}
    assert "main" in region_types
    assert "offer_shelf" in region_types["main"]["allowed_block_types"]

    region_fields = {row["name"]: row for row in payload["region_form_fields"]}
    assert region_fields["region_type"]["control"] == "select"
    assert region_fields["title"]["control"] == "input"
    assert "region_code" in payload["system_fields"]
    assert "block_code" in payload["system_fields"]
    assert "renderer_key" in payload["system_fields"]

    block_types = {row["block_type"]: row for row in payload["block_types"]}
    assert set(block_types).issubset(
        {
            "title",
            "ad_banner",
            "promotion_strip",
            "promo_strip",
            "category_nav",
            "image_grid",
            "offer_shelf",
            "ranking_list",
            "product_recommendation",
            "rich_text",
        }
    )
    assert not any(block_type.startswith("client-block-") for block_type in block_types)
    assert block_types["title"]["renderer_key"] == "pc_web.title"
    assert "manual_inline" in block_types["title"]["content_source_types"]
    assert block_types["offer_shelf"]["renderer_key"] == "storefront.offer_shelf"
    assert "data_binding" in block_types["offer_shelf"]["content_source_types"]


def test_client_presentation_pc_web_home_authoring_creates_and_updates_region_and_block() -> None:
    client = TestClient(app)
    suffix = uuid4().hex[:8]

    region_response = client.post(
        "/backoffice/client-presentation/pc-web/pages/home/regions",
        headers=BACKOFFICE_HEADERS,
        json={
            "region_type": "footer",
            "title": f"页尾测试区域 {suffix}",
            "description": "pytest home planner region",
            "sort_order": 900,
            "is_required": False,
            "max_blocks": 4,
            "display_status": "visible",
            "is_active": True,
        },
    )
    assert region_response.status_code == 201
    region_payload = region_response.json()
    regions = {
        region["title"]: region
        for region in region_payload["page"]["regions"]
        if region["title"] == f"页尾测试区域 {suffix}"
    }
    assert f"页尾测试区域 {suffix}" in regions
    region_code = regions[f"页尾测试区域 {suffix}"]["region_code"]
    assert region_code.startswith("home.footer")

    update_region_response = client.patch(
        f"/backoffice/client-presentation/pc-web/pages/home/regions/{region_code}",
        headers=BACKOFFICE_HEADERS,
        json={"title": f"页尾测试区域已更新 {suffix}", "sort_order": 901},
    )
    assert update_region_response.status_code == 200
    updated_regions = {
        region["region_code"]: region for region in update_region_response.json()["page"]["regions"]
    }
    assert updated_regions[region_code]["title"] == f"页尾测试区域已更新 {suffix}"
    assert updated_regions[region_code]["sort_order"] == 901

    block_response = client.post(
        "/backoffice/client-presentation/pc-web/pages/home/regions/home.main/blocks",
        headers=BACKOFFICE_HEADERS,
        json={
            "block_type": "title",
            "title": f"测试标题 Block {suffix}",
            "subtitle": "pytest subtitle",
            "description": "pytest home planner block",
            "sort_order": 910,
            "display_status": "visible",
            "is_active": True,
            "content_source_type": "manual_inline",
            "content_payload": {
                "title": f"测试标题 Block {suffix}",
                "subtitle": "pytest subtitle",
            },
        },
    )
    assert block_response.status_code == 201
    block_payload = block_response.json()
    main_region = {region["region_code"]: region for region in block_payload["page"]["regions"]}[
        "home.main"
    ]
    blocks = {
        block["title"]: block
        for block in main_region["blocks"]
        if block["title"] == f"测试标题 Block {suffix}"
    }
    assert f"测试标题 Block {suffix}" in blocks
    block_code = blocks[f"测试标题 Block {suffix}"]["block_code"]
    assert block_code.startswith("home.main.title.")
    assert blocks[f"测试标题 Block {suffix}"]["renderer_key"] == "pc_web.title"

    update_block_response = client.patch(
        f"/backoffice/client-presentation/pc-web/pages/home/blocks/{block_code}",
        headers=BACKOFFICE_HEADERS,
        json={
            "title": f"测试标题 Block 已更新 {suffix}",
            "content_payload": {
                "title": f"测试标题 Block 已更新 {suffix}",
                "subtitle": "updated subtitle",
            },
        },
    )
    assert update_block_response.status_code == 200
    updated_main = {
        region["region_code"]: region for region in update_block_response.json()["page"]["regions"]
    }["home.main"]
    updated_blocks = {block["block_code"]: block for block in updated_main["blocks"]}
    assert updated_blocks[block_code]["title"] == f"测试标题 Block 已更新 {suffix}"
    assert updated_blocks[block_code]["renderer_key"] == "pc_web.title"


def test_client_presentation_pc_web_home_authoring_rejects_invalid_choice() -> None:
    client = TestClient(app)

    response = client.post(
        "/backoffice/client-presentation/pc-web/pages/home/regions/home.quick_nav/blocks",
        headers=BACKOFFICE_HEADERS,
        json={
            "block_type": "ad_banner",
            "title": "非法广告位",
            "sort_order": 10,
            "content_source_type": "manual_inline",
            "content_payload": {
                "items": [
                    {
                        "title": "非法广告",
                        "image_url": "https://example.test/banner.png",
                    }
                ]
            },
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "home_block_type_not_allowed"}


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
