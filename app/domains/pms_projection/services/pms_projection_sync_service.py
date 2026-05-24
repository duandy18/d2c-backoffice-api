"""Synchronize PMS projection feeds into D2C backoffice projection tables."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Protocol

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.barcodes import PmsBarcodeProjection
from app.domains.pms_projection.models.brand_assets import PmsBrandAssetProjection
from app.domains.pms_projection.models.brand_profiles import PmsBrandProfileProjection
from app.domains.pms_projection.models.category_bindings import (
    PmsItemDisplayCategoryBindingProjection,
)
from app.domains.pms_projection.models.display_categories import PmsDisplayCategoryProjection
from app.domains.pms_projection.models.item_assets import PmsItemAssetProjection
from app.domains.pms_projection.models.item_contents import PmsItemContentProjection
from app.domains.pms_projection.models.products import PmsProductProjection
from app.domains.pms_projection.models.sku_codes import PmsSkuCodeProjection
from app.domains.pms_projection.models.sync_runs import PmsProjectionSyncRun
from app.domains.pms_projection.models.units import PmsUnitProjection

PMS_PROJECTION_SYNC_SCOPES = (
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
)


class PmsProjectionFeedReader(Protocol):
    base_url: str

    def fetch_all(self, scope: str) -> tuple[str, list[dict[str, Any]]]: ...


@dataclass(frozen=True)
class PmsProjectionSyncScopeResult:
    scope: str
    endpoint: str | None
    status: str
    rows_fetched: int
    rows_upserted: int
    error_code: str | None = None
    error_message: str | None = None


@dataclass(frozen=True)
class PmsProjectionSyncResult:
    status: str
    scopes: list[PmsProjectionSyncScopeResult]


def _parse_datetime(value: object) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        normalized = value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    return None


def _decimal(value: object) -> Decimal:
    return Decimal(str(value))


def _raw_payload(row: dict[str, Any]) -> dict[str, Any]:
    return dict(row)


def _source_base_url(client: PmsProjectionFeedReader) -> str | None:
    raw = getattr(client, "base_url", None)
    return str(raw).rstrip("/") if raw is not None else None


def _product_values(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "pms_item_id": int(row["item_id"]),
        "pms_sku": str(row["sku"]),
        "item_name": str(row["name"]),
        "item_spec": row.get("spec"),
        "enabled": bool(row["enabled"]),
        "supplier_id": row.get("supplier_id"),
        "brand_id": row.get("brand_id"),
        "brand_code": row.get("brand_code"),
        "brand_name": row.get("brand_name") or row.get("brand"),
        "category_id": row.get("category_id"),
        "category_code": row.get("category_code"),
        "category_name": row.get("category_name") or row.get("category"),
        "category_path_code": row.get("category_path_code"),
        "category_level": row.get("category_level"),
        "category_is_leaf": row.get("category_is_leaf"),
        "pms_updated_at": _parse_datetime(row.get("pms_updated_at")),
        "synced_at": datetime.now(UTC),
        "raw_payload": _raw_payload(row),
    }


def _unit_values(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "pms_item_uom_id": int(row["item_uom_id"]),
        "pms_item_id": int(row["item_id"]),
        "uom": str(row["uom"]),
        "uom_name": str(row.get("uom_name") or row.get("display_name") or row["uom"]),
        "display_name": row.get("display_name"),
        "ratio_to_base": _decimal(row["ratio_to_base"]),
        "net_weight_kg": (
            _decimal(row["net_weight_kg"]) if row.get("net_weight_kg") is not None else None
        ),
        "is_base": bool(row["is_base"]),
        "is_purchase_default": bool(row["is_purchase_default"]),
        "is_inbound_default": bool(row["is_inbound_default"]),
        "is_outbound_default": bool(row["is_outbound_default"]),
        "pms_updated_at": _parse_datetime(row.get("pms_updated_at")),
        "synced_at": datetime.now(UTC),
        "raw_payload": _raw_payload(row),
    }


def _product_identity_by_item_id(session: Session, pms_item_id: int) -> tuple[str, str]:
    product = (
        session.query(PmsProductProjection)
        .filter(PmsProductProjection.pms_item_id == int(pms_item_id))
        .one_or_none()
    )
    if product is None:
        raise RuntimeError(f"missing product projection for PMS item {pms_item_id}")
    return product.pms_sku, product.item_name


def _unit_identity_by_uom_id(session: Session, pms_item_uom_id: int) -> tuple[str, str, Decimal]:
    unit = (
        session.query(PmsUnitProjection)
        .filter(PmsUnitProjection.pms_item_uom_id == int(pms_item_uom_id))
        .one_or_none()
    )
    if unit is None:
        raise RuntimeError(f"missing unit projection for PMS item_uom {pms_item_uom_id}")
    return unit.uom, unit.uom_name, unit.ratio_to_base


def _sku_code_values(session: Session, row: dict[str, Any]) -> dict[str, Any]:
    pms_item_id = int(row["item_id"])
    item_sku, item_name = _product_identity_by_item_id(session, pms_item_id)
    return {
        "pms_sku_code_id": int(row["sku_code_id"]),
        "pms_item_id": pms_item_id,
        "sku_code": str(row["sku_code"]),
        "code_type": str(row["code_type"]),
        "is_primary": bool(row["is_primary"]),
        "is_active": bool(row["is_active"]),
        "effective_from": _parse_datetime(row.get("effective_from")),
        "effective_to": _parse_datetime(row.get("effective_to")),
        "remark": row.get("remark"),
        "item_sku": item_sku,
        "item_name": item_name,
        "item_enabled": bool(row.get("item_enabled", True)),
        "pms_updated_at": _parse_datetime(row.get("pms_updated_at")),
        "synced_at": datetime.now(UTC),
        "raw_payload": _raw_payload(row),
    }


def _barcode_values(session: Session, row: dict[str, Any]) -> dict[str, Any]:
    pms_item_uom_id = int(row["item_uom_id"])
    uom, uom_name, ratio_to_base = _unit_identity_by_uom_id(session, pms_item_uom_id)
    return {
        "pms_barcode_id": int(row["barcode_id"]),
        "pms_item_id": int(row["item_id"]),
        "pms_item_uom_id": pms_item_uom_id,
        "barcode": str(row["barcode"]),
        "symbology": row.get("symbology"),
        "active": bool(row["active"]),
        "is_primary": bool(row["is_primary"]),
        "uom": uom,
        "uom_name": uom_name,
        "ratio_to_base": ratio_to_base,
        "pms_updated_at": _parse_datetime(row.get("pms_updated_at")),
        "synced_at": datetime.now(UTC),
        "raw_payload": _raw_payload(row),
    }


def _item_content_values(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "pms_content_id": int(row["content_id"]),
        "pms_item_id": int(row["item_id"]),
        "item_sku": row.get("item_sku"),
        "item_name": row.get("item_name"),
        "base_title": row.get("base_title"),
        "base_description": row.get("base_description"),
        "short_description": row.get("short_description"),
        "spec_params": row.get("spec_params"),
        "material_text": row.get("material_text"),
        "ingredients_text": row.get("ingredients_text"),
        "dimensions_text": row.get("dimensions_text"),
        "weight_text": row.get("weight_text"),
        "safety_instructions": row.get("safety_instructions"),
        "usage_instructions": row.get("usage_instructions"),
        "storage_instructions": row.get("storage_instructions"),
        "status": str(row["status"]),
        "pms_updated_at": _parse_datetime(row.get("pms_updated_at")),
        "synced_at": datetime.now(UTC),
        "raw_payload": _raw_payload(row),
    }


def _item_asset_values(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "pms_asset_id": int(row["asset_id"]),
        "pms_item_id": int(row["item_id"]),
        "item_sku": row.get("item_sku"),
        "item_name": row.get("item_name"),
        "asset_type": str(row["asset_type"]),
        "usage_type": str(row["usage_type"]),
        "source_type": str(row["source_type"]),
        "object_key": row.get("object_key"),
        "url": row.get("url"),
        "alt_text": row.get("alt_text"),
        "sort_order": int(row["sort_order"]),
        "is_primary": bool(row["is_primary"]),
        "status": str(row["status"]),
        "raw_meta": row.get("raw_meta"),
        "pms_updated_at": _parse_datetime(row.get("pms_updated_at")),
        "synced_at": datetime.now(UTC),
        "raw_payload": _raw_payload(row),
    }


def _display_category_values(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "pms_display_category_id": int(row["display_category_id"]),
        "parent_id": int(row["parent_id"]) if row.get("parent_id") is not None else None,
        "level": int(row["level"]),
        "category_code": str(row["category_code"]),
        "category_name": str(row["category_name"]),
        "display_name": row.get("display_name"),
        "path_code": str(row["path_code"]),
        "description": row.get("description"),
        "image_url": row.get("image_url"),
        "sort_order": int(row["sort_order"]),
        "is_active": bool(row["is_active"]),
        "is_leaf": bool(row["is_leaf"]),
        "pms_updated_at": _parse_datetime(row.get("pms_updated_at")),
        "synced_at": datetime.now(UTC),
        "raw_payload": _raw_payload(row),
    }


def _item_display_category_binding_values(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "pms_binding_id": int(row["binding_id"]),
        "pms_item_id": int(row["item_id"]),
        "pms_display_category_id": int(row["display_category_id"]),
        "item_sku": row.get("item_sku"),
        "item_name": row.get("item_name"),
        "display_category_code": row.get("display_category_code"),
        "display_category_name": row.get("display_category_name"),
        "display_category_path_code": row.get("display_category_path_code"),
        "is_primary": bool(row["is_primary"]),
        "sort_order": int(row["sort_order"]),
        "pms_updated_at": _parse_datetime(row.get("pms_updated_at")),
        "synced_at": datetime.now(UTC),
        "raw_payload": _raw_payload(row),
    }


def _brand_profile_values(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "pms_profile_id": int(row["profile_id"]),
        "brand_id": int(row["brand_id"]),
        "brand_code": row.get("brand_code"),
        "brand_name": row.get("brand_name"),
        "display_name": row.get("display_name"),
        "official_name": row.get("official_name"),
        "brand_story": row.get("brand_story"),
        "country_or_region": row.get("country_or_region"),
        "website_url": row.get("website_url"),
        "seo_title": row.get("seo_title"),
        "seo_description": row.get("seo_description"),
        "status": str(row["status"]),
        "pms_updated_at": _parse_datetime(row.get("pms_updated_at")),
        "synced_at": datetime.now(UTC),
        "raw_payload": _raw_payload(row),
    }


def _brand_asset_values(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "pms_asset_id": int(row["asset_id"]),
        "brand_id": int(row["brand_id"]),
        "brand_code": row.get("brand_code"),
        "brand_name": row.get("brand_name"),
        "asset_type": str(row["asset_type"]),
        "usage_type": str(row["usage_type"]),
        "object_key": row.get("object_key"),
        "url": row.get("url"),
        "alt_text": row.get("alt_text"),
        "sort_order": int(row["sort_order"]),
        "is_primary": bool(row["is_primary"]),
        "status": str(row["status"]),
        "raw_meta": row.get("raw_meta"),
        "pms_updated_at": _parse_datetime(row.get("pms_updated_at")),
        "synced_at": datetime.now(UTC),
        "raw_payload": _raw_payload(row),
    }


class PmsProjectionSyncService:
    def __init__(
        self,
        *,
        session: Session,
        feed_reader: PmsProjectionFeedReader,
    ) -> None:
        self.session = session
        self.feed_reader = feed_reader

    def sync_all(self, *, requested_by: str | None = None) -> PmsProjectionSyncResult:
        results = [
            self.sync_scope(scope, requested_by=requested_by)
            for scope in PMS_PROJECTION_SYNC_SCOPES
        ]
        status = "success" if all(result.status == "success" for result in results) else "failed"
        return PmsProjectionSyncResult(status=status, scopes=results)

    def sync_scope(
        self,
        scope: str,
        *,
        requested_by: str | None = None,
    ) -> PmsProjectionSyncScopeResult:
        if scope not in PMS_PROJECTION_SYNC_SCOPES:
            raise ValueError(f"unsupported PMS projection sync scope: {scope}")

        endpoint: str | None = None
        source_base_url = _source_base_url(self.feed_reader)

        try:
            endpoint, rows = self.feed_reader.fetch_all(scope)
            rows_upserted = self._upsert_scope(scope, rows)

            run = PmsProjectionSyncRun(
                sync_scope=scope,
                source_service="pms-api",
                source_base_url=source_base_url,
                source_endpoint=endpoint,
                status="success",
                requested_by=requested_by,
                rows_fetched=len(rows),
                rows_upserted=rows_upserted,
                rows_deleted=0,
                raw_summary={"scope": scope, "rows_fetched": len(rows)},
                finished_at=datetime.now(UTC),
            )
            self.session.add(run)
            self.session.commit()

            return PmsProjectionSyncScopeResult(
                scope=scope,
                endpoint=endpoint,
                status="success",
                rows_fetched=len(rows),
                rows_upserted=rows_upserted,
            )
        except Exception as exc:
            self.session.rollback()
            run = PmsProjectionSyncRun(
                sync_scope=scope,
                source_service="pms-api",
                source_base_url=source_base_url,
                source_endpoint=endpoint,
                status="failed",
                requested_by=requested_by,
                rows_fetched=0,
                rows_upserted=0,
                rows_deleted=0,
                error_code=type(exc).__name__,
                error_message=str(exc),
                raw_summary={"scope": scope},
                finished_at=datetime.now(UTC),
            )
            self.session.add(run)
            self.session.commit()

            return PmsProjectionSyncScopeResult(
                scope=scope,
                endpoint=endpoint,
                status="failed",
                rows_fetched=0,
                rows_upserted=0,
                error_code=type(exc).__name__,
                error_message=str(exc),
            )

    def _upsert_scope(self, scope: str, rows: list[dict[str, Any]]) -> int:
        if not rows:
            return 0

        if scope == "products":
            return self._upsert_products(rows)
        if scope == "units":
            return self._upsert_units(rows)
        if scope == "sku_codes":
            return self._upsert_sku_codes(rows)
        if scope == "barcodes":
            return self._upsert_barcodes(rows)
        if scope == "item_contents":
            return self._upsert_item_contents(rows)
        if scope == "item_assets":
            return self._upsert_item_assets(rows)
        if scope == "display_categories":
            return self._upsert_display_categories(rows)
        if scope == "item_display_category_bindings":
            return self._upsert_item_display_category_bindings(rows)
        if scope == "brand_profiles":
            return self._upsert_brand_profiles(rows)
        if scope == "brand_assets":
            return self._upsert_brand_assets(rows)

        raise ValueError(f"unsupported PMS projection sync scope: {scope}")

    def _upsert_products(self, rows: list[dict[str, Any]]) -> int:
        values = [_product_values(row) for row in rows]
        statement = insert(PmsProductProjection).values(values)
        excluded = statement.excluded
        update_values = {
            "pms_sku": excluded.pms_sku,
            "item_name": excluded.item_name,
            "item_spec": excluded.item_spec,
            "enabled": excluded.enabled,
            "supplier_id": excluded.supplier_id,
            "brand_id": excluded.brand_id,
            "brand_code": excluded.brand_code,
            "brand_name": excluded.brand_name,
            "category_id": excluded.category_id,
            "category_code": excluded.category_code,
            "category_name": excluded.category_name,
            "category_path_code": excluded.category_path_code,
            "category_level": excluded.category_level,
            "category_is_leaf": excluded.category_is_leaf,
            "pms_updated_at": excluded.pms_updated_at,
            "synced_at": excluded.synced_at,
            "raw_payload": excluded.raw_payload,
        }
        self.session.execute(
            statement.on_conflict_do_update(
                index_elements=[PmsProductProjection.pms_item_id],
                set_=update_values,
            )
        )
        return len(values)

    def _upsert_units(self, rows: list[dict[str, Any]]) -> int:
        values = [_unit_values(row) for row in rows]
        statement = insert(PmsUnitProjection).values(values)
        excluded = statement.excluded
        update_values = {
            "pms_item_id": excluded.pms_item_id,
            "uom": excluded.uom,
            "uom_name": excluded.uom_name,
            "display_name": excluded.display_name,
            "ratio_to_base": excluded.ratio_to_base,
            "net_weight_kg": excluded.net_weight_kg,
            "is_base": excluded.is_base,
            "is_purchase_default": excluded.is_purchase_default,
            "is_inbound_default": excluded.is_inbound_default,
            "is_outbound_default": excluded.is_outbound_default,
            "pms_updated_at": excluded.pms_updated_at,
            "synced_at": excluded.synced_at,
            "raw_payload": excluded.raw_payload,
        }
        self.session.execute(
            statement.on_conflict_do_update(
                index_elements=[PmsUnitProjection.pms_item_uom_id],
                set_=update_values,
            )
        )
        return len(values)

    def _upsert_sku_codes(self, rows: list[dict[str, Any]]) -> int:
        values = [_sku_code_values(self.session, row) for row in rows]
        statement = insert(PmsSkuCodeProjection).values(values)
        excluded = statement.excluded
        update_values = {
            "pms_item_id": excluded.pms_item_id,
            "sku_code": excluded.sku_code,
            "code_type": excluded.code_type,
            "is_primary": excluded.is_primary,
            "is_active": excluded.is_active,
            "effective_from": excluded.effective_from,
            "effective_to": excluded.effective_to,
            "remark": excluded.remark,
            "item_sku": excluded.item_sku,
            "item_name": excluded.item_name,
            "item_enabled": excluded.item_enabled,
            "pms_updated_at": excluded.pms_updated_at,
            "synced_at": excluded.synced_at,
            "raw_payload": excluded.raw_payload,
        }
        self.session.execute(
            statement.on_conflict_do_update(
                index_elements=[PmsSkuCodeProjection.pms_sku_code_id],
                set_=update_values,
            )
        )
        return len(values)

    def _upsert_barcodes(self, rows: list[dict[str, Any]]) -> int:
        values = [_barcode_values(self.session, row) for row in rows]
        statement = insert(PmsBarcodeProjection).values(values)
        excluded = statement.excluded
        update_values = {
            "pms_item_id": excluded.pms_item_id,
            "pms_item_uom_id": excluded.pms_item_uom_id,
            "barcode": excluded.barcode,
            "symbology": excluded.symbology,
            "active": excluded.active,
            "is_primary": excluded.is_primary,
            "uom": excluded.uom,
            "uom_name": excluded.uom_name,
            "ratio_to_base": excluded.ratio_to_base,
            "pms_updated_at": excluded.pms_updated_at,
            "synced_at": excluded.synced_at,
            "raw_payload": excluded.raw_payload,
        }
        self.session.execute(
            statement.on_conflict_do_update(
                index_elements=[PmsBarcodeProjection.pms_barcode_id],
                set_=update_values,
            )
        )
        return len(values)

    def _upsert_item_contents(self, rows: list[dict[str, Any]]) -> int:
        values = [_item_content_values(row) for row in rows]
        statement = insert(PmsItemContentProjection).values(values)
        excluded = statement.excluded
        update_values = {
            "pms_item_id": excluded.pms_item_id,
            "item_sku": excluded.item_sku,
            "item_name": excluded.item_name,
            "base_title": excluded.base_title,
            "base_description": excluded.base_description,
            "short_description": excluded.short_description,
            "spec_params": excluded.spec_params,
            "material_text": excluded.material_text,
            "ingredients_text": excluded.ingredients_text,
            "dimensions_text": excluded.dimensions_text,
            "weight_text": excluded.weight_text,
            "safety_instructions": excluded.safety_instructions,
            "usage_instructions": excluded.usage_instructions,
            "storage_instructions": excluded.storage_instructions,
            "status": excluded.status,
            "pms_updated_at": excluded.pms_updated_at,
            "synced_at": excluded.synced_at,
            "raw_payload": excluded.raw_payload,
        }
        self.session.execute(
            statement.on_conflict_do_update(
                index_elements=[PmsItemContentProjection.pms_content_id],
                set_=update_values,
            )
        )
        return len(values)

    def _upsert_item_assets(self, rows: list[dict[str, Any]]) -> int:
        values = [_item_asset_values(row) for row in rows]
        statement = insert(PmsItemAssetProjection).values(values)
        excluded = statement.excluded
        update_values = {
            "pms_item_id": excluded.pms_item_id,
            "item_sku": excluded.item_sku,
            "item_name": excluded.item_name,
            "asset_type": excluded.asset_type,
            "usage_type": excluded.usage_type,
            "source_type": excluded.source_type,
            "object_key": excluded.object_key,
            "url": excluded.url,
            "alt_text": excluded.alt_text,
            "sort_order": excluded.sort_order,
            "is_primary": excluded.is_primary,
            "status": excluded.status,
            "raw_meta": excluded.raw_meta,
            "pms_updated_at": excluded.pms_updated_at,
            "synced_at": excluded.synced_at,
            "raw_payload": excluded.raw_payload,
        }
        self.session.execute(
            statement.on_conflict_do_update(
                index_elements=[PmsItemAssetProjection.pms_asset_id],
                set_=update_values,
            )
        )
        return len(values)

    def _upsert_display_categories(self, rows: list[dict[str, Any]]) -> int:
        values = [_display_category_values(row) for row in rows]
        statement = insert(PmsDisplayCategoryProjection).values(values)
        excluded = statement.excluded
        update_values = {
            "parent_id": excluded.parent_id,
            "level": excluded.level,
            "category_code": excluded.category_code,
            "category_name": excluded.category_name,
            "display_name": excluded.display_name,
            "path_code": excluded.path_code,
            "description": excluded.description,
            "image_url": excluded.image_url,
            "sort_order": excluded.sort_order,
            "is_active": excluded.is_active,
            "is_leaf": excluded.is_leaf,
            "pms_updated_at": excluded.pms_updated_at,
            "synced_at": excluded.synced_at,
            "raw_payload": excluded.raw_payload,
        }
        self.session.execute(
            statement.on_conflict_do_update(
                index_elements=[PmsDisplayCategoryProjection.pms_display_category_id],
                set_=update_values,
            )
        )
        return len(values)

    def _upsert_item_display_category_bindings(self, rows: list[dict[str, Any]]) -> int:
        values = [_item_display_category_binding_values(row) for row in rows]
        statement = insert(PmsItemDisplayCategoryBindingProjection).values(values)
        excluded = statement.excluded
        update_values = {
            "pms_item_id": excluded.pms_item_id,
            "pms_display_category_id": excluded.pms_display_category_id,
            "item_sku": excluded.item_sku,
            "item_name": excluded.item_name,
            "display_category_code": excluded.display_category_code,
            "display_category_name": excluded.display_category_name,
            "display_category_path_code": excluded.display_category_path_code,
            "is_primary": excluded.is_primary,
            "sort_order": excluded.sort_order,
            "pms_updated_at": excluded.pms_updated_at,
            "synced_at": excluded.synced_at,
            "raw_payload": excluded.raw_payload,
        }
        self.session.execute(
            statement.on_conflict_do_update(
                index_elements=[PmsItemDisplayCategoryBindingProjection.pms_binding_id],
                set_=update_values,
            )
        )
        return len(values)

    def _upsert_brand_profiles(self, rows: list[dict[str, Any]]) -> int:
        values = [_brand_profile_values(row) for row in rows]
        statement = insert(PmsBrandProfileProjection).values(values)
        excluded = statement.excluded
        update_values = {
            "brand_id": excluded.brand_id,
            "brand_code": excluded.brand_code,
            "brand_name": excluded.brand_name,
            "display_name": excluded.display_name,
            "official_name": excluded.official_name,
            "brand_story": excluded.brand_story,
            "country_or_region": excluded.country_or_region,
            "website_url": excluded.website_url,
            "seo_title": excluded.seo_title,
            "seo_description": excluded.seo_description,
            "status": excluded.status,
            "pms_updated_at": excluded.pms_updated_at,
            "synced_at": excluded.synced_at,
            "raw_payload": excluded.raw_payload,
        }
        self.session.execute(
            statement.on_conflict_do_update(
                index_elements=[PmsBrandProfileProjection.pms_profile_id],
                set_=update_values,
            )
        )
        return len(values)

    def _upsert_brand_assets(self, rows: list[dict[str, Any]]) -> int:
        values = [_brand_asset_values(row) for row in rows]
        statement = insert(PmsBrandAssetProjection).values(values)
        excluded = statement.excluded
        update_values = {
            "brand_id": excluded.brand_id,
            "brand_code": excluded.brand_code,
            "brand_name": excluded.brand_name,
            "asset_type": excluded.asset_type,
            "usage_type": excluded.usage_type,
            "object_key": excluded.object_key,
            "url": excluded.url,
            "alt_text": excluded.alt_text,
            "sort_order": excluded.sort_order,
            "is_primary": excluded.is_primary,
            "status": excluded.status,
            "raw_meta": excluded.raw_meta,
            "pms_updated_at": excluded.pms_updated_at,
            "synced_at": excluded.synced_at,
            "raw_payload": excluded.raw_payload,
        }
        self.session.execute(
            statement.on_conflict_do_update(
                index_elements=[PmsBrandAssetProjection.pms_asset_id],
                set_=update_values,
            )
        )
        return len(values)


__all__ = [
    "PMS_PROJECTION_SYNC_SCOPES",
    "PmsProjectionSyncResult",
    "PmsProjectionSyncScopeResult",
    "PmsProjectionSyncService",
]
