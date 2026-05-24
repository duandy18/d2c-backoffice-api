"""PMS projection ORM models for D2C backoffice.

These tables are read-side copies of PMS master data. D2C backoffice must not
treat them as product owner tables; they only anchor merchant listing configs.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PmsProductProjection(Base):
    __tablename__ = "d2c_pms_product_projection"
    __table_args__ = (
        UniqueConstraint("pms_item_id", name="uq_d2c_pms_product_projection_item_id"),
        UniqueConstraint("pms_sku", name="uq_d2c_pms_product_projection_sku"),
        Index("ix_d2c_pms_product_projection_enabled", "enabled"),
        Index("ix_d2c_pms_product_projection_category", "category_id", "category_code"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pms_item_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pms_sku: Mapped[str] = mapped_column(String(128), nullable=False)
    item_name: Mapped[str] = mapped_column(String(200), nullable=False)
    item_spec: Mapped[str | None] = mapped_column(String(240), nullable=True)
    enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    supplier_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    brand_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    brand_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    brand_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    category_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    category_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    category_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    category_path_code: Mapped[str | None] = mapped_column(String(160), nullable=True)
    category_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    category_is_leaf: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    pms_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PmsUnitProjection(Base):
    __tablename__ = "d2c_pms_unit_projection"
    __table_args__ = (
        UniqueConstraint("pms_item_uom_id", name="uq_d2c_pms_unit_projection_item_uom_id"),
        CheckConstraint(
            "ratio_to_base > 0",
            name="ck_d2c_pms_unit_projection_ratio_positive",
        ),
        Index("ix_d2c_pms_unit_projection_item_id", "pms_item_id"),
        Index("ix_d2c_pms_unit_projection_usage", "is_base", "is_outbound_default"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pms_item_uom_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pms_item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_product_projection.pms_item_id", ondelete="CASCADE"),
        nullable=False,
    )
    uom: Mapped[str] = mapped_column(String(32), nullable=False)
    uom_name: Mapped[str] = mapped_column(String(80), nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    ratio_to_base: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    net_weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    is_base: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    is_purchase_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    is_inbound_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    is_outbound_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    pms_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PmsSkuCodeProjection(Base):
    __tablename__ = "d2c_pms_sku_code_projection"
    __table_args__ = (
        UniqueConstraint("pms_sku_code_id", name="uq_d2c_pms_sku_code_projection_id"),
        UniqueConstraint("sku_code", name="uq_d2c_pms_sku_code_projection_code"),
        CheckConstraint(
            "effective_to IS NULL OR effective_from IS NULL OR effective_to > effective_from",
            name="ck_d2c_pms_sku_code_projection_effective_range_valid",
        ),
        Index("ix_d2c_pms_sku_code_projection_item_id", "pms_item_id"),
        Index("ix_d2c_pms_sku_code_projection_primary_active", "is_primary", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pms_sku_code_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pms_item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_product_projection.pms_item_id", ondelete="CASCADE"),
        nullable=False,
    )
    sku_code: Mapped[str] = mapped_column(String(128), nullable=False)
    code_type: Mapped[str] = mapped_column(String(32), nullable=False)
    is_primary: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    effective_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    item_sku: Mapped[str] = mapped_column(String(128), nullable=False)
    item_name: Mapped[str] = mapped_column(String(200), nullable=False)
    item_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    pms_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PmsBarcodeProjection(Base):
    __tablename__ = "d2c_pms_barcode_projection"
    __table_args__ = (
        UniqueConstraint("pms_barcode_id", name="uq_d2c_pms_barcode_projection_id"),
        UniqueConstraint("barcode", name="uq_d2c_pms_barcode_projection_barcode"),
        CheckConstraint(
            "ratio_to_base > 0",
            name="ck_d2c_pms_barcode_projection_ratio_positive",
        ),
        Index("ix_d2c_pms_barcode_projection_item_id", "pms_item_id"),
        Index("ix_d2c_pms_barcode_projection_primary_active", "is_primary", "active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pms_barcode_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pms_item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_product_projection.pms_item_id", ondelete="CASCADE"),
        nullable=False,
    )
    pms_item_uom_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_unit_projection.pms_item_uom_id", ondelete="CASCADE"),
        nullable=False,
    )
    barcode: Mapped[str] = mapped_column(String(128), nullable=False)
    symbology: Mapped[str | None] = mapped_column(String(32), nullable=True)
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    is_primary: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    uom: Mapped[str] = mapped_column(String(32), nullable=False)
    uom_name: Mapped[str] = mapped_column(String(80), nullable=False)
    ratio_to_base: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    pms_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PmsProjectionSyncRun(Base):
    __tablename__ = "d2c_pms_projection_sync_runs"
    __table_args__ = (
        CheckConstraint(
            "rows_fetched >= 0",
            name="ck_d2c_pms_projection_sync_rows_fetched_non_negative",
        ),
        CheckConstraint(
            "rows_upserted >= 0",
            name="ck_d2c_pms_projection_sync_rows_upserted_non_negative",
        ),
        CheckConstraint(
            "rows_deleted >= 0",
            name="ck_d2c_pms_projection_sync_rows_deleted_non_negative",
        ),
        Index("ix_d2c_pms_projection_sync_runs_scope_status", "sync_scope", "status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sync_scope: Mapped[str] = mapped_column(String(32), nullable=False)
    source_service: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="pms-api",
        server_default="pms-api",
    )
    source_base_url: Mapped[str | None] = mapped_column(String(240), nullable=True)
    source_endpoint: Mapped[str | None] = mapped_column(String(240), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    requested_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    rows_fetched: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    rows_upserted: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    rows_deleted: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    error_code: Mapped[str | None] = mapped_column(String(120), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_summary: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
