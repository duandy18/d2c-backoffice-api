"""D2C PromotionRule and coupon owner models.

PromotionRule is the merchant-owned rule definition. PromotionTarget decides
where the rule applies. Coupon is an optional trigger credential bound to a
PromotionRule.
"""

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


class PromotionRule(Base):
    __tablename__ = "d2c_promotion_rules"
    __table_args__ = (
        UniqueConstraint("promotion_code", name="uq_d2c_promotion_rules_code"),
        CheckConstraint("discount_value > 0", name="ck_d2c_promo_rules_discount"),
        CheckConstraint(
            "discount_type <> 'percentage' OR discount_value <= 100",
            name="ck_d2c_promo_rules_pct",
        ),
        CheckConstraint(
            "threshold_amount_cents IS NULL OR threshold_amount_cents >= 0",
            name="ck_d2c_promo_rules_threshold",
        ),
        CheckConstraint(
            "max_discount_cents IS NULL OR max_discount_cents >= 0",
            name="ck_d2c_promo_rules_max_discount",
        ),
        CheckConstraint(
            "ends_at IS NULL OR starts_at IS NULL OR ends_at > starts_at",
            name="ck_d2c_promo_rules_range",
        ),
        CheckConstraint("priority >= 0", name="ck_d2c_promo_rules_priority"),
        Index("ix_d2c_promo_rules_code", "promotion_code"),
        Index("ix_d2c_promo_rules_status", "status"),
        Index("ix_d2c_promo_rules_type", "promotion_type"),
        Index("ix_d2c_promo_rules_active_range", "is_active", "starts_at", "ends_at"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    promotion_code: Mapped[str] = mapped_column(String(64), nullable=False)
    promotion_name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    promotion_type: Mapped[str] = mapped_column(String(32), nullable=False)
    discount_type: Mapped[str] = mapped_column(String(32), nullable=False)
    discount_value: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_amount_cents: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_discount_cents: Mapped[int | None] = mapped_column(Integer, nullable=True)
    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="USD",
        server_default="USD",
    )
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="draft",
        server_default="draft",
    )
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    stackable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    display_badge: Mapped[str | None] = mapped_column(String(64), nullable=True)
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


class PromotionTarget(Base):
    __tablename__ = "d2c_promotion_targets"
    __table_args__ = (
        UniqueConstraint(
            "promotion_rule_id",
            "target_type",
            "target_id",
            "target_code",
            name="uq_d2c_promo_targets_scope",
        ),
        CheckConstraint(
            "target_type = 'all_store' OR target_id IS NOT NULL OR target_code IS NOT NULL",
            name="ck_d2c_promo_targets_present",
        ),
        Index("ix_d2c_promo_targets_rule", "promotion_rule_id"),
        Index("ix_d2c_promo_targets_target", "target_type", "target_id", "target_code"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    promotion_rule_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_promotion_rules.id", ondelete="CASCADE"),
        nullable=False,
    )
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)
    target_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    target_code: Mapped[str | None] = mapped_column(String(96), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class Coupon(Base):
    __tablename__ = "d2c_coupons"
    __table_args__ = (
        UniqueConstraint("coupon_code", name="uq_d2c_coupons_code"),
        CheckConstraint(
            "total_limit IS NULL OR total_limit > 0",
            name="ck_d2c_coupons_total_limit_positive",
        ),
        CheckConstraint(
            "per_customer_limit IS NULL OR per_customer_limit > 0",
            name="ck_d2c_coupons_per_customer_limit_positive",
        ),
        CheckConstraint(
            "ends_at IS NULL OR starts_at IS NULL OR ends_at > starts_at",
            name="ck_d2c_coupons_effective_range_valid",
        ),
        Index("ix_d2c_coupons_code", "coupon_code"),
        Index("ix_d2c_coupons_status", "status"),
        Index("ix_d2c_coupons_rule", "promotion_rule_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    coupon_code: Mapped[str] = mapped_column(String(64), nullable=False)
    coupon_name: Mapped[str] = mapped_column(String(160), nullable=False)
    promotion_rule_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_promotion_rules.id", ondelete="CASCADE"),
        nullable=False,
    )
    coupon_type: Mapped[str] = mapped_column(String(32), nullable=False)
    total_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    per_customer_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="draft",
        server_default="draft",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
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
