"""D2C storefront group owner models.

Groups are D2C Backoffice-owned customer storefront shelves. PMS display
categories may seed groups, but PMS never owns the final customer-facing group
structure.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Group(Base):
    __tablename__ = "d2c_groups"
    __table_args__ = (
        UniqueConstraint("group_code", name="uq_d2c_groups_code"),
        CheckConstraint("sort_order >= 0", name="ck_d2c_groups_sort"),
        Index("ix_d2c_groups_kind_status", "group_kind", "display_status", "is_active"),
        Index("ix_d2c_groups_sort", "sort_order"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    group_code: Mapped[str] = mapped_column(String(96), nullable=False)
    group_name: Mapped[str] = mapped_column(String(160), nullable=False)
    group_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
        server_default="100",
    )
    display_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="visible",
        server_default="visible",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )
    source_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="manual",
        server_default="manual",
    )
    source_ref: Mapped[str | None] = mapped_column(String(160), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
