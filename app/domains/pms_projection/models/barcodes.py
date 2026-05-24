"""PMS barcode projection ORM model."""

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
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


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


__all__ = ["PmsBarcodeProjection"]
