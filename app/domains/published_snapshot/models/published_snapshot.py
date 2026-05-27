"""Published storefront snapshot ORM models.

Published snapshots are immutable runtime contracts generated from D2C
Backoffice owner rows. Customer runtime should consume these rows instead of
reading merchant owner tables directly.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PublishedGroup(Base):
    __tablename__ = "d2c_published_groups"
    __table_args__ = (
        UniqueConstraint("publish_version", "group_code", name="uq_d2c_pub_groups_code"),
        Index("ix_d2c_pub_groups_version_sort", "publish_version", "sort_order"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    group_code: Mapped[str] = mapped_column(String(96), nullable=False)
    group_name: Mapped[str] = mapped_column(String(160), nullable=False)
    group_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    display_status: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    source_group_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PublishedClientPage(Base):
    __tablename__ = "d2c_published_client_pages"
    __table_args__ = (
        UniqueConstraint("publish_version", "page_code", name="uq_d2c_pub_cp_pages_code"),
        Index("ix_d2c_pub_cp_pages_sort", "publish_version", "sort_order"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    page_code: Mapped[str] = mapped_column(String(96), nullable=False)
    page_type: Mapped[str] = mapped_column(String(32), nullable=False)
    route_path: Mapped[str] = mapped_column(String(240), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    seo_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    seo_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    display_status: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_page_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PublishedClientRegion(Base):
    __tablename__ = "d2c_published_client_regions"
    __table_args__ = (
        UniqueConstraint("publish_version", "region_code", name="uq_d2c_pub_cp_regions_code"),
        Index("ix_d2c_pub_cp_regions_page", "publish_version", "page_code", "sort_order"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    page_code: Mapped[str] = mapped_column(String(96), nullable=False)
    region_code: Mapped[str] = mapped_column(String(120), nullable=False)
    region_type: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False)
    max_blocks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    allowed_block_types: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    display_status: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_region_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PublishedClientBlockType(Base):
    __tablename__ = "d2c_published_client_block_types"
    __table_args__ = (
        UniqueConstraint("publish_version", "block_type", name="uq_d2c_pub_cp_blocks_code"),
        Index("ix_d2c_pub_cp_blocks_renderer", "publish_version", "renderer_key"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    block_type: Mapped[str] = mapped_column(String(64), nullable=False)
    display_name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    renderer_key: Mapped[str] = mapped_column(String(160), nullable=False)
    data_contract_version: Mapped[str] = mapped_column(String(32), nullable=False)
    allowed_region_types: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    allowed_content_types: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    layout_schema: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    slot_schema: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    action_schema: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    analytics_schema: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    display_status: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_block_type_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PublishedClientRegionBlock(Base):
    __tablename__ = "d2c_published_client_region_blocks"
    __table_args__ = (
        UniqueConstraint(
            "publish_version",
            "block_code",
            name="uq_d2c_pub_cp_region_blocks_code",
        ),
        Index(
            "ix_d2c_pub_cp_region_blocks_region",
            "publish_version",
            "page_code",
            "region_code",
            "sort_order",
        ),
        Index(
            "ix_d2c_pub_cp_region_blocks_renderer",
            "publish_version",
            "renderer_key",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    page_code: Mapped[str] = mapped_column(String(96), nullable=False)
    region_code: Mapped[str] = mapped_column(String(120), nullable=False)
    block_code: Mapped[str] = mapped_column(String(120), nullable=False)
    block_type: Mapped[str] = mapped_column(String(64), nullable=False)
    renderer_key: Mapped[str] = mapped_column(String(160), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    subtitle: Mapped[str | None] = mapped_column(String(240), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    display_status: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    visible_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    visible_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    content_source_type: Mapped[str] = mapped_column(String(32), nullable=False)
    content_source_ref: Mapped[str | None] = mapped_column(String(160), nullable=True)
    content_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_region_block_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PublishedClientSurface(Base):
    __tablename__ = "d2c_published_client_surfaces"
    __table_args__ = (
        UniqueConstraint("publish_version", "surface_code", name="uq_d2c_pub_cp_surfaces_code"),
        Index("ix_d2c_pub_cp_surfaces_type", "publish_version", "surface_type"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    surface_code: Mapped[str] = mapped_column(String(64), nullable=False)
    surface_name: Mapped[str] = mapped_column(String(160), nullable=False)
    surface_type: Mapped[str] = mapped_column(String(32), nullable=False)
    device_family: Mapped[str] = mapped_column(String(32), nullable=False)
    breakpoint_profile: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    supported_renderer_keys: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_surface_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PublishedClientDataBinding(Base):
    __tablename__ = "d2c_published_client_data_bindings"
    __table_args__ = (
        UniqueConstraint("publish_version", "binding_code", name="uq_d2c_pub_cp_bindings_code"),
        Index("ix_d2c_pub_cp_bindings_target", "publish_version", "target_type", "target_code"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
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
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_binding_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PublishedClientVisibilityRule(Base):
    __tablename__ = "d2c_published_client_visibility_rules"
    __table_args__ = (
        UniqueConstraint("publish_version", "rule_code", name="uq_d2c_pub_cp_vis_code"),
        Index(
            "ix_d2c_pub_cp_vis_target",
            "publish_version",
            "target_type",
            "target_code",
            "priority",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
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
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_rule_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PublishedClientActionPolicy(Base):
    __tablename__ = "d2c_published_client_action_policies"
    __table_args__ = (
        UniqueConstraint("publish_version", "policy_code", name="uq_d2c_pub_cp_actions_code"),
        Index("ix_d2c_pub_cp_actions_target", "publish_version", "target_type", "target_code"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    policy_code: Mapped[str] = mapped_column(String(96), nullable=False)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)
    target_code: Mapped[str] = mapped_column(String(120), nullable=False)
    action_type: Mapped[str] = mapped_column(String(32), nullable=False)
    label: Mapped[str | None] = mapped_column(String(120), nullable=True)
    target_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_page_code: Mapped[str | None] = mapped_column(String(96), nullable=True)
    target_ref: Mapped[str | None] = mapped_column(String(160), nullable=True)
    open_mode: Mapped[str] = mapped_column(String(32), nullable=False)
    action_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_policy_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PublishedClientTrackingPolicy(Base):
    __tablename__ = "d2c_published_client_tracking_policies"
    __table_args__ = (
        UniqueConstraint("publish_version", "policy_code", name="uq_d2c_pub_cp_tracking_code"),
        Index("ix_d2c_pub_cp_track_target", "publish_version", "target_type", "target_code"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    policy_code: Mapped[str] = mapped_column(String(96), nullable=False)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)
    target_code: Mapped[str] = mapped_column(String(120), nullable=False)
    event_name: Mapped[str] = mapped_column(String(96), nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    event_trigger: Mapped[str] = mapped_column(String(32), nullable=False)
    tracking_params: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_policy_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PublishedStorefrontSection(Base):
    __tablename__ = "d2c_published_storefront_sections"
    __table_args__ = (
        UniqueConstraint("publish_version", "section_code", name="uq_d2c_pub_sections_code"),
        Index("ix_d2c_pub_sections_group_sort", "publish_version", "group_code", "sort_order"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    section_code: Mapped[str] = mapped_column(String(96), nullable=False)
    section_type: Mapped[str] = mapped_column(String(32), nullable=False)
    group_code: Mapped[str | None] = mapped_column(String(96), nullable=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    subtitle: Mapped[str | None] = mapped_column(String(240), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    display_status: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    source_section_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PublishedStorefrontSectionLayout(Base):
    __tablename__ = "d2c_published_storefront_section_layouts"
    __table_args__ = (
        UniqueConstraint("publish_version", "section_code", name="uq_d2c_pub_section_layouts_code"),
        Index("ix_d2c_pub_section_layouts_display", "publish_version", "display_type"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    section_code: Mapped[str] = mapped_column(String(96), nullable=False)
    display_type: Mapped[str] = mapped_column(String(32), nullable=False)
    columns_desktop: Mapped[int] = mapped_column(Integer, nullable=False)
    columns_tablet: Mapped[int] = mapped_column(Integer, nullable=False)
    columns_mobile: Mapped[int] = mapped_column(Integer, nullable=False)
    card_size: Mapped[str] = mapped_column(String(32), nullable=False)
    image_ratio: Mapped[str] = mapped_column(String(16), nullable=False)
    show_promotion_badge: Mapped[bool] = mapped_column(Boolean, nullable=False)
    show_sales_summary: Mapped[bool] = mapped_column(Boolean, nullable=False)
    show_review_summary: Mapped[bool] = mapped_column(Boolean, nullable=False)
    show_compare_price: Mapped[bool] = mapped_column(Boolean, nullable=False)
    show_quantity_stepper: Mapped[bool] = mapped_column(Boolean, nullable=False)
    max_items: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_layout_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PublishedStorefrontSectionPosition(Base):
    __tablename__ = "d2c_published_storefront_section_positions"
    __table_args__ = (
        UniqueConstraint("publish_version", "position_code", name="uq_d2c_pub_sec_pos_code"),
        Index("ix_d2c_pub_sec_pos_section", "publish_version", "section_code", "sort_order"),
        Index("ix_d2c_pub_sec_pos_offer", "publish_version", "offer_code"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    section_code: Mapped[str] = mapped_column(String(96), nullable=False)
    position_code: Mapped[str] = mapped_column(String(120), nullable=False)
    offer_code: Mapped[str] = mapped_column(String(96), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    position_type: Mapped[str] = mapped_column(String(32), nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False)
    visible_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    visible_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_position_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PublishedOffer(Base):
    __tablename__ = "d2c_published_offers"
    __table_args__ = (
        UniqueConstraint("publish_version", "offer_code", name="uq_d2c_pub_offers_code"),
        Index("ix_d2c_pub_offers_version_type", "publish_version", "offer_type"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    offer_code: Mapped[str] = mapped_column(String(96), nullable=False)
    offer_type: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    subtitle: Mapped[str | None] = mapped_column(String(240), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_status: Mapped[str] = mapped_column(String(32), nullable=False)
    sell_status: Mapped[str] = mapped_column(String(32), nullable=False)
    source_offer_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PublishedOfferComponent(Base):
    __tablename__ = "d2c_published_offer_components"
    __table_args__ = (
        UniqueConstraint(
            "publish_version",
            "offer_code",
            "component_no",
            name="uq_d2c_pub_components_no",
        ),
        Index("ix_d2c_pub_components_offer", "publish_version", "offer_code"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    offer_code: Mapped[str] = mapped_column(String(96), nullable=False)
    component_no: Mapped[int] = mapped_column(Integer, nullable=False)
    pms_item_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pms_sku: Mapped[str] = mapped_column(String(128), nullable=False)
    pms_sku_code_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sku_code: Mapped[str] = mapped_column(String(128), nullable=False)
    pms_item_uom_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    uom_code: Mapped[str] = mapped_column(String(32), nullable=False)
    uom_name: Mapped[str] = mapped_column(String(80), nullable=False)
    pms_barcode_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    barcode: Mapped[str | None] = mapped_column(String(128), nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    component_role: Mapped[str] = mapped_column(String(32), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    required: Mapped[bool] = mapped_column(Boolean, nullable=False)
    source_component_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PublishedOfferPrice(Base):
    __tablename__ = "d2c_published_offer_prices"
    __table_args__ = (
        UniqueConstraint("publish_version", "price_code", name="uq_d2c_pub_prices_code"),
        Index("ix_d2c_pub_prices_offer", "publish_version", "offer_code", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    offer_code: Mapped[str] = mapped_column(String(96), nullable=False)
    price_code: Mapped[str] = mapped_column(String(96), nullable=False)
    channel: Mapped[str] = mapped_column(String(32), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    compare_at_price_cents: Mapped[int | None] = mapped_column(Integer, nullable=True)
    effective_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    effective_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    source_price_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PublishedOfferPosition(Base):
    __tablename__ = "d2c_published_offer_positions"
    __table_args__ = (
        UniqueConstraint("publish_version", "position_code", name="uq_d2c_pub_positions_code"),
        Index("ix_d2c_pub_positions_group", "publish_version", "group_code", "sort_order"),
        Index("ix_d2c_pub_positions_offer", "publish_version", "offer_code"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    position_code: Mapped[str] = mapped_column(String(120), nullable=False)
    group_code: Mapped[str] = mapped_column(String(96), nullable=False)
    offer_code: Mapped[str] = mapped_column(String(96), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    position_source: Mapped[str] = mapped_column(String(32), nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False)
    visible_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    visible_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    source_position_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PublishedPromotionRule(Base):
    __tablename__ = "d2c_published_promotion_rules"
    __table_args__ = (
        UniqueConstraint("publish_version", "promotion_code", name="uq_d2c_pub_rules_code"),
        Index("ix_d2c_pub_rules_active", "publish_version", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    promotion_code: Mapped[str] = mapped_column(String(64), nullable=False)
    promotion_name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    promotion_type: Mapped[str] = mapped_column(String(32), nullable=False)
    discount_type: Mapped[str] = mapped_column(String(32), nullable=False)
    discount_value: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_amount_cents: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_discount_cents: Mapped[int | None] = mapped_column(Integer, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    stackable: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    display_badge: Mapped[str | None] = mapped_column(String(64), nullable=True)
    source_promotion_rule_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PublishedPromotionTarget(Base):
    __tablename__ = "d2c_published_promotion_targets"
    __table_args__ = (
        UniqueConstraint(
            "publish_version",
            "promotion_code",
            "target_type",
            "target_code",
            "target_id",
            name="uq_d2c_pub_targets_scope",
        ),
        Index("ix_d2c_pub_targets_rule", "publish_version", "promotion_code"),
        Index("ix_d2c_pub_targets_target", "publish_version", "target_type", "target_code"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    promotion_code: Mapped[str] = mapped_column(String(64), nullable=False)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)
    target_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    target_code: Mapped[str | None] = mapped_column(String(96), nullable=True)
    source_target_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PublishedCoupon(Base):
    __tablename__ = "d2c_published_coupons"
    __table_args__ = (
        UniqueConstraint("publish_version", "coupon_code", name="uq_d2c_pub_coupons_code"),
        Index("ix_d2c_pub_coupons_rule", "publish_version", "promotion_code"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    publish_version: Mapped[str] = mapped_column(String(64), nullable=False)
    coupon_code: Mapped[str] = mapped_column(String(64), nullable=False)
    coupon_name: Mapped[str] = mapped_column(String(160), nullable=False)
    promotion_code: Mapped[str] = mapped_column(String(64), nullable=False)
    coupon_type: Mapped[str] = mapped_column(String(32), nullable=False)
    total_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    per_customer_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    source_coupon_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
