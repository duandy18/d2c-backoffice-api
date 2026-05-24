"""PMS unit projection ORM model."""

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


__all__ = ["PmsUnitProjection"]
