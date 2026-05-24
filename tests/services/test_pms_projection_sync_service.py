from __future__ import annotations

from typing import Any
from uuid import uuid4

from sqlalchemy import text

from app.core.config import load_settings
from app.core.database import get_session_factory
from app.domains.pms_projection.services.pms_projection_sync_service import (
    PmsProjectionSyncService,
)


class FakePmsProjectionFeedReader:
    base_url = "http://pms-api.test"

    def __init__(self, rows_by_scope: dict[str, list[dict[str, Any]]]) -> None:
        self.rows_by_scope = rows_by_scope
        self.calls: list[str] = []

    def fetch_all(self, scope: str) -> tuple[str, list[dict[str, Any]]]:
        self.calls.append(scope)
        endpoint_scope = scope.replace("_", "-")
        return (
            f"/pms/read/v1/projection-feed/{endpoint_scope}",
            list(self.rows_by_scope[scope]),
        )


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12].upper()}"


def _clear_projection_tables() -> None:
    settings = load_settings()
    session_factory = get_session_factory(settings.test_database_url)
    with session_factory() as session:
        # Listing/pricing tables hold RESTRICT FKs to PMS projection rows.
        # Clear merchant-owned dependent rows first, then clear projection rows.
        session.execute(text("DELETE FROM d2c_price_configs"))
        session.execute(text("DELETE FROM d2c_storefront_category_bindings"))
        session.execute(text("DELETE FROM d2c_storefront_categories"))
        session.execute(text("DELETE FROM d2c_sku_listing_configs"))
        session.execute(text("DELETE FROM d2c_product_listing_media"))
        session.execute(text("DELETE FROM d2c_product_listing_contents"))
        session.execute(text("DELETE FROM d2c_product_listing_configs"))

        session.execute(text("DELETE FROM d2c_pms_projection_sync_runs"))
        session.execute(text("DELETE FROM d2c_pms_brand_asset_projection"))
        session.execute(text("DELETE FROM d2c_pms_brand_profile_projection"))
        session.execute(text("DELETE FROM d2c_pms_item_display_category_binding_projection"))
        session.execute(text("DELETE FROM d2c_pms_display_category_projection"))
        session.execute(text("DELETE FROM d2c_pms_item_asset_projection"))
        session.execute(text("DELETE FROM d2c_pms_item_content_projection"))
        session.execute(text("DELETE FROM d2c_pms_barcode_projection"))
        session.execute(text("DELETE FROM d2c_pms_sku_code_projection"))
        session.execute(text("DELETE FROM d2c_pms_unit_projection"))
        session.execute(text("DELETE FROM d2c_pms_product_projection"))
        session.commit()


def _rows() -> dict[str, list[dict[str, Any]]]:
    pms_item_id = int(uuid4().int % 1_000_000_000)
    pms_item_uom_id = int(uuid4().int % 1_000_000_000)
    pms_sku_code_id = int(uuid4().int % 1_000_000_000)
    pms_barcode_id = int(uuid4().int % 1_000_000_000)
    pms_content_id = int(uuid4().int % 1_000_000_000)
    pms_item_asset_id = int(uuid4().int % 1_000_000_000)
    pms_display_category_id = int(uuid4().int % 1_000_000_000)
    pms_binding_id = int(uuid4().int % 1_000_000_000)
    pms_brand_profile_id = int(uuid4().int % 1_000_000_000)
    pms_brand_asset_id = int(uuid4().int % 1_000_000_000)
    brand_id = int(uuid4().int % 1_000_000_000)
    sku = _unique("PMS-SKU")
    sku_code = _unique("SKU-CODE")
    barcode = _unique("690")

    return {
        "products": [
            {
                "item_id": pms_item_id,
                "sku": sku,
                "name": "PMS 商品",
                "spec": "1kg",
                "enabled": True,
                "supplier_id": None,
                "brand_id": brand_id,
                "brand": "测试品牌",
                "category": "测试类目",
                "expiry_policy": "NONE",
                "shelf_life_value": None,
                "shelf_life_unit": None,
                "lot_source_policy": "INTERNAL_ONLY",
                "derivation_allowed": True,
                "uom_governance_enabled": True,
                "pms_updated_at": "2026-05-24T00:00:00+00:00",
            }
        ],
        "units": [
            {
                "item_uom_id": pms_item_uom_id,
                "item_id": pms_item_id,
                "uom": "bag",
                "display_name": "袋",
                "uom_name": "袋",
                "ratio_to_base": "1",
                "net_weight_kg": "1.000",
                "is_base": True,
                "is_purchase_default": False,
                "is_inbound_default": False,
                "is_outbound_default": True,
                "pms_updated_at": "2026-05-24T00:00:00+00:00",
            }
        ],
        "sku_codes": [
            {
                "sku_code_id": pms_sku_code_id,
                "item_id": pms_item_id,
                "sku_code": sku_code,
                "code_type": "PRIMARY",
                "is_primary": True,
                "is_active": True,
                "effective_from": None,
                "effective_to": None,
                "pms_updated_at": "2026-05-24T00:00:00+00:00",
            }
        ],
        "barcodes": [
            {
                "barcode_id": pms_barcode_id,
                "item_id": pms_item_id,
                "item_uom_id": pms_item_uom_id,
                "barcode": barcode,
                "symbology": "EAN13",
                "active": True,
                "is_primary": True,
                "pms_updated_at": "2026-05-24T00:00:00+00:00",
            }
        ],
        "item_contents": [
            {
                "content_id": pms_content_id,
                "item_id": pms_item_id,
                "base_title": "标准展示标题",
                "base_description": "标准展示说明",
                "short_description": "短说明",
                "spec_params": {"size": "S"},
                "material_text": "材质",
                "ingredients_text": None,
                "dimensions_text": None,
                "weight_text": None,
                "safety_instructions": None,
                "usage_instructions": None,
                "storage_instructions": None,
                "status": "active",
                "pms_updated_at": "2026-05-24T00:00:00+00:00",
            }
        ],
        "item_assets": [
            {
                "asset_id": pms_item_asset_id,
                "item_id": pms_item_id,
                "asset_type": "image",
                "usage_type": "main",
                "source_type": "external",
                "object_key": None,
                "url": "https://example.test/item.png",
                "alt_text": "商品图",
                "sort_order": 10,
                "is_primary": True,
                "status": "active",
                "raw_meta": {"width": 800},
                "pms_updated_at": "2026-05-24T00:00:00+00:00",
            }
        ],
        "display_categories": [
            {
                "display_category_id": pms_display_category_id,
                "parent_id": None,
                "level": 1,
                "category_code": "CAT",
                "category_name": "猫用品",
                "display_name": "猫用品",
                "path_code": "CAT",
                "description": "展示类目",
                "image_url": None,
                "sort_order": 10,
                "is_active": True,
                "is_leaf": True,
                "pms_updated_at": "2026-05-24T00:00:00+00:00",
            }
        ],
        "item_display_category_bindings": [
            {
                "binding_id": pms_binding_id,
                "item_id": pms_item_id,
                "display_category_id": pms_display_category_id,
                "is_primary": True,
                "sort_order": 10,
                "pms_updated_at": "2026-05-24T00:00:00+00:00",
            }
        ],
        "brand_profiles": [
            {
                "profile_id": pms_brand_profile_id,
                "brand_id": brand_id,
                "display_name": "品牌展示名",
                "official_name": "官方品牌名",
                "brand_story": "品牌故事",
                "country_or_region": "CN",
                "website_url": "https://example.test",
                "seo_title": "品牌 SEO",
                "seo_description": "品牌 SEO 描述",
                "status": "active",
                "pms_updated_at": "2026-05-24T00:00:00+00:00",
            }
        ],
        "brand_assets": [
            {
                "asset_id": pms_brand_asset_id,
                "brand_id": brand_id,
                "asset_type": "image",
                "usage_type": "logo",
                "object_key": None,
                "url": "https://example.test/logo.png",
                "alt_text": "logo",
                "sort_order": 10,
                "is_primary": True,
                "status": "active",
                "raw_meta": None,
                "pms_updated_at": "2026-05-24T00:00:00+00:00",
            }
        ],
    }


def test_pms_projection_sync_all_upserts_projection_rows_and_logs_runs() -> None:
    _clear_projection_tables()
    settings = load_settings()
    session_factory = get_session_factory(settings.test_database_url)
    reader = FakePmsProjectionFeedReader(_rows())

    with session_factory() as session:
        result = PmsProjectionSyncService(session=session, feed_reader=reader).sync_all(
            requested_by="pytest"
        )

    assert result.status == "success"
    assert [scope.scope for scope in result.scopes] == [
        "products",
        "units",
        "sku_codes",
        "barcodes",
        "item_contents",
        "item_assets",
        "display_categories",
        "item_display_category_bindings",
        "brand_profiles",
        "brand_assets",
    ]
    assert reader.calls == [
        "products",
        "units",
        "sku_codes",
        "barcodes",
        "item_contents",
        "item_assets",
        "display_categories",
        "item_display_category_bindings",
        "brand_profiles",
        "brand_assets",
    ]

    with session_factory() as session:
        counts = dict(
            session.execute(
                text(
                    """
                    SELECT 'products' AS name, COUNT(*)
                    FROM d2c_pms_product_projection
                    UNION ALL SELECT 'units', COUNT(*)
                    FROM d2c_pms_unit_projection
                    UNION ALL SELECT 'sku_codes', COUNT(*)
                    FROM d2c_pms_sku_code_projection
                    UNION ALL SELECT 'barcodes', COUNT(*)
                    FROM d2c_pms_barcode_projection
                    UNION ALL SELECT 'item_contents', COUNT(*)
                    FROM d2c_pms_item_content_projection
                    UNION ALL SELECT 'item_assets', COUNT(*)
                    FROM d2c_pms_item_asset_projection
                    UNION ALL SELECT 'display_categories', COUNT(*)
                    FROM d2c_pms_display_category_projection
                    UNION ALL SELECT 'display_bindings', COUNT(*)
                    FROM d2c_pms_item_display_category_binding_projection
                    UNION ALL SELECT 'brand_profiles', COUNT(*)
                    FROM d2c_pms_brand_profile_projection
                    UNION ALL SELECT 'brand_assets', COUNT(*)
                    FROM d2c_pms_brand_asset_projection
                    UNION ALL SELECT 'runs', COUNT(*)
                    FROM d2c_pms_projection_sync_runs
                    """
                )
            ).all()
        )

        product = (
            session.execute(
                text(
                    """
                    SELECT pms_sku, item_name, brand_name, category_name
                    FROM d2c_pms_product_projection
                    LIMIT 1
                    """
                )
            )
            .mappings()
            .one()
        )
        sku_code = (
            session.execute(
                text(
                    """
                    SELECT sku_code, item_sku, item_name
                    FROM d2c_pms_sku_code_projection
                    LIMIT 1
                    """
                )
            )
            .mappings()
            .one()
        )
        barcode = (
            session.execute(
                text(
                    """
                    SELECT barcode, uom, uom_name, ratio_to_base
                    FROM d2c_pms_barcode_projection
                    LIMIT 1
                    """
                )
            )
            .mappings()
            .one()
        )

    assert counts == {
        "products": 1,
        "units": 1,
        "sku_codes": 1,
        "barcodes": 1,
        "item_contents": 1,
        "item_assets": 1,
        "display_categories": 1,
        "display_bindings": 1,
        "brand_profiles": 1,
        "brand_assets": 1,
        "runs": 10,
    }
    assert product["item_name"] == "PMS 商品"
    assert product["brand_name"] == "测试品牌"
    assert product["category_name"] == "测试类目"
    assert sku_code["item_sku"] == product["pms_sku"]
    assert sku_code["item_name"] == "PMS 商品"
    assert barcode["uom"] == "bag"
    assert barcode["uom_name"] == "袋"

    with session_factory() as session:
        content = (
            session.execute(
                text(
                    """
                    SELECT base_title, spec_params
                    FROM d2c_pms_item_content_projection
                    LIMIT 1
                    """
                )
            )
            .mappings()
            .one()
        )
        item_asset = (
            session.execute(
                text(
                    """
                    SELECT usage_type, url, is_primary
                    FROM d2c_pms_item_asset_projection
                    LIMIT 1
                    """
                )
            )
            .mappings()
            .one()
        )
        display_category = (
            session.execute(
                text(
                    """
                    SELECT category_code, category_name
                    FROM d2c_pms_display_category_projection
                    LIMIT 1
                    """
                )
            )
            .mappings()
            .one()
        )
        brand_profile = (
            session.execute(
                text(
                    """
                    SELECT display_name
                    FROM d2c_pms_brand_profile_projection
                    LIMIT 1
                    """
                )
            )
            .mappings()
            .one()
        )

    assert content["base_title"] == "标准展示标题"
    assert content["spec_params"] == {"size": "S"}
    assert item_asset["usage_type"] == "main"
    assert item_asset["is_primary"] is True
    assert display_category["category_code"] == "CAT"
    assert brand_profile["display_name"] == "品牌展示名"


def test_pms_projection_sync_is_idempotent_on_second_run() -> None:
    _clear_projection_tables()
    settings = load_settings()
    session_factory = get_session_factory(settings.test_database_url)
    rows = _rows()

    with session_factory() as session:
        service = PmsProjectionSyncService(
            session=session,
            feed_reader=FakePmsProjectionFeedReader(rows),
        )
        first = service.sync_all(requested_by="pytest")
        second = service.sync_all(requested_by="pytest")

    assert first.status == "success"
    assert second.status == "success"

    with session_factory() as session:
        counts = dict(
            session.execute(
                text(
                    """
                    SELECT 'products' AS name, COUNT(*)
                    FROM d2c_pms_product_projection
                    UNION ALL SELECT 'units', COUNT(*)
                    FROM d2c_pms_unit_projection
                    UNION ALL SELECT 'sku_codes', COUNT(*)
                    FROM d2c_pms_sku_code_projection
                    UNION ALL SELECT 'barcodes', COUNT(*)
                    FROM d2c_pms_barcode_projection
                    UNION ALL SELECT 'item_contents', COUNT(*)
                    FROM d2c_pms_item_content_projection
                    UNION ALL SELECT 'item_assets', COUNT(*)
                    FROM d2c_pms_item_asset_projection
                    UNION ALL SELECT 'display_categories', COUNT(*)
                    FROM d2c_pms_display_category_projection
                    UNION ALL SELECT 'display_bindings', COUNT(*)
                    FROM d2c_pms_item_display_category_binding_projection
                    UNION ALL SELECT 'brand_profiles', COUNT(*)
                    FROM d2c_pms_brand_profile_projection
                    UNION ALL SELECT 'brand_assets', COUNT(*)
                    FROM d2c_pms_brand_asset_projection
                    UNION ALL SELECT 'runs', COUNT(*)
                    FROM d2c_pms_projection_sync_runs
                    """
                )
            ).all()
        )

    assert counts == {
        "products": 1,
        "units": 1,
        "sku_codes": 1,
        "barcodes": 1,
        "item_contents": 1,
        "item_assets": 1,
        "display_categories": 1,
        "display_bindings": 1,
        "brand_profiles": 1,
        "brand_assets": 1,
        "runs": 20,
    }
