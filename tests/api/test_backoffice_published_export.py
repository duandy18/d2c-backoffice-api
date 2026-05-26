from datetime import UTC, datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import load_settings
from app.core.database import get_session_factory
from app.domains.promotions.models.promotion_rule import Coupon, PromotionRule
from app.domains.publish.models.publish_version import PublishVersion
from app.main import app

SERVICE_HEADERS = {"X-Service-Client": "d2c-service"}


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12].upper()}"


def _seed_promotion_coupon_export_data() -> dict[str, str]:
    settings = load_settings()
    session_factory = get_session_factory(settings.test_database_url)
    now = datetime.now(UTC)

    publish_version = _unique("PUB")
    promotion_code = _unique("PROMO")
    coupon_code = _unique("COUPON")

    with session_factory() as session:
        session.add(
            PublishVersion(
                publish_version=publish_version,
                publish_scope="all",
                status="published",
                source="manual",
                started_at=now,
                published_at=now,
                published_by="pytest",
                note="published export contract test",
            )
        )

        promotion = PromotionRule(
            promotion_code=promotion_code,
            promotion_name="测试促销",
            description="pytest promotion",
            promotion_type="store_campaign",
            discount_type="percentage",
            discount_value=10,
            max_discount_cents=None,
            currency="USD",
            starts_at=None,
            ends_at=None,
            status="active",
            priority=10,
            stackable=False,
            is_active=True,
            display_badge="测试促销",
        )
        session.add(promotion)
        session.flush()

        session.add(
            Coupon(
                coupon_code=coupon_code,
                coupon_name="测试优惠券",
                promotion_rule_id=promotion.id,
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
        "publish_version": publish_version,
        "promotion_code": promotion_code,
        "coupon_code": coupon_code,
    }


def test_published_export_requires_service_client() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/read/v1/published/promotions")

    assert response.status_code == 401
    assert response.json() == {"detail": "service_client_required"}


def test_legacy_published_catalog_and_prices_exports_are_retired() -> None:
    client = TestClient(app)

    for path in (
        "/backoffice/read/v1/published/catalog",
        "/backoffice/read/v1/published/prices",
    ):
        response = client.get(path, headers=SERVICE_HEADERS)
        assert response.status_code == 404


def test_published_export_health() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/read/v1/published/health", headers=SERVICE_HEADERS)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "module": "published_export",
        "surface": "service_read_v1",
    }


def test_published_promotions_and_coupons_export_match_runtime_contract_shape() -> None:
    values = _seed_promotion_coupon_export_data()
    client = TestClient(app)

    promotions_response = client.get(
        "/backoffice/read/v1/published/promotions",
        params={"publish_version": values["publish_version"]},
        headers=SERVICE_HEADERS,
    )
    coupons_response = client.get(
        "/backoffice/read/v1/published/coupons",
        params={"publish_version": values["publish_version"]},
        headers=SERVICE_HEADERS,
    )

    assert promotions_response.status_code == 200
    assert coupons_response.status_code == 200

    promotion_by_code = {
        promotion["promotion_code"]: promotion
        for promotion in promotions_response.json()["promotions"]
    }
    promotion = promotion_by_code[values["promotion_code"]]
    assert promotion["promotion_name"] == "测试促销"
    assert promotion["discount_type"] == "percentage"
    assert promotion["discount_value"] == 10
    assert promotion["is_active"] is True

    coupon_by_code = {
        coupon["coupon_code"]: coupon for coupon in coupons_response.json()["coupons"]
    }
    coupon = coupon_by_code[values["coupon_code"]]
    assert coupon["coupon_name"] == "测试优惠券"
    assert coupon["promotion_code"] == values["promotion_code"]
    assert coupon["coupon_type"] == "public_code"
    assert coupon["is_active"] is True
