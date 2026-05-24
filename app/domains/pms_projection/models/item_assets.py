"""PMS item asset projection ORM model."""

from __future__ import annotations

from datetime import datetime
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
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PmsItemAssetProjection(Base):
    __tablename__ = "d2c_pms_item_asset_projection"
    __table_args__ = (
        UniqueConstraint("pms_asset_id", name="uq_d2c_pms_item_asset_pid"),
        CheckConstraint("sort_order >= 0", name="ck_d2c_pms_item_asset_sort"),
        Index("ix_d2c_pms_item_asset_item_usage", "pms_item_id", "usage_type", "status"),
        Index(
            "uq_d2c_pms_item_asset_primary",
            "pms_item_id",
            "usage_type",
            unique=True,
            postgresql_where="is_primary = true AND status = 'active'",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pms_asset_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pms_item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_product_projection.pms_item_id", ondelete="CASCADE"),
        nullable=False,
    )
    item_sku: Mapped[str | None] = mapped_column(String(128), nullable=True)
    item_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    asset_type: Mapped[str] = mapped_column(String(32), nullable=False)
    usage_type: Mapped[str] = mapped_column(String(32), nullable=False)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False)
    object_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    alt_text: Mapped[str | None] = mapped_column(String(240), nullable=True)
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    is_primary: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    raw_meta: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    pms_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


__all__ = ["PmsItemAssetProjection"]
