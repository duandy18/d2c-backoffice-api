"""PMS brand profile projection ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, BigInteger, DateTime, Index, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PmsBrandProfileProjection(Base):
    __tablename__ = "d2c_pms_brand_profile_projection"
    __table_args__ = (
        UniqueConstraint("pms_profile_id", name="uq_d2c_pms_brand_profile_pid"),
        UniqueConstraint("brand_id", name="uq_d2c_pms_brand_profile_brand"),
        Index("ix_d2c_pms_brand_profile_status", "status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pms_profile_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    brand_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    brand_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    brand_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    display_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    official_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    brand_story: Mapped[str | None] = mapped_column(Text, nullable=True)
    country_or_region: Mapped[str | None] = mapped_column(String(64), nullable=True)
    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    seo_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    seo_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    pms_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


__all__ = ["PmsBrandProfileProjection"]
