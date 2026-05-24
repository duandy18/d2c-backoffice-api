"""PMS item content projection ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PmsItemContentProjection(Base):
    __tablename__ = "d2c_pms_item_content_projection"
    __table_args__ = (
        UniqueConstraint("pms_content_id", name="uq_d2c_pms_item_content_pid"),
        UniqueConstraint("pms_item_id", name="uq_d2c_pms_item_content_item"),
        Index("ix_d2c_pms_item_content_status", "status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pms_content_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pms_item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_product_projection.pms_item_id", ondelete="CASCADE"),
        nullable=False,
    )
    item_sku: Mapped[str | None] = mapped_column(String(128), nullable=True)
    item_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    base_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    base_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    short_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    spec_params: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON, nullable=True)
    material_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    ingredients_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    dimensions_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    weight_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    safety_instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    usage_instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    storage_instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    pms_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


__all__ = ["PmsItemContentProjection"]
