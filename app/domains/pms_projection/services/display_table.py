"""Build PMS-like display table payloads for PMS projection read APIs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel


@dataclass(frozen=True)
class ProjectionDisplayColumnSpec:
    key: str
    label: str
    kind: str = "text"
    candidates: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProjectionDisplayTableSpec:
    resource: str
    projection_table: str
    columns: tuple[ProjectionDisplayColumnSpec, ...]


def col(
    key: str,
    label: str,
    kind: str = "text",
    *candidates: str,
) -> ProjectionDisplayColumnSpec:
    return ProjectionDisplayColumnSpec(
        key=key,
        label=label,
        kind=kind,
        candidates=tuple(candidates or (key,)),
    )


DISPLAY_TABLE_SPECS: dict[str, ProjectionDisplayTableSpec] = {
    "products": ProjectionDisplayTableSpec(
        resource="products",
        projection_table="d2c_pms_product_projection",
        columns=(
            col("item_id", "PMS item_id", "number", "item_id", "pms_item_id"),
            col("sku", "SKU", "text", "sku", "pms_sku"),
            col("name", "商品名称", "text", "name", "item_name"),
            col("spec", "规格", "text", "spec", "item_spec"),
            col("brand", "品牌", "text", "brand", "brand_name", "brand_code"),
            col("category", "分类", "text", "category", "category_name", "category_code"),
            col("lot_source_policy", "批次策略"),
            col("expiry_policy", "有效期策略"),
            col("shelf_life_value", "保质期值", "number"),
            col("shelf_life_unit", "保质期单位"),
            col("enabled", "启用", "boolean"),
            col("pms_updated_at", "PMS 更新时间", "datetime"),
            col("synced_at", "同步时间", "datetime"),
        ),
    ),
    "units": ProjectionDisplayTableSpec(
        resource="units",
        projection_table="d2c_pms_unit_projection",
        columns=(
            col("item_uom_id", "PMS item_uom_id", "number", "item_uom_id", "pms_item_uom_id"),
            col("item_id", "PMS item_id", "number", "item_id", "pms_item_id"),
            col("uom", "单位"),
            col("display_name", "展示", "text", "display_name", "uom_name"),
            col("ratio_to_base", "倍率", "number"),
            col("net_weight_kg", "净重", "number"),
            col("is_base", "基础单位", "boolean"),
            col("is_purchase_default", "采购默认", "boolean"),
            col("is_inbound_default", "入库默认", "boolean"),
            col("is_outbound_default", "出库默认", "boolean"),
            col("pms_updated_at", "PMS 更新时间", "datetime"),
            col("synced_at", "同步时间", "datetime"),
        ),
    ),
    "sku_codes": ProjectionDisplayTableSpec(
        resource="sku_codes",
        projection_table="d2c_pms_sku_code_projection",
        columns=(
            col("sku_code_id", "PMS sku_code_id", "number", "sku_code_id", "pms_sku_code_id"),
            col("item_id", "PMS item_id", "number", "item_id", "pms_item_id"),
            col("sku_code", "编码"),
            col("item_sku", "商品 SKU"),
            col("item_name", "商品名称"),
            col("code_type", "类型"),
            col("is_primary", "主编码", "boolean"),
            col("is_active", "状态", "boolean"),
            col("effective_from", "生效开始", "datetime"),
            col("effective_to", "生效结束", "datetime"),
            col("remark", "备注"),
            col("pms_updated_at", "PMS 更新时间", "datetime"),
            col("synced_at", "同步时间", "datetime"),
        ),
    ),
    "barcodes": ProjectionDisplayTableSpec(
        resource="barcodes",
        projection_table="d2c_pms_barcode_projection",
        columns=(
            col("barcode_id", "PMS barcode_id", "number", "barcode_id", "pms_barcode_id"),
            col("item_id", "PMS item_id", "number", "item_id", "pms_item_id"),
            col("item_uom_id", "PMS item_uom_id", "number", "item_uom_id", "pms_item_uom_id"),
            col("uom", "包装单位", "text", "uom", "uom_name"),
            col("net_weight_kg", "重量（kg）", "number"),
            col("barcode", "条码"),
            col("symbology", "码制"),
            col("is_primary", "主条码", "boolean"),
            col("active", "状态", "boolean"),
            col("pms_updated_at", "PMS 更新时间", "datetime"),
            col("synced_at", "同步时间", "datetime"),
        ),
    ),
    "item_contents": ProjectionDisplayTableSpec(
        resource="item_contents",
        projection_table="d2c_pms_item_content_projection",
        columns=(
            col("content_id", "ID", "number", "content_id", "pms_content_id"),
            col("item", "商品"),
            col("item_sku", "商品 SKU"),
            col("item_name", "商品名称"),
            col("base_title", "标准标题"),
            col("short_description", "短说明"),
            col("status", "状态", "status"),
            col("pms_updated_at", "PMS 更新时间", "datetime"),
            col("synced_at", "同步时间", "datetime"),
        ),
    ),
    "item_assets": ProjectionDisplayTableSpec(
        resource="item_assets",
        projection_table="d2c_pms_item_asset_projection",
        columns=(
            col("asset_id", "ID", "number", "asset_id", "pms_asset_id"),
            col("preview", "预览", "image", "url"),
            col("item", "商品"),
            col("item_sku", "商品 SKU"),
            col("item_name", "商品名称"),
            col("usage_type", "用途"),
            col("url", "URL", "url"),
            col("is_primary", "主素材", "boolean"),
            col("status", "状态", "status"),
            col("sort_order", "排序", "number"),
            col("pms_updated_at", "PMS 更新时间", "datetime"),
            col("synced_at", "同步时间", "datetime"),
        ),
    ),
    "display_categories": ProjectionDisplayTableSpec(
        resource="display_categories",
        projection_table="d2c_pms_display_category_projection",
        columns=(
            col(
                "display_category_id",
                "ID",
                "number",
                "display_category_id",
                "pms_display_category_id",
            ),
            col("image_url", "图片", "image"),
            col("path_code", "路径"),
            col("category_name", "分类名称"),
            col("display_name", "展示名"),
            col("level", "层级", "number"),
            col("is_leaf", "叶子", "boolean"),
            col("is_active", "状态", "boolean"),
            col("sort_order", "排序", "number"),
            col("pms_updated_at", "PMS 更新时间", "datetime"),
            col("synced_at", "同步时间", "datetime"),
        ),
    ),
    "item_display_category_bindings": ProjectionDisplayTableSpec(
        resource="item_display_category_bindings",
        projection_table="d2c_pms_item_display_category_binding_projection",
        columns=(
            col("binding_id", "ID", "number", "binding_id", "pms_binding_id"),
            col("item", "商品"),
            col("item_sku", "商品 SKU"),
            col("item_name", "商品名称"),
            col("display_category", "展示分类"),
            col("display_category_path_code", "展示分类路径"),
            col("is_primary", "主分类", "boolean"),
            col("sort_order", "排序", "number"),
            col("pms_updated_at", "PMS 更新时间", "datetime"),
            col("synced_at", "同步时间", "datetime"),
        ),
    ),
    "brand_profiles": ProjectionDisplayTableSpec(
        resource="brand_profiles",
        projection_table="d2c_pms_brand_profile_projection",
        columns=(
            col("profile_id", "ID", "number", "profile_id", "pms_profile_id"),
            col("brand", "品牌"),
            col("brand_code", "品牌编码"),
            col("brand_name", "品牌名称"),
            col("display_name", "展示名"),
            col("official_name", "官方名"),
            col("status", "状态", "status"),
            col("pms_updated_at", "PMS 更新时间", "datetime"),
            col("synced_at", "同步时间", "datetime"),
        ),
    ),
    "brand_assets": ProjectionDisplayTableSpec(
        resource="brand_assets",
        projection_table="d2c_pms_brand_asset_projection",
        columns=(
            col("asset_id", "ID", "number", "asset_id", "pms_asset_id"),
            col("preview", "预览", "image", "url"),
            col("brand", "品牌"),
            col("brand_code", "品牌编码"),
            col("brand_name", "品牌名称"),
            col("usage_type", "用途"),
            col("url", "URL", "url"),
            col("is_primary", "主素材", "boolean"),
            col("status", "状态", "status"),
            col("sort_order", "排序", "number"),
            col("pms_updated_at", "PMS 更新时间", "datetime"),
            col("synced_at", "同步时间", "datetime"),
        ),
    ),
}


def _model_to_dict(row: object) -> dict[str, Any]:
    if isinstance(row, BaseModel):
        return row.model_dump(mode="json")
    if isinstance(row, dict):
        return dict(row)
    return dict(getattr(row, "__dict__", {}))


def _raw_payload(data: dict[str, Any]) -> dict[str, Any]:
    raw = data.get("raw_payload")
    return raw if isinstance(raw, dict) else {}


def _lookup(data: dict[str, Any], spec: ProjectionDisplayColumnSpec) -> Any:
    raw = _raw_payload(data)

    if spec.key == "item":
        sku = data.get("item_sku") or raw.get("item_sku") or data.get("pms_sku") or raw.get("sku")
        name = data.get("item_name") or raw.get("item_name") or raw.get("name")
        return f"{sku or '—'} / {name or '—'}"

    if spec.key == "display_category":
        code = (
            data.get("display_category_path_code")
            or raw.get("display_category_path_code")
            or data.get("display_category_code")
            or raw.get("display_category_code")
        )
        name = data.get("display_category_name") or raw.get("display_category_name")
        return f"{code or '—'} / {name or '—'}"

    if spec.key == "brand":
        name = data.get("brand_name") or raw.get("brand_name") or raw.get("brand")
        code = data.get("brand_code") or raw.get("brand_code")
        if name and code:
            return f"{name} / {code}"
        return name or code

    for candidate in spec.candidates:
        if candidate in raw and raw[candidate] is not None:
            return raw[candidate]
        if candidate in data and data[candidate] is not None:
            return data[candidate]

    return None


def build_projection_display_table(
    resource: str,
    rows: list[object],
) -> dict[str, Any]:
    spec = DISPLAY_TABLE_SPECS[resource]

    return {
        "resource": spec.resource,
        "projection_table": spec.projection_table,
        "columns": [
            {
                "key": column.key,
                "label": column.label,
                "kind": column.kind,
                "source_field": column.candidates[0] if column.candidates else None,
            }
            for column in spec.columns
        ],
        "rows": [
            {column.key: _lookup(_model_to_dict(row), column) for column in spec.columns}
            for row in rows
        ],
    }


__all__ = [
    "DISPLAY_TABLE_SPECS",
    "ProjectionDisplayColumnSpec",
    "ProjectionDisplayTableSpec",
    "build_projection_display_table",
]
