"""D2C Offer owner models.

Offer is the customer-facing sellable unit. It may represent a single PMS SKU,
a multi-pack, or a bundle. Group and Position decide where an Offer appears;
OfferPrice decides the base sell price; PromotionRule/Coupon decide runtime
discounts.
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


class Offer(Base):
    __tablename__ = "d2c_offers"
    __table_args__ = (
        UniqueConstraint("offer_code", name="uq_d2c_offers_code"),
        CheckConstraint("sort_order >= 0", name="ck_d2c_offers_sort"),
        CheckConstraint(
            "visible_until IS NULL OR visible_from IS NULL OR visible_until > visible_from",
            name="ck_d2c_offers_visible_range",
        ),
        Index("ix_d2c_offers_type_status", "offer_type", "display_status", "sell_status"),
        Index("ix_d2c_offers_publish_status", "publish_status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    offer_code: Mapped[str] = mapped_column(String(96), nullable=False)
    offer_type: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    subtitle: Mapped[str | None] = mapped_column(String(240), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="hidden",
        server_default="hidden",
    )
    sell_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="not_sellable",
        server_default="not_sellable",
    )
    publish_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="draft",
        server_default="draft",
    )
    source_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="manual",
        server_default="manual",
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    visible_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    visible_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
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


class OfferComponent(Base):
    __tablename__ = "d2c_offer_components"
    __table_args__ = (
        UniqueConstraint("offer_id", "component_no", name="uq_d2c_offer_components_no"),
        CheckConstraint("quantity > 0", name="ck_d2c_offer_components_qty"),
        CheckConstraint("sort_order >= 0", name="ck_d2c_offer_components_sort"),
        Index("ix_d2c_offer_components_offer", "offer_id"),
        Index("ix_d2c_offer_components_pms_item", "pms_item_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    offer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_offers.id", ondelete="CASCADE"),
        nullable=False,
    )
    component_no: Mapped[int] = mapped_column(Integer, nullable=False)
    pms_item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_product_projection.pms_item_id", ondelete="RESTRICT"),
        nullable=False,
    )
    pms_sku: Mapped[str] = mapped_column(String(128), nullable=False)
    pms_sku_code_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_sku_code_projection.pms_sku_code_id", ondelete="RESTRICT"),
        nullable=False,
    )
    sku_code: Mapped[str] = mapped_column(String(128), nullable=False)
    pms_item_uom_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_unit_projection.pms_item_uom_id", ondelete="RESTRICT"),
        nullable=False,
    )
    uom_code: Mapped[str] = mapped_column(String(32), nullable=False)
    uom_name: Mapped[str] = mapped_column(String(80), nullable=False)
    pms_barcode_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_barcode_projection.pms_barcode_id", ondelete="SET NULL"),
        nullable=True,
    )
    barcode: Mapped[str | None] = mapped_column(String(128), nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    component_role: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="primary",
        server_default="primary",
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    required: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
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


class OfferPrice(Base):
    __tablename__ = "d2c_offer_prices"
    __table_args__ = (
        UniqueConstraint("price_code", name="uq_d2c_offer_prices_code"),
        CheckConstraint("price_cents >= 0", name="ck_d2c_offer_prices_price"),
        CheckConstraint("priority >= 0", name="ck_d2c_offer_prices_priority"),
        CheckConstraint(
            "compare_at_price_cents IS NULL OR compare_at_price_cents >= price_cents",
            name="ck_d2c_offer_prices_compare",
        ),
        CheckConstraint(
            "effective_until IS NULL OR effective_from IS NULL OR effective_until > effective_from",
            name="ck_d2c_offer_prices_range",
        ),
        Index("ix_d2c_offer_prices_offer_active", "offer_id", "channel", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    offer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_offers.id", ondelete="CASCADE"),
        nullable=False,
    )
    price_code: Mapped[str] = mapped_column(String(96), nullable=False)
    channel: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="storefront",
        server_default="storefront",
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="USD",
        server_default="USD",
    )
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    compare_at_price_cents: Mapped[int | None] = mapped_column(Integer, nullable=True)
    effective_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    effective_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
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


class OfferPosition(Base):
    __tablename__ = "d2c_offer_positions"
    __table_args__ = (
        UniqueConstraint("position_code", name="uq_d2c_offer_positions_code"),
        UniqueConstraint("group_id", "offer_id", name="uq_d2c_offer_positions_group_offer"),
        CheckConstraint("sort_order >= 0", name="ck_d2c_offer_positions_sort"),
        CheckConstraint(
            "visible_until IS NULL OR visible_from IS NULL OR visible_until > visible_from",
            name="ck_d2c_offer_positions_range",
        ),
        Index("ix_d2c_offer_positions_group_sort", "group_id", "sort_order"),
        Index("ix_d2c_offer_positions_offer", "offer_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    position_code: Mapped[str] = mapped_column(String(120), nullable=False)
    group_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_groups.id", ondelete="CASCADE"),
        nullable=False,
    )
    offer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_offers.id", ondelete="CASCADE"),
        nullable=False,
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    position_source: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="manual",
        server_default="manual",
    )
    is_featured: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    visible_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    visible_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
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
