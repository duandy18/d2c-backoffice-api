"""D2C publish version ORM model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PublishVersion(Base):
    __tablename__ = "d2c_publish_versions"
    __table_args__ = (
        UniqueConstraint("publish_version", name="uq_d2c_publish_versions_version"),
        Index("ix_d2c_publish_versions_scope_status", "publish_scope", "status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    publish_scope: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="draft",
        server_default="draft",
    )
    source: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="manual",
        server_default="manual",
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
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
