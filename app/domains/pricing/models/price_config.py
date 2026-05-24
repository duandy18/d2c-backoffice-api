"""D2C merchant price configuration ORM models."""

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
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PriceConfig(Base):
    __tablename__ = "d2c_price_configs"
    __table_args__ = (
        UniqueConstraint("price_config_code", name="uq_d2c_price_configs_code"),
        CheckConstraint("price_cents >= 0", name="ck_d2c_price_configs_price_non_negative"),
        CheckConstraint("priority >= 0", name="ck_d2c_price_configs_priority_non_negative"),
        CheckConstraint(
            "compare_at_price_cents IS NULL OR compare_at_price_cents >= price_cents",
            name="ck_d2c_price_configs_compare_at_valid",
        ),
        CheckConstraint(
            "effective_until IS NULL OR effective_from IS NULL OR effective_until > effective_from",
            name="ck_d2c_price_configs_effective_range_valid",
        ),
        Index(
            "ix_d2c_price_configs_sku_channel_active",
            "sku_listing_config_id",
            "channel",
            "is_active",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sku_listing_config_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_sku_listing_configs.id", ondelete="CASCADE"),
        nullable=False,
    )
    price_config_code: Mapped[str] = mapped_column(String(96), nullable=False)
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
