from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import load_settings
from app.core.database import get_session_factory
from app.domains.groups.models.group import Group
from app.domains.offers.models.offer import Offer, OfferComponent, OfferPosition, OfferPrice
from app.domains.pms_projection.models import (
    PmsBarcodeProjection,
    PmsProductProjection,
    PmsSkuCodeProjection,
    PmsUnitProjection,
)
from app.domains.promotions.models.promotion_rule import Coupon, PromotionRule, PromotionTarget
from app.main import app

BACKOFFICE_HEADERS = {"X-Backoffice-Client": "d2c-backoffice"}
SERVICE_HEADERS = {"X-Service-Client": "d2c-service"}


def unique_code(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12].upper()}"


def seed_snapshot_owner_data() -> dict[str, str]:
    settings = load_settings()
    session_factory = get_session_factory(settings.test_database_url)
    now = datetime.now(UTC)

    group_code = unique_code("GROUP")
    offer_code = unique_code("OFFER")
    price_code = unique_code("PRICE")
    position_code = unique_code("POS")
    promotion_code = unique_code("PROMO")
    coupon_code = unique_code("COUPON")
    sku_code = unique_code("SKU")
    barcode_value = unique_code("690")

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
                sku_code=sku_code,
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
                barcode=barcode_value,
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

        group = Group(
            group_code=group_code,
            group_name="测试 Group",
            group_kind="category",
            description="pytest group",
            image_url=None,
            sort_order=999,
            display_status="visible",
            is_active=True,
            source_type="manual",
            source_ref=None,
        )
        session.add(group)
        session.flush()

        offer = Offer(
            offer_code=offer_code,
            offer_type="single",
            title="AKT 猫粮 1 袋",
            subtitle="适合成猫日常主粮",
            description="pytest offer",
            image_url="https://example.test/offer.png",
            display_status="visible",
            sell_status="sellable",
            publish_status="draft",
            source_type="manual",
            sort_order=10,
            visible_from=None,
            visible_until=None,
        )
        session.add(offer)
        session.flush()

        session.add(
            OfferComponent(
                offer_id=offer.id,
                component_no=1,
                pms_item_id=pms_item_id,
                pms_sku="PMS-SNAPSHOT",
                pms_sku_code_id=pms_sku_code_id,
                sku_code=sku_code,
                pms_item_uom_id=pms_item_uom_id,
                uom_code="bag",
                uom_name="袋",
                pms_barcode_id=pms_barcode_id,
                barcode=barcode_value,
                quantity=Decimal("1.000000"),
                component_role="primary",
                sort_order=10,
                required=True,
                raw_payload={"source": "pytest"},
            )
        )
        session.add(
            OfferPrice(
                offer_id=offer.id,
                price_code=price_code,
                channel="storefront",
                currency="USD",
                price_cents=1999,
                compare_at_price_cents=2199,
                effective_from=None,
                effective_until=None,
                is_active=True,
                priority=10,
            )
        )
        session.add(
            OfferPosition(
                position_code=position_code,
                group_id=group.id,
                offer_id=offer.id,
                sort_order=1,
                position_source="manual",
                is_featured=True,
                visible_from=None,
                visible_until=None,
                is_active=True,
            )
        )

        promotion_rule = PromotionRule(
            promotion_code=promotion_code,
            promotion_name="猫粮周末九折",
            description="pytest promotion",
            promotion_type="group_discount",
            discount_type="percentage",
            discount_value=10,
            threshold_amount_cents=None,
            max_discount_cents=None,
            currency="USD",
            starts_at=None,
            ends_at=None,
            status="active",
            priority=10,
            stackable=False,
            is_active=True,
            display_badge="周末9折",
        )
        session.add(promotion_rule)
        session.flush()

        session.add(
            PromotionTarget(
                promotion_rule_id=promotion_rule.id,
                target_type="group",
                target_id=group.id,
                target_code=group_code,
            )
        )
        session.add(
            Coupon(
                coupon_code=coupon_code,
                coupon_name="新人券",
                promotion_rule_id=promotion_rule.id,
                coupon_type="public_code",
                total_limit=100,
                per_customer_limit=1,
                starts_at=None,
                ends_at=None,
                status="active",
                is_active=True,
            )
        )
        session.commit()

    return {
        "group_code": group_code,
        "offer_code": offer_code,
        "price_code": price_code,
        "position_code": position_code,
        "promotion_code": promotion_code,
        "coupon_code": coupon_code,
        "sku_code": sku_code,
    }


def test_backoffice_publish_creates_terminal_snapshot_and_exports() -> None:
    values = seed_snapshot_owner_data()
    publish_version = unique_code("PUB")
    client = TestClient(app)

    publish_response = client.post(
        "/backoffice/publish",
        json={
            "publish_version": publish_version,
            "published_by": "pytest",
            "note": "terminal snapshot test",
        },
        headers=BACKOFFICE_HEADERS,
    )

    assert publish_response.status_code == 201
    assert publish_response.json()["publish_version"] == publish_version
    assert publish_response.json()["status"] == "published"

    groups_response = client.get(
        "/backoffice/read/v1/published/snapshot/groups",
        params={"publish_version": publish_version},
        headers=SERVICE_HEADERS,
    )
    offers_response = client.get(
        "/backoffice/read/v1/published/snapshot/offers",
        params={"publish_version": publish_version},
        headers=SERVICE_HEADERS,
    )
    components_response = client.get(
        "/backoffice/read/v1/published/snapshot/offer-components",
        params={"publish_version": publish_version},
        headers=SERVICE_HEADERS,
    )
    prices_response = client.get(
        "/backoffice/read/v1/published/snapshot/offer-prices",
        params={"publish_version": publish_version},
        headers=SERVICE_HEADERS,
    )
    positions_response = client.get(
        "/backoffice/read/v1/published/snapshot/offer-positions",
        params={"publish_version": publish_version},
        headers=SERVICE_HEADERS,
    )
    rules_response = client.get(
        "/backoffice/read/v1/published/snapshot/promotion-rules",
        params={"publish_version": publish_version},
        headers=SERVICE_HEADERS,
    )
    targets_response = client.get(
        "/backoffice/read/v1/published/snapshot/promotion-targets",
        params={"publish_version": publish_version},
        headers=SERVICE_HEADERS,
    )
    coupons_response = client.get(
        "/backoffice/read/v1/published/snapshot/coupons",
        params={"publish_version": publish_version},
        headers=SERVICE_HEADERS,
    )

    for response in (
        groups_response,
        offers_response,
        components_response,
        prices_response,
        positions_response,
        rules_response,
        targets_response,
        coupons_response,
    ):
        assert response.status_code == 200

    groups = {row["group_code"]: row for row in groups_response.json()["groups"]}
    offers = {row["offer_code"]: row for row in offers_response.json()["offers"]}
    components = {row["offer_code"]: row for row in components_response.json()["components"]}
    prices = {row["price_code"]: row for row in prices_response.json()["prices"]}
    positions = {row["position_code"]: row for row in positions_response.json()["positions"]}
    rules = {row["promotion_code"]: row for row in rules_response.json()["promotion_rules"]}
    targets = {
        (row["promotion_code"], row["target_code"]): row
        for row in targets_response.json()["promotion_targets"]
    }
    coupons = {row["coupon_code"]: row for row in coupons_response.json()["coupons"]}

    assert groups[values["group_code"]]["group_name"] == "测试 Group"
    assert offers[values["offer_code"]]["title"] == "AKT 猫粮 1 袋"
    assert components[values["offer_code"]]["sku_code"] == values["sku_code"]
    assert prices[values["price_code"]]["price_cents"] == 1999
    assert positions[values["position_code"]]["group_code"] == values["group_code"]
    assert rules[values["promotion_code"]]["display_badge"] == "周末9折"
    assert targets[(values["promotion_code"], values["group_code"])]["target_type"] == "group"
    assert coupons[values["coupon_code"]]["coupon_name"] == "新人券"


def test_published_snapshot_requires_service_client() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/read/v1/published/snapshot/groups")

    assert response.status_code == 401
    assert response.json() == {"detail": "service_client_required"}

def test_backoffice_publish_exports_storefront_section_positions() -> None:
    client = TestClient(app)
    publish_version = unique_code("PUB-SEC-POS")
    offer_code = unique_code("OFFER-SEC-POS")
    section_code = unique_code("SECTION-SEC-POS")
    position_code = unique_code("SEC-POS")

    offer_response = client.post(
        "/backoffice/offers",
        json={
            "offer_code": offer_code,
            "offer_type": "single",
            "title": "SectionPosition 发布测试商品",
            "subtitle": "精准货架坑位",
            "description": "pytest section position snapshot",
            "image_url": "https://example.test/section-position-snapshot.png",
            "display_status": "visible",
            "sell_status": "sellable",
            "publish_status": "draft",
            "source_type": "manual",
            "sort_order": 10,
        },
        headers=BACKOFFICE_HEADERS,
    )
    assert offer_response.status_code == 201

    section_response = client.post(
        "/backoffice/storefront-sections",
        json={
            "section_code": section_code,
            "section_type": "offer_shelf",
            "group_code": "cat_litter",
            "title": "SectionPosition 发布测试货架",
            "sort_order": 10,
        },
        headers=BACKOFFICE_HEADERS,
    )
    assert section_response.status_code == 201

    position_response = client.post(
        f"/backoffice/storefront-sections/{section_code}/positions",
        json={
            "offer_code": offer_code,
            "position_code": position_code,
            "sort_order": 1,
            "position_type": "manual",
            "is_featured": True,
            "is_active": True,
            "source_type": "manual",
        },
        headers=BACKOFFICE_HEADERS,
    )
    assert position_response.status_code == 201

    publish_response = client.post(
        "/backoffice/publish",
        json={
            "publish_version": publish_version,
            "published_by": "pytest",
            "note": "section position snapshot test",
        },
        headers=BACKOFFICE_HEADERS,
    )
    assert publish_response.status_code == 201

    export_response = client.get(
        "/backoffice/read/v1/published/snapshot/storefront-section-positions",
        params={"publish_version": publish_version},
        headers=SERVICE_HEADERS,
    )
    assert export_response.status_code == 200

    positions = {
        row["position_code"]: row
        for row in export_response.json()["positions"]
    }
    assert positions[position_code]["section_code"] == section_code
    assert positions[position_code]["offer_code"] == offer_code
    assert positions[position_code]["position_type"] == "manual"
    assert positions[position_code]["is_featured"] is True
