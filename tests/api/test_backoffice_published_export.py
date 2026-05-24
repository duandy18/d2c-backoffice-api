from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import load_settings
from app.core.database import get_session_factory
from app.domains.listing.models.listing import (
    ProductListingConfig,
    SkuListingConfig,
    StorefrontCategory,
    StorefrontCategoryBinding,
)
from app.domains.pms_projection.models.pms_projection import (
    PmsBarcodeProjection,
    PmsProductProjection,
    PmsSkuCodeProjection,
    PmsUnitProjection,
)
from app.domains.pricing.models.price_config import PriceConfig
from app.domains.promotions.models.promotion import Coupon, Promotion
from app.domains.publish.models.publish_version import PublishVersion
from app.main import app

SERVICE_HEADERS = {"X-Service-Client": "d2c-service"}


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12].upper()}"


def _seed_export_data() -> dict[str, str]:
    settings = load_settings()
    session_factory = get_session_factory(settings.test_database_url)
    now = datetime.now(UTC)

    publish_version = _unique("PUB")
    pms_sku = _unique("PMS-SKU")
    listing_code = _unique("LISTING")
    sku_code = _unique("SKU")
    price_config_code = _unique("PRICE")
    promotion_code = _unique("PROMO")
    coupon_code = _unique("COUPON")
    category_code = _unique("CAT")

    pms_item_id = int(uuid4().int % 1_000_000_000)
    pms_item_uom_id = int(uuid4().int % 1_000_000_000)
    pms_sku_code_id = int(uuid4().int % 1_000_000_000)
    pms_barcode_id = int(uuid4().int % 1_000_000_000)

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

        session.add(
            PmsProductProjection(
                pms_item_id=pms_item_id,
                pms_sku=pms_sku,
                item_name="PMS 商品名",
                item_spec="1kg",
                enabled=True,
                supplier_id=None,
                brand_id=None,
                brand_code="brand_test",
                brand_name="测试品牌",
                category_id=None,
                category_code="pms_cat",
                category_name="PMS 类目",
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
                item_sku=pms_sku,
                item_name="PMS 商品名",
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
                barcode=_unique("690"),
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

        product_listing = ProductListingConfig(
            pms_item_id=pms_item_id,
            pms_sku=pms_sku,
            listing_code=listing_code,
            display_name="商城展示商品名",
            subtitle="商城副标题",
            description_override="商城商品描述",
            cover_image_url="https://example.test/product.png",
            listing_status="published",
            display_status="visible",
            sell_status="sellable",
            sort_order=10,
            visible_from=None,
            visible_until=None,
        )
        session.add(product_listing)
        session.flush()

        sku_listing = SkuListingConfig(
            product_listing_config_id=product_listing.id,
            pms_item_id=pms_item_id,
            pms_sku_code_id=pms_sku_code_id,
            pms_item_uom_id=pms_item_uom_id,
            pms_barcode_id=pms_barcode_id,
            sku_display_name="商城展示 SKU",
            sku_spec_text="1kg/袋",
            sku_image_url="https://example.test/sku.png",
            listing_status="published",
            display_status="visible",
            sell_status="sellable",
            sort_order=10,
            visible_from=None,
            visible_until=None,
        )
        session.add(sku_listing)
        session.flush()

        storefront_category = StorefrontCategory(
            category_code=category_code,
            category_name="前台类目",
            parent_category_id=None,
            level=1,
            display_status="visible",
            sort_order=10,
            image_url=None,
            description=None,
        )
        session.add(storefront_category)
        session.flush()

        session.add(
            StorefrontCategoryBinding(
                product_listing_config_id=product_listing.id,
                storefront_category_id=storefront_category.id,
                is_primary=True,
                sort_order=10,
            )
        )

        session.add(
            PriceConfig(
                sku_listing_config_id=sku_listing.id,
                price_config_code=price_config_code,
                channel="storefront",
                currency="USD",
                price_cents=1234,
                compare_at_price_cents=1500,
                effective_from=None,
                effective_until=None,
                is_active=True,
                priority=10,
            )
        )

        promotion = Promotion(
            promotion_code=promotion_code,
            name="测试促销",
            description="pytest promotion",
            promotion_type="store_campaign",
            discount_type="percentage",
            discount_value=10,
            scope_type="all_store",
            min_order_amount_cents=None,
            max_discount_cents=None,
            currency="USD",
            starts_at=None,
            ends_at=None,
            status="active",
            priority=10,
            stackable=False,
            is_active=True,
        )
        session.add(promotion)
        session.flush()

        session.add(
            Coupon(
                coupon_code=coupon_code,
                name="测试优惠券",
                promotion_id=promotion.id,
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
        "listing_code": listing_code,
        "sku_code": sku_code,
        "price_config_code": price_config_code,
        "promotion_code": promotion_code,
        "coupon_code": coupon_code,
        "category_code": category_code,
    }


def test_published_export_requires_service_client() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/read/v1/published/catalog")

    assert response.status_code == 401
    assert response.json() == {"detail": "service_client_required"}


def test_published_export_health() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/read/v1/published/health", headers=SERVICE_HEADERS)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "module": "published_export",
        "surface": "service_read_v1",
    }


def test_published_catalog_export_matches_runtime_contract_shape() -> None:
    values = _seed_export_data()
    client = TestClient(app)

    response = client.get(
        "/backoffice/read/v1/published/catalog",
        params={"publish_version": values["publish_version"]},
        headers=SERVICE_HEADERS,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["publish_version"] == values["publish_version"]
    assert payload["product_count"] >= 1
    assert payload["sku_count"] >= 1

    product_by_code = {product["product_code"]: product for product in payload["products"]}
    product = product_by_code[values["listing_code"]]
    assert product["display_name"] == "商城展示商品名"
    assert product["category_code"] == values["category_code"]
    assert product["brand_code"] == "brand_test"
    assert product["sell_status"] == "sellable"
    assert product["raw_payload"]["source_product_listing_config_id"] is not None

    sku_by_code = {sku["sku_code"]: sku for sku in payload["skus"]}
    sku = sku_by_code[values["sku_code"]]
    assert sku["product_code"] == values["listing_code"]
    assert sku["display_sku_name"] == "商城展示 SKU"
    assert sku["sales_unit_code"] == "bag"
    assert sku["is_sellable"] is True
    assert sku["raw_payload"]["source_sku_listing_config_id"] is not None


def test_published_prices_export_matches_runtime_contract_shape() -> None:
    values = _seed_export_data()
    client = TestClient(app)

    response = client.get(
        "/backoffice/read/v1/published/prices",
        params={"publish_version": values["publish_version"]},
        headers=SERVICE_HEADERS,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["publish_version"] == values["publish_version"]
    assert payload["count"] >= 1

    price_by_code = {price["price_list_code"]: price for price in payload["prices"]}
    price = price_by_code[values["price_config_code"]]
    assert price["sku_code"] == values["sku_code"]
    assert price["channel"] == "storefront"
    assert price["currency"] == "USD"
    assert price["price_cents"] == 1234
    assert price["compare_at_price_cents"] == 1500
    assert price["raw_payload"]["source_price_config_id"] is not None


def test_published_promotions_and_coupons_export_match_runtime_contract_shape() -> None:
    values = _seed_export_data()
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
