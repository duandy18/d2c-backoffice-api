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
    ]
    assert reader.calls == ["products", "units", "sku_codes", "barcodes"]

    with session_factory() as session:
        counts = dict(
            session.execute(
                text(
                    """
                    SELECT 'products' AS name, COUNT(*) FROM d2c_pms_product_projection
                    UNION ALL SELECT 'units', COUNT(*) FROM d2c_pms_unit_projection
                    UNION ALL SELECT 'sku_codes', COUNT(*) FROM d2c_pms_sku_code_projection
                    UNION ALL SELECT 'barcodes', COUNT(*) FROM d2c_pms_barcode_projection
                    UNION ALL SELECT 'runs', COUNT(*) FROM d2c_pms_projection_sync_runs
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
        "runs": 4,
    }
    assert product["item_name"] == "PMS 商品"
    assert product["brand_name"] == "测试品牌"
    assert product["category_name"] == "测试类目"
    assert sku_code["item_sku"] == product["pms_sku"]
    assert sku_code["item_name"] == "PMS 商品"
    assert barcode["uom"] == "bag"
    assert barcode["uom_name"] == "袋"


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
                    SELECT 'products' AS name, COUNT(*) FROM d2c_pms_product_projection
                    UNION ALL SELECT 'units', COUNT(*) FROM d2c_pms_unit_projection
                    UNION ALL SELECT 'sku_codes', COUNT(*) FROM d2c_pms_sku_code_projection
                    UNION ALL SELECT 'barcodes', COUNT(*) FROM d2c_pms_barcode_projection
                    UNION ALL SELECT 'runs', COUNT(*) FROM d2c_pms_projection_sync_runs
                    """
                )
            ).all()
        )

    assert counts == {
        "products": 1,
        "units": 1,
        "sku_codes": 1,
        "barcodes": 1,
        "runs": 8,
    }
