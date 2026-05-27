from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

BACKOFFICE_HEADERS = {"X-Backoffice-Client": "d2c-backoffice"}
SERVICE_HEADERS = {"X-Service-Client": "d2c-service"}


def unique_code(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


def test_client_presentation_lists_seeded_protocol_services() -> None:
    client = TestClient(app)

    responses = {
        "surfaces": client.get(
            "/backoffice/client-presentation/surfaces",
            headers=BACKOFFICE_HEADERS,
        ),
        "data_bindings": client.get(
            "/backoffice/client-presentation/data-bindings", headers=BACKOFFICE_HEADERS
        ),
        "visibility_rules": client.get(
            "/backoffice/client-presentation/visibility-rules", headers=BACKOFFICE_HEADERS
        ),
        "action_policies": client.get(
            "/backoffice/client-presentation/action-policies", headers=BACKOFFICE_HEADERS
        ),
        "tracking_policies": client.get(
            "/backoffice/client-presentation/tracking-policies", headers=BACKOFFICE_HEADERS
        ),
    }

    for response in responses.values():
        assert response.status_code == 200

    surfaces = {row["surface_code"]: row for row in responses["surfaces"].json()["surfaces"]}
    bindings = {
        row["binding_code"]: row for row in responses["data_bindings"].json()["data_bindings"]
    }
    visibility = {
        row["rule_code"]: row for row in responses["visibility_rules"].json()["visibility_rules"]
    }
    actions = {
        row["policy_code"]: row for row in responses["action_policies"].json()["action_policies"]
    }
    tracking = {
        row["policy_code"]: row
        for row in responses["tracking_policies"].json()["tracking_policies"]
    }

    assert "storefront.offer_shelf" in surfaces["web_desktop"]["supported_renderer_keys"]
    assert bindings["binding.home.main.offer_shelf.manual"]["content_type"] == "offer"
    assert visibility["visibility.default.all_surfaces"]["login_state"] == "any"
    assert actions["action.offer_shelf.open_offer"]["target_page_code"] == "product_detail"
    assert tracking["tracking.offer_shelf.add_to_cart"]["event_type"] == "conversion"


def test_client_presentation_create_protocol_service_rows() -> None:
    client = TestClient(app)
    suffix = uuid4().hex[:8]

    surface_response = client.post(
        "/backoffice/client-presentation/surfaces",
        headers=BACKOFFICE_HEADERS,
        json={
            "surface_code": f"surface-{suffix}",
            "surface_name": "测试客户端渠道",
            "surface_type": "web",
            "device_family": "desktop",
            "breakpoint_profile": {"min_width": 1200},
            "supported_renderer_keys": ["storefront.offer_shelf"],
            "is_active": True,
            "source_type": "manual",
        },
    )
    assert surface_response.status_code == 201

    binding_response = client.post(
        "/backoffice/client-presentation/data-bindings",
        headers=BACKOFFICE_HEADERS,
        json={
            "binding_code": f"binding-{suffix}",
            "target_type": "block_type",
            "target_code": "offer_shelf",
            "data_source_type": "manual_positions",
            "data_source_ref": "pytest",
            "content_type": "offer",
            "query_params": {"pytest": True},
            "result_limit": 5,
            "sort_policy": {"order_by": ["sort_order"]},
            "refresh_policy": {"mode": "publish_snapshot"},
            "is_active": True,
            "source_type": "manual",
        },
    )
    assert binding_response.status_code == 201

    visibility_response = client.post(
        "/backoffice/client-presentation/visibility-rules",
        headers=BACKOFFICE_HEADERS,
        json={
            "rule_code": f"visibility-{suffix}",
            "target_type": "block_type",
            "target_code": "offer_shelf",
            "client_surface_codes": ["web_desktop"],
            "customer_segments": ["all"],
            "login_state": "any",
            "rule_expression": {"allow": True},
            "priority": 1,
            "is_active": True,
            "source_type": "manual",
        },
    )
    assert visibility_response.status_code == 201

    action_response = client.post(
        "/backoffice/client-presentation/action-policies",
        headers=BACKOFFICE_HEADERS,
        json={
            "policy_code": f"action-{suffix}",
            "target_type": "block_type",
            "target_code": "offer_shelf",
            "action_type": "open_offer",
            "label": "查看商品",
            "target_page_code": "product_detail",
            "target_ref": "offer_code",
            "open_mode": "same",
            "action_payload": {"param": "offer_code"},
            "is_active": True,
            "source_type": "manual",
        },
    )
    assert action_response.status_code == 201

    tracking_response = client.post(
        "/backoffice/client-presentation/tracking-policies",
        headers=BACKOFFICE_HEADERS,
        json={
            "policy_code": f"tracking-{suffix}",
            "target_type": "block_type",
            "target_code": "offer_shelf",
            "event_name": "pytest_event",
            "event_type": "click",
            "event_trigger": "click",
            "tracking_params": {"include": ["offer_code"]},
            "is_required": True,
            "is_active": True,
            "source_type": "manual",
        },
    )
    assert tracking_response.status_code == 201


def test_client_presentation_protocol_services_publish_exports() -> None:
    client = TestClient(app)
    publish_version = unique_code("pub-protocol")

    publish_response = client.post(
        "/backoffice/publish",
        headers=BACKOFFICE_HEADERS,
        json={
            "publish_version": publish_version,
            "published_by": "pytest",
            "note": "client presentation protocol services",
        },
    )
    assert publish_response.status_code == 201

    paths = {
        "surfaces": "/backoffice/read/v1/published/snapshot/client-surfaces",
        "data_bindings": "/backoffice/read/v1/published/snapshot/client-data-bindings",
        "visibility_rules": "/backoffice/read/v1/published/snapshot/client-visibility-rules",
        "action_policies": "/backoffice/read/v1/published/snapshot/client-action-policies",
        "tracking_policies": "/backoffice/read/v1/published/snapshot/client-tracking-policies",
    }

    payloads = {}
    for key, path in paths.items():
        response = client.get(
            path,
            headers=SERVICE_HEADERS,
            params={"publish_version": publish_version},
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["publish_version"] == publish_version
        assert payload["count"] > 0
        payloads[key] = payload

    surfaces = {row["surface_code"]: row for row in payloads["surfaces"]["surfaces"]}
    assert "web_desktop" in surfaces
    assert "storefront.offer_shelf" in surfaces["web_desktop"]["supported_renderer_keys"]

    bindings = {row["binding_code"]: row for row in payloads["data_bindings"]["data_bindings"]}
    assert bindings["binding.home.main.offer_shelf.manual"]["content_type"] == "offer"

    actions = {row["policy_code"]: row for row in payloads["action_policies"]["action_policies"]}
    assert actions["action.offer_shelf.open_offer"]["action_type"] == "open_offer"


def test_client_presentation_region_blocks_publish_exports() -> None:
    client = TestClient(app)
    publish_version = unique_code("pub-region-block")

    publish_response = client.post(
        "/backoffice/publish",
        headers=BACKOFFICE_HEADERS,
        json={
            "publish_version": publish_version,
            "published_by": "pytest",
            "note": "client region blocks snapshot",
        },
    )
    assert publish_response.status_code == 201

    export_response = client.get(
        "/backoffice/read/v1/published/snapshot/client-region-blocks",
        headers=SERVICE_HEADERS,
        params={"publish_version": publish_version},
    )
    assert export_response.status_code == 200

    payload = export_response.json()
    assert payload["publish_version"] == publish_version
    blocks = {row["block_code"]: row for row in payload["region_blocks"]}

    assert "home.title.main" in blocks
    assert blocks["home.title.main"]["page_code"] == "home"
    assert blocks["home.title.main"]["region_code"] == "home.main"
    assert blocks["home.title.main"]["renderer_key"] == "pc_web.title"
