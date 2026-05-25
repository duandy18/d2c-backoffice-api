"""D2C storefront section and layout owner models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
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


class StorefrontSection(Base):
    __tablename__ = "d2c_storefront_sections"
    __table_args__ = (
        UniqueConstraint("section_code", name="uq_d2c_sections_code"),
        CheckConstraint("sort_order >= 0", name="ck_d2c_sections_sort"),
        Index("ix_d2c_sections_group_sort", "group_id", "sort_order"),
        Index("ix_d2c_sections_status", "section_type", "display_status", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    section_code: Mapped[str] = mapped_column(String(96), nullable=False)
    section_type: Mapped[str] = mapped_column(String(32), nullable=False)
    group_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("d2c_groups.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    subtitle: Mapped[str | None] = mapped_column(String(240), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    display_status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="visible", server_default="visible"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    source_type: Mapped[str] = mapped_column(
        String(32), nullable=False, default="manual", server_default="manual"
    )
    source_ref: Mapped[str | None] = mapped_column(String(160), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class StorefrontSectionLayout(Base):
    __tablename__ = "d2c_storefront_section_layouts"
    __table_args__ = (
        UniqueConstraint("section_id", name="uq_d2c_section_layouts_section"),
        CheckConstraint("columns_desktop > 0", name="ck_d2c_section_layout_desktop_cols"),
        CheckConstraint("columns_tablet > 0", name="ck_d2c_section_layout_tablet_cols"),
        CheckConstraint("columns_mobile > 0", name="ck_d2c_section_layout_mobile_cols"),
        CheckConstraint(
            "max_items IS NULL OR max_items > 0", name="ck_d2c_section_layout_max_items"
        ),
        Index("ix_d2c_section_layouts_display", "display_type"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    section_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_storefront_sections.id", ondelete="CASCADE"),
        nullable=False,
    )
    display_type: Mapped[str] = mapped_column(String(32), nullable=False)
    columns_desktop: Mapped[int] = mapped_column(
        Integer, nullable=False, default=4, server_default="4"
    )
    columns_tablet: Mapped[int] = mapped_column(
        Integer, nullable=False, default=2, server_default="2"
    )
    columns_mobile: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default="1"
    )
    card_size: Mapped[str] = mapped_column(
        String(32), nullable=False, default="standard", server_default="standard"
    )
    image_ratio: Mapped[str] = mapped_column(
        String(16), nullable=False, default="1:1", server_default="1:1"
    )
    show_promotion_badge: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    show_sales_summary: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    show_review_summary: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    show_compare_price: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    show_quantity_stepper: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    max_items: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
