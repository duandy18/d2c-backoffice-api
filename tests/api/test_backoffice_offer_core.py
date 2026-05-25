from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.config import load_settings
from app.core.database import get_session_factory
from app.domains.pms_projection.models import (
    PmsBarcodeProjection,
    PmsProductProjection,
    PmsSkuCodeProjection,
    PmsUnitProjection,
)
from app.main import app

BACKOFFICE_HEADERS = {"X-Backoffice-Client": "d2c-backoffice"}


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def unique_code(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12].upper()}"


def seed_pms_component_source() -> dict[str, int]:
    settings = load_settings()
    session_factory = get_session_factory(settings.test_database_url)
    now = datetime.now(UTC)

    pms_item_id = int(uuid4().int % 1_000_000_000)
    pms_item_uom_id = int(uuid4().int % 1_000_000_000)
    pms_sku_code_id = int(uuid4().int % 1_000_000_000)
    pms_barcode_id = int(uuid4().int % 1_000_000_000)

    with session_factory() as session:
        session.add(
            PmsProductProjection(
                pms_item_id=pms_item_id,
                pms_sku=unique_code("PMS"),
                item_name="测试 PMS 商品",
                item_spec="1kg",
                enabled=True,
                supplier_id=None,
                brand_id=None,
                brand_code="brand_test",
                brand_name="测试品牌",
                category_id=None,
                category_code="cat_food",
                category_name="猫粮",
                category_path_code=None,
                category_level=None,
                category_is_leaf=None,
                pms_updated_at=now,
                raw_payload={"source": "pytest"},
            )
        )
        session.flush()

        session.add(
            PmsUnitProjection(
                pms_item_uom_id=pms_item_uom_id,
                pms_item_id=pms_item_id,
                uom="bag",
                uom_name="袋",
                display_name="袋",
                ratio_to_base=Decimal("1.000000"),
                net_weight_kg=Decimal("1.000000"),
                is_base=True,
                is_purchase_default=False,
                is_inbound_default=False,
                is_outbound_default=True,
                pms_updated_at=now,
                raw_payload={"source": "pytest"},
            )
        )
        session.add(
            PmsSkuCodeProjection(
                pms_sku_code_id=pms_sku_code_id,
                pms_item_id=pms_item_id,
                sku_code=unique_code("SKU"),
                code_type="primary",
                is_primary=True,
                is_active=True,
                effective_from=None,
                effective_to=None,
                remark=None,
                item_sku=unique_code("PMS-SKU"),
                item_name="测试 PMS 商品",
                item_enabled=True,
                pms_updated_at=now,
                raw_payload={"source": "pytest"},
            )
        )
        session.flush()

        session.add(
            PmsBarcodeProjection(
                pms_barcode_id=pms_barcode_id,
                pms_item_id=pms_item_id,
                pms_item_uom_id=pms_item_uom_id,
                barcode=unique_code("690"),
                symbology="EAN13",
                active=True,
                is_primary=True,
                uom="bag",
                uom_name="袋",
                ratio_to_base=Decimal("1.000000"),
                pms_updated_at=now,
                raw_payload={"source": "pytest"},
            )
        )
        session.commit()

    return {
        "pms_item_id": pms_item_id,
        "pms_item_uom_id": pms_item_uom_id,
        "pms_sku_code_id": pms_sku_code_id,
        "pms_barcode_id": pms_barcode_id,
    }


def test_backoffice_groups_require_client(client: TestClient) -> None:
    response = client.get("/backoffice/groups")

    assert response.status_code == 401
    assert response.json() == {"detail": "backoffice_client_required"}


def test_backoffice_groups_list_contains_terminal_seed_groups(client: TestClient) -> None:
    response = client.get("/backoffice/groups", headers=BACKOFFICE_HEADERS)

    assert response.status_code == 200
    payload = response.json()
    group_codes = {group["group_code"] for group in payload["groups"]}

    assert {
        "all",
        "cat_food",
        "cat_litter",
        "cat_canned",
        "cat_treats",
        "cat_supplies",
        "new_arrivals",
        "hot_rank",
        "bundles",
    }.issubset(group_codes)


def test_backoffice_create_offer_component_price_position_and_publish_check(
    client: TestClient,
) -> None:
    offer_code = unique_code("OFFER")
    component_source = seed_pms_component_source()

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
    assert offer_response.json()["offer_code"] == offer_code

    component_response = client.post(
        f"/backoffice/offers/{offer_code}/components",
        json={
            "pms_item_id": component_source["pms_item_id"],
            "pms_sku_code_id": component_source["pms_sku_code_id"],
            "pms_item_uom_id": component_source["pms_item_uom_id"],
            "pms_barcode_id": component_source["pms_barcode_id"],
            "quantity": "1.000000",
            "component_role": "primary",
            "sort_order": 10,
            "required": True,
        },
        headers=BACKOFFICE_HEADERS,
    )

    assert component_response.status_code == 201
    assert component_response.json()["pms_item_id"] == component_source["pms_item_id"]

    price_response = client.post(
        f"/backoffice/offers/{offer_code}/prices",
        json={
            "price_code": unique_code("PRICE"),
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
    assert price_response.json()["price_cents"] == 1999

    section_code = unique_code("SECTION")
    section_response = client.post(
        "/backoffice/storefront-sections",
        json={
            "section_code": section_code,
            "section_type": "offer_shelf",
            "group_code": "cat_food",
            "title": "猫粮主推",
            "sort_order": 1,
        },
        headers=BACKOFFICE_HEADERS,
    )
    assert section_response.status_code == 201

    position_response = client.post(
        f"/backoffice/storefront-sections/{section_code}/positions",
        json={
            "offer_code": offer_code,
            "position_code": unique_code("SEC-POS"),
            "sort_order": 1,
            "position_type": "manual",
            "is_featured": True,
            "is_active": True,
            "source_type": "manual",
        },
        headers=BACKOFFICE_HEADERS,
    )

    assert position_response.status_code == 201
    assert position_response.json()["section_code"] == section_code
    assert position_response.json()["offer_code"] == offer_code

    check_response = client.get(
        f"/backoffice/offers/{offer_code}/publish-check",
        headers=BACKOFFICE_HEADERS,
    )

    assert check_response.status_code == 200
    assert check_response.json() == {
        "offer_code": offer_code,
        "can_publish": True,
        "blocking_reasons": [],
        "has_component": True,
        "has_active_price": True,
        "has_section_position": True,
        "has_title": True,
        "has_image": True,
        "is_visible": True,
        "is_sellable": True,
    }
