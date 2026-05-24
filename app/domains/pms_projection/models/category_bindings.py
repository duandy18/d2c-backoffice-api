"""PMS item display category binding projection ORM model."""

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
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PmsItemDisplayCategoryBindingProjection(Base):
    __tablename__ = "d2c_pms_item_display_category_binding_projection"
    __table_args__ = (
        UniqueConstraint(
            "pms_binding_id",
            name="uq_d2c_pms_item_disp_bind_pid",
        ),
        UniqueConstraint(
            "pms_item_id",
            "pms_display_category_id",
            name="uq_d2c_pms_item_disp_bind_item_cat",
        ),
        CheckConstraint(
            "sort_order >= 0",
            name="ck_d2c_pms_item_disp_bind_sort",
        ),
        Index("ix_d2c_pms_item_disp_bind_item", "pms_item_id"),
        Index(
            "ix_d2c_pms_item_disp_bind_cat",
            "pms_display_category_id",
        ),
        Index(
            "uq_d2c_pms_item_disp_bind_primary",
            "pms_item_id",
            unique=True,
            postgresql_where="is_primary = true",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pms_binding_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pms_item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_product_projection.pms_item_id", ondelete="CASCADE"),
        nullable=False,
    )
    pms_display_category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "d2c_pms_display_category_projection.pms_display_category_id", ondelete="CASCADE"
        ),
        nullable=False,
    )
    item_sku: Mapped[str | None] = mapped_column(String(128), nullable=True)
    item_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    display_category_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    display_category_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    display_category_path_code: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_primary: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    pms_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


__all__ = ["PmsItemDisplayCategoryBindingProjection"]
