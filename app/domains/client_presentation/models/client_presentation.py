"""Client presentation owner models.

These models define the customer-client page protocol. They are D2C Backoffice
owner rows and are published into immutable runtime snapshots for d2c-api.
"""

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


class ClientPresentationPage(Base):
    __tablename__ = "d2c_client_pages"
    __table_args__ = (
        UniqueConstraint("page_code", name="uq_d2c_cp_pages_code"),
        UniqueConstraint("route_path", name="uq_d2c_cp_pages_route"),
        CheckConstraint("sort_order >= 0", name="ck_d2c_cp_pages_sort"),
        Index("ix_d2c_cp_pages_type", "page_type", "display_status", "is_active"),
        Index("ix_d2c_cp_pages_sort", "sort_order"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    page_code: Mapped[str] = mapped_column(String(96), nullable=False)
    page_type: Mapped[str] = mapped_column(String(32), nullable=False)
    route_path: Mapped[str] = mapped_column(String(240), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    seo_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    seo_description: Mapped[str | None] = mapped_column(Text, nullable=True)
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


class ClientPresentationRegion(Base):
    __tablename__ = "d2c_client_regions"
    __table_args__ = (
        UniqueConstraint("region_code", name="uq_d2c_cp_regions_code"),
        CheckConstraint("sort_order >= 0", name="ck_d2c_cp_regions_sort"),
        CheckConstraint("max_blocks IS NULL OR max_blocks > 0", name="ck_d2c_cp_regions_max"),
        Index("ix_d2c_cp_regions_page", "page_id", "sort_order"),
        Index("ix_d2c_cp_regions_type", "region_type", "display_status", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    page_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_client_pages.id", ondelete="CASCADE"),
        nullable=False,
    )
    region_code: Mapped[str] = mapped_column(String(120), nullable=False)
    region_type: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    is_required: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    max_blocks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    allowed_block_types: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
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


class ClientPresentationBlockType(Base):
    __tablename__ = "d2c_client_block_types"
    __table_args__ = (
        UniqueConstraint("block_type", name="uq_d2c_cp_block_types_code"),
        UniqueConstraint("renderer_key", name="uq_d2c_cp_block_types_renderer"),
        Index("ix_d2c_cp_block_types_status", "display_status", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    block_type: Mapped[str] = mapped_column(String(64), nullable=False)
    display_name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    renderer_key: Mapped[str] = mapped_column(String(160), nullable=False)
    data_contract_version: Mapped[str] = mapped_column(
        String(32), nullable=False, default="v1", server_default="v1"
    )
    allowed_region_types: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    allowed_content_types: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    layout_schema: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    slot_schema: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    action_schema: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    analytics_schema: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
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



class ClientPresentationSurface(Base):
    __tablename__ = "d2c_client_surfaces"
    __table_args__ = (
        UniqueConstraint("surface_code", name="uq_d2c_cp_surfaces_code"),
        Index("ix_d2c_cp_surfaces_type", "surface_type", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    surface_code: Mapped[str] = mapped_column(String(64), nullable=False)
    surface_name: Mapped[str] = mapped_column(String(160), nullable=False)
    surface_type: Mapped[str] = mapped_column(String(32), nullable=False)
    device_family: Mapped[str] = mapped_column(String(32), nullable=False)
    breakpoint_profile: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    supported_renderer_keys: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
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


class ClientPresentationDataBinding(Base):
    __tablename__ = "d2c_client_data_bindings"
    __table_args__ = (
        UniqueConstraint("binding_code", name="uq_d2c_cp_bindings_code"),
        CheckConstraint(
            "result_limit IS NULL OR result_limit > 0",
            name="ck_d2c_cp_bindings_limit",
        ),
        Index("ix_d2c_cp_bindings_target", "target_type", "target_code", "is_active"),
        Index("ix_d2c_cp_bindings_source", "data_source_type", "content_type"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    binding_code: Mapped[str] = mapped_column(String(96), nullable=False)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)
    target_code: Mapped[str] = mapped_column(String(120), nullable=False)
    data_source_type: Mapped[str] = mapped_column(String(32), nullable=False)
    data_source_ref: Mapped[str | None] = mapped_column(String(160), nullable=True)
    content_type: Mapped[str] = mapped_column(String(32), nullable=False)
    query_params: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    result_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sort_policy: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    refresh_policy: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
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


class ClientPresentationVisibilityRule(Base):
    __tablename__ = "d2c_client_visibility_rules"
    __table_args__ = (
        UniqueConstraint("rule_code", name="uq_d2c_cp_vis_code"),
        CheckConstraint("priority >= 0", name="ck_d2c_cp_vis_priority"),
        Index("ix_d2c_cp_vis_target", "target_type", "target_code", "is_active"),
        Index("ix_d2c_cp_vis_window", "visible_from", "visible_until"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    rule_code: Mapped[str] = mapped_column(String(96), nullable=False)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)
    target_code: Mapped[str] = mapped_column(String(120), nullable=False)
    client_surface_codes: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    customer_segments: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    login_state: Mapped[str | None] = mapped_column(String(32), nullable=True)
    locale: Mapped[str | None] = mapped_column(String(16), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    visible_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    visible_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rule_expression: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
        server_default="100",
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


class ClientPresentationActionPolicy(Base):
    __tablename__ = "d2c_client_action_policies"
    __table_args__ = (
        UniqueConstraint("policy_code", name="uq_d2c_cp_actions_code"),
        Index("ix_d2c_cp_actions_target", "target_type", "target_code", "is_active"),
        Index("ix_d2c_cp_actions_type", "action_type"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    policy_code: Mapped[str] = mapped_column(String(96), nullable=False)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)
    target_code: Mapped[str] = mapped_column(String(120), nullable=False)
    action_type: Mapped[str] = mapped_column(String(32), nullable=False)
    label: Mapped[str | None] = mapped_column(String(120), nullable=True)
    target_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_page_code: Mapped[str | None] = mapped_column(String(96), nullable=True)
    target_ref: Mapped[str | None] = mapped_column(String(160), nullable=True)
    open_mode: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="same",
        server_default="same",
    )
    action_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
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


class ClientPresentationTrackingPolicy(Base):
    __tablename__ = "d2c_client_tracking_policies"
    __table_args__ = (
        UniqueConstraint("policy_code", name="uq_d2c_cp_tracking_code"),
        Index("ix_d2c_cp_track_target", "target_type", "target_code", "is_active"),
        Index("ix_d2c_cp_track_event", "event_name", "event_type"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    policy_code: Mapped[str] = mapped_column(String(96), nullable=False)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)
    target_code: Mapped[str] = mapped_column(String(120), nullable=False)
    event_name: Mapped[str] = mapped_column(String(96), nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    event_trigger: Mapped[str] = mapped_column(String(32), nullable=False)
    tracking_params: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    is_required: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
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
