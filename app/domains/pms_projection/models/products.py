"""PMS product projection ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    DateTime,
    Index,
    Integer,
    String,
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


__all__ = ["PmsProductProjection"]
