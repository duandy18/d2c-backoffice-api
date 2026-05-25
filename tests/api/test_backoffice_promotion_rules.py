from __future__ import annotations

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app

BACKOFFICE_HEADERS = {"X-Backoffice-Client": "d2c-backoffice"}


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def unique_code(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:16].upper()}"


def promotion_rule_payload(promotion_code: str | None = None) -> dict[str, object]:
    return {
        "promotion_code": promotion_code or unique_code("PROMORULE"),
        "promotion_name": "猫粮周末九折",
        "description": "promotion rule management test",
        "promotion_type": "group_discount",
        "discount_type": "percentage",
        "discount_value": 10,
        "threshold_amount_cents": None,
        "max_discount_cents": None,
        "currency": "USD",
        "starts_at": None,
        "ends_at": None,
        "priority": 10,
        "stackable": False,
        "display_badge": "周末9折",
    }


def coupon_payload(coupon_code: str | None = None) -> dict[str, object]:
    return {
        "coupon_code": coupon_code or unique_code("COUPON"),
        "coupon_name": "测试优惠券",
        "coupon_type": "public_code",
        "total_limit": 100,
        "per_customer_limit": 1,
        "starts_at": None,
        "ends_at": None,
    }


def create_rule(client: TestClient) -> str:
    response = client.post(
        "/backoffice/promotion-rules",
        json=promotion_rule_payload(),
        headers=BACKOFFICE_HEADERS,
    )
    assert response.status_code == 201
    return response.json()["promotion_code"]


def test_backoffice_promotion_rules_requires_backoffice_client(client: TestClient) -> None:
    response = client.get("/backoffice/promotion-rules")

    assert response.status_code == 401
    assert response.json() == {"detail": "backoffice_client_required"}


def test_backoffice_promotion_rules_health(client: TestClient) -> None:
    response = client.get("/backoffice/promotion-rules/health", headers=BACKOFFICE_HEADERS)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "module": "backoffice_promotion_rules",
        "surface": "merchant_management",
    }


def test_backoffice_promotion_rules_create_activate_deactivate(client: TestClient) -> None:
    payload = promotion_rule_payload()

    create_response = client.post(
        "/backoffice/promotion-rules",
        json=payload,
        headers=BACKOFFICE_HEADERS,
    )

    assert create_response.status_code == 201
    body = create_response.json()
    assert body["promotion_code"] == payload["promotion_code"]
    assert body["promotion_name"] == "猫粮周末九折"
    assert body["promotion_type"] == "group_discount"
    assert body["discount_type"] == "percentage"
    assert body["status"] == "draft"
    assert body["is_active"] is False

    promotion_code = body["promotion_code"]

    activate_response = client.post(
        f"/backoffice/promotion-rules/{promotion_code}/activate",
        headers=BACKOFFICE_HEADERS,
    )
    assert activate_response.status_code == 200
    assert activate_response.json()["status"] == "active"
    assert activate_response.json()["is_active"] is True

    deactivate_response = client.post(
        f"/backoffice/promotion-rules/{promotion_code}/deactivate",
        headers=BACKOFFICE_HEADERS,
    )
    assert deactivate_response.status_code == 200
    assert deactivate_response.json()["status"] == "paused"
    assert deactivate_response.json()["is_active"] is False


def test_backoffice_promotion_rules_create_rejects_duplicate_code(client: TestClient) -> None:
    code = unique_code("DUPPROMORULE")
    payload = promotion_rule_payload(code)

    first_response = client.post(
        "/backoffice/promotion-rules",
        json=payload,
        headers=BACKOFFICE_HEADERS,
    )
    second_response = client.post(
        "/backoffice/promotion-rules",
        json=payload,
        headers=BACKOFFICE_HEADERS,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {"detail": "promotion_code_already_exists"}


def test_backoffice_promotion_rule_targets_and_coupons(client: TestClient) -> None:
    promotion_code = create_rule(client)

    target_response = client.post(
        f"/backoffice/promotion-rules/{promotion_code}/targets",
        json={"target_type": "group", "target_code": "cat_food"},
        headers=BACKOFFICE_HEADERS,
    )
    assert target_response.status_code == 201
    assert target_response.json()["promotion_code"] == promotion_code
    assert target_response.json()["target_type"] == "group"
    assert target_response.json()["target_code"] == "cat_food"

    targets_response = client.get("/backoffice/promotion-rules/targets", headers=BACKOFFICE_HEADERS)
    assert targets_response.status_code == 200
    assert any(
        target["promotion_code"] == promotion_code
        for target in targets_response.json()["promotion_targets"]
    )

    coupon_response = client.post(
        f"/backoffice/promotion-rules/{promotion_code}/coupons",
        json=coupon_payload(),
        headers=BACKOFFICE_HEADERS,
    )
    assert coupon_response.status_code == 201
    coupon_code = coupon_response.json()["coupon_code"]
    assert coupon_response.json()["coupon_name"] == "测试优惠券"
    assert coupon_response.json()["promotion_code"] == promotion_code
    assert coupon_response.json()["status"] == "draft"

    activate_coupon_response = client.post(
        f"/backoffice/promotion-rules/coupons/{coupon_code}/activate",
        headers=BACKOFFICE_HEADERS,
    )
    assert activate_coupon_response.status_code == 200
    assert activate_coupon_response.json()["status"] == "active"

    coupons_response = client.get("/backoffice/promotion-rules/coupons", headers=BACKOFFICE_HEADERS)
    assert coupons_response.status_code == 200
    assert any(
        coupon["coupon_code"] == coupon_code for coupon in coupons_response.json()["coupons"]
    )


def test_backoffice_promotion_rule_preview_matches_group_offer(client: TestClient) -> None:
    offer_code = unique_code("OFFER")
    price_code = unique_code("PRICE")

    offer_response = client.post(
        "/backoffice/offers",
        json={
            "offer_code": offer_code,
            "offer_type": "single",
            "title": "AKT 猫粮 1 袋",
            "subtitle": "适合成猫日常主粮",
            "description": "测试描述",
            "image_url": "https://example.test/offer.png",
            "display_status": "visible",
            "sell_status": "sellable",
            "publish_status": "draft",
            "source_type": "manual",
            "sort_order": 10,
        },
        headers=BACKOFFICE_HEADERS,
    )
    assert offer_response.status_code == 201

    price_response = client.post(
        f"/backoffice/offers/{offer_code}/prices",
        json={
            "price_code": price_code,
            "channel": "storefront",
            "currency": "USD",
            "price_cents": 1999,
            "compare_at_price_cents": 2199,
            "is_active": True,
            "priority": 10,
        },
        headers=BACKOFFICE_HEADERS,
    )
    assert price_response.status_code == 201

    position_response = client.post(
        f"/backoffice/offers/{offer_code}/positions",
        json={
            "group_code": "cat_food",
            "position_code": unique_code("POS"),
            "sort_order": 1,
            "position_source": "manual",
            "is_featured": True,
            "is_active": True,
        },
        headers=BACKOFFICE_HEADERS,
    )
    assert position_response.status_code == 201

    promotion_code = create_rule(client)
    target_response = client.post(
        f"/backoffice/promotion-rules/{promotion_code}/targets",
        json={"target_type": "group", "target_code": "cat_food"},
        headers=BACKOFFICE_HEADERS,
    )
    assert target_response.status_code == 201

    preview_response = client.post(
        f"/backoffice/promotion-rules/{promotion_code}/preview",
        headers=BACKOFFICE_HEADERS,
    )

    assert preview_response.status_code == 200
    payload = preview_response.json()
    assert payload["matched_offer_count"] >= 1
    offer_by_code = {offer["offer_code"]: offer for offer in payload["offers"]}
    preview = offer_by_code[offer_code]
    assert preview["base_price_cents"] == 1999
    assert preview["final_price_cents"] == 1800
    assert preview["discount_cents"] == 199
    assert preview["promotion_badges"] == ["周末9折"]
    assert "cat_food" in preview["group_codes"]
