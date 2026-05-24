"""PMS projection sync run ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    CheckConstraint,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PmsProjectionSyncRun(Base):
    __tablename__ = "d2c_pms_projection_sync_runs"
    __table_args__ = (
        CheckConstraint(
            "rows_fetched >= 0",
            name="ck_d2c_pms_projection_sync_rows_fetched_non_negative",
        ),
        CheckConstraint(
            "rows_upserted >= 0",
            name="ck_d2c_pms_projection_sync_rows_upserted_non_negative",
        ),
        CheckConstraint(
            "rows_deleted >= 0",
            name="ck_d2c_pms_projection_sync_rows_deleted_non_negative",
        ),
        Index("ix_d2c_pms_projection_sync_runs_scope_status", "sync_scope", "status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sync_scope: Mapped[str] = mapped_column(String(32), nullable=False)
    source_service: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="pms-api",
        server_default="pms-api",
    )
    source_base_url: Mapped[str | None] = mapped_column(String(240), nullable=True)
    source_endpoint: Mapped[str | None] = mapped_column(String(240), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    requested_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    rows_fetched: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    rows_upserted: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    rows_deleted: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    error_code: Mapped[str | None] = mapped_column(String(120), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_summary: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


__all__ = ["PmsProjectionSyncRun"]
