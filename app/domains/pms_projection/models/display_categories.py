"""PMS display category projection ORM model."""

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


class PmsDisplayCategoryProjection(Base):
    __tablename__ = "d2c_pms_display_category_projection"
    __table_args__ = (
        UniqueConstraint(
            "pms_display_category_id",
            name="uq_d2c_pms_disp_cat_pid",
        ),
        UniqueConstraint("path_code", name="uq_d2c_pms_disp_cat_path"),
        CheckConstraint("level >= 1 AND level <= 3", name="ck_d2c_pms_disp_cat_level"),
        CheckConstraint("sort_order >= 0", name="ck_d2c_pms_disp_cat_sort"),
        Index("ix_d2c_pms_disp_cat_parent", "parent_id"),
        Index("ix_d2c_pms_disp_cat_active_leaf", "is_active", "is_leaf"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pms_display_category_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "d2c_pms_display_category_projection.pms_display_category_id", ondelete="SET NULL"
        ),
        nullable=True,
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    category_code: Mapped[str] = mapped_column(String(64), nullable=False)
    category_name: Mapped[str] = mapped_column(String(128), nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    path_code: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    is_leaf: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    pms_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


__all__ = ["PmsDisplayCategoryProjection"]
