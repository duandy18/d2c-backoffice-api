from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import load_settings
from app.core.database import get_session_factory
from app.domains.listing.models.listing import (
    ProductListingConfig,
    ProductListingContent,
    ProductListingMedia,
    SkuListingConfig,
    StorefrontCategory,
    StorefrontCategoryBinding,
)
from app.domains.pms_projection.models import (
    PmsBarcodeProjection,
    PmsBrandProfileProjection,
    PmsDisplayCategoryProjection,
    PmsItemAssetProjection,
    PmsItemContentProjection,
    PmsItemDisplayCategoryBindingProjection,
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

    fallback_pms_item_id = int(uuid4().int % 1_000_000_000)
    fallback_pms_content_id = int(uuid4().int % 1_000_000_000)
    fallback_pms_asset_id = int(uuid4().int % 1_000_000_000)
    fallback_pms_display_category_id = int(uuid4().int % 1_000_000_000)
    fallback_pms_binding_id = int(uuid4().int % 1_000_000_000)
    fallback_pms_brand_profile_id = int(uuid4().int % 1_000_000_000)
    fallback_brand_id = int(uuid4().int % 1_000_000_000)
    fallback_pms_sku = _unique("PMS-FB")
    fallback_listing_code = _unique("LISTING-FB")
    fallback_display_category_code = _unique("PMS-DISP-CAT")
    fallback_brand_code = _unique("PMS-BRAND")

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
            PmsProductProjection(
                pms_item_id=fallback_pms_item_id,
                pms_sku=fallback_pms_sku,
                item_name="PMS 原始商品名",
                item_spec="500g",
                enabled=True,
                supplier_id=None,
                brand_id=fallback_brand_id,
                brand_code=fallback_brand_code,
                brand_name="PMS 原始品牌名",
                category_id=None,
                category_code="pms_original_cat",
                category_name="PMS 原始类目",
                category_path_code=None,
                category_level=None,
                category_is_leaf=None,
                pms_updated_at=now,
                raw_payload={"source": "pytest-fallback"},
            )
        )
        session.flush()

        session.add(
            PmsItemContentProjection(
                pms_content_id=fallback_pms_content_id,
                pms_item_id=fallback_pms_item_id,
                base_title="PMS 标准商品标题",
                base_description="PMS 标准商品说明",
                short_description="PMS 标准短说明",
                spec_params={"weight": "500g"},
                material_text=None,
                ingredients_text=None,
                dimensions_text=None,
                weight_text=None,
                safety_instructions=None,
                usage_instructions=None,
                storage_instructions=None,
                status="active",
                pms_updated_at=now,
                raw_payload={"source": "pytest-fallback"},
            )
        )
        session.add(
            PmsItemAssetProjection(
                pms_asset_id=fallback_pms_asset_id,
                pms_item_id=fallback_pms_item_id,
                asset_type="image",
                usage_type="main",
                source_type="external",
                object_key=None,
                url="https://example.test/pms-main.png",
                alt_text="PMS 标准主图",
                sort_order=10,
                is_primary=True,
                status="active",
                raw_meta={"source": "pytest"},
                pms_updated_at=now,
                raw_payload={"source": "pytest-fallback"},
            )
        )
        session.add(
            PmsDisplayCategoryProjection(
                pms_display_category_id=fallback_pms_display_category_id,
                parent_id=None,
                level=1,
                category_code=fallback_display_category_code,
                category_name="PMS 标准展示类目",
                display_name="PMS 展示类目名",
                path_code=fallback_display_category_code,
                description="PMS 展示类目说明",
                image_url=None,
                sort_order=10,
                is_active=True,
                is_leaf=True,
                pms_updated_at=now,
                raw_payload={"source": "pytest-fallback"},
            )
        )
        # The binding projection has a real FK to the display category projection.
        # Flush the category row first so the test fixture does not depend on
        # implicit unit-of-work ordering across split ORM modules.
        session.flush()
        session.add(
            PmsItemDisplayCategoryBindingProjection(
                pms_binding_id=fallback_pms_binding_id,
                pms_item_id=fallback_pms_item_id,
                pms_display_category_id=fallback_pms_display_category_id,
                is_primary=True,
                sort_order=10,
                pms_updated_at=now,
                raw_payload={"source": "pytest-fallback"},
            )
        )
        session.add(
            PmsBrandProfileProjection(
                pms_profile_id=fallback_pms_brand_profile_id,
                brand_id=fallback_brand_id,
                display_name="PMS 品牌展示名",
                official_name="PMS 品牌官方名",
                brand_story="PMS 品牌故事",
                country_or_region="CN",
                website_url="https://example.test/brand",
                seo_title="PMS 品牌 SEO",
                seo_description="PMS 品牌 SEO 描述",
                status="active",
                pms_updated_at=now,
                raw_payload={"source": "pytest-fallback"},
            )
        )

        session.add(
            ProductListingConfig(
                pms_item_id=fallback_pms_item_id,
                pms_sku=fallback_pms_sku,
                listing_code=fallback_listing_code,
                listing_status="published",
                display_status="visible",
                sell_status="sellable",
                sort_order=20,
                visible_from=None,
                visible_until=None,
            )
        )

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
            listing_status="published",
            display_status="visible",
            sell_status="sellable",
            sort_order=10,
            visible_from=None,
            visible_until=None,
        )
        session.add(product_listing)
        session.flush()

        session.add(
            ProductListingContent(
                product_listing_config_id=product_listing.id,
                display_title="商城展示商品名",
                subtitle="商城副标题",
                short_description="商城短描述",
                detail_description="商城商品描述",
                seo_title="商城 SEO 标题",
                seo_description="商城 SEO 描述",
                selling_points=["卖点一", "卖点二"],
                content_status="active",
            )
        )
        session.add(
            ProductListingMedia(
                product_listing_config_id=product_listing.id,
                media_type="image",
                source_type="d2c_upload",
                pms_asset_id=None,
                object_key=None,
                url="https://example.test/product.png",
                alt_text="商城展示商品名",
                usage_type="cover",
                sort_order=10,
                is_primary=True,
                status="active",
            )
        )

        sku_listing = SkuListingConfig(
            product_listing_config_id=product_listing.id,
            pms_item_id=pms_item_id,
            pms_sku_code_id=pms_sku_code_id,
            pms_item_uom_id=pms_item_uom_id,
            pms_barcode_id=pms_barcode_id,
            sku_display_name="商城展示 SKU",
            sku_spec_text="1kg/袋",
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
        "fallback_listing_code": fallback_listing_code,
        "fallback_display_category_code": fallback_display_category_code,
        "fallback_brand_code": fallback_brand_code,
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
    assert product["description"] == "商城商品描述"
    assert product["image_url"] == "https://example.test/product.png"
    assert product["category_code"] == values["category_code"]
    assert product["brand_code"] == "brand_test"
    assert product["sell_status"] == "sellable"
    assert product["raw_payload"]["source_product_listing_config_id"] is not None
    assert product["raw_payload"]["source_product_listing_content_id"] is not None
    assert product["raw_payload"]["source_primary_media_id"] is not None

    fallback_product = product_by_code[values["fallback_listing_code"]]
    assert fallback_product["display_name"] == "PMS 标准商品标题"
    assert fallback_product["description"] == "PMS 标准商品说明"
    assert fallback_product["image_url"] == "https://example.test/pms-main.png"
    assert fallback_product["category_code"] == values["fallback_display_category_code"]
    assert fallback_product["category_name"] == "PMS 展示类目名"
    assert fallback_product["brand_code"] == values["fallback_brand_code"]
    assert fallback_product["brand_name"] == "PMS 品牌展示名"
    assert fallback_product["raw_payload"]["source_product_listing_content_id"] is None
    assert fallback_product["raw_payload"]["source_primary_media_id"] is None
    assert fallback_product["raw_payload"]["pms_item_content_id"] is not None
    assert fallback_product["raw_payload"]["pms_item_asset_id"] is not None
    assert fallback_product["raw_payload"]["pms_display_category_id"] is not None
    assert fallback_product["raw_payload"]["pms_brand_profile_id"] is not None

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
