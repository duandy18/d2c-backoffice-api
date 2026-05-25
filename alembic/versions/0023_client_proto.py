"""add_client_presentation_protocol_services.

Revision ID: 0023_client_proto
Revises: 0022_client_found
Create Date: 2026-05-25
"""

from __future__ import annotations

import json
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0023_client_proto"
down_revision: str | Sequence[str] | None = "0022_client_found"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


SURFACE_ROWS = [
    {
        "surface_code": "web_desktop",
        "surface_name": "Web 桌面端",
        "surface_type": "web",
        "device_family": "desktop",
        "breakpoint_profile": {"min_width": 1024, "layout": "desktop"},
        "supported_renderer_keys": [
            "storefront.hero_banner",
            "storefront.promo_strip",
            "storefront.category_nav",
            "storefront.offer_shelf",
            "storefront.ranking_list",
            "storefront.image_grid",
            "storefront.rich_text",
            "storefront.coupon_strip",
            "storefront.product_summary",
            "storefront.product_recommendation",
        ],
    },
    {
        "surface_code": "web_mobile",
        "surface_name": "Web 移动端",
        "surface_type": "web",
        "device_family": "mobile",
        "breakpoint_profile": {"max_width": 767, "layout": "mobile"},
        "supported_renderer_keys": [
            "storefront.hero_banner",
            "storefront.promo_strip",
            "storefront.category_nav",
            "storefront.offer_shelf",
            "storefront.image_grid",
            "storefront.coupon_strip",
            "storefront.product_summary",
            "storefront.product_recommendation",
        ],
    },
    {
        "surface_code": "app",
        "surface_name": "App",
        "surface_type": "app",
        "device_family": "mobile",
        "breakpoint_profile": {"layout": "native_mobile"},
        "supported_renderer_keys": [
            "storefront.hero_banner",
            "storefront.promo_strip",
            "storefront.category_nav",
            "storefront.offer_shelf",
            "storefront.coupon_strip",
            "storefront.product_summary",
            "storefront.product_recommendation",
        ],
    },
]

DATA_BINDING_ROWS = [
    {
        "binding_code": "binding.home.main.offer_shelf.manual",
        "target_type": "block_type",
        "target_code": "offer_shelf",
        "data_source_type": "manual_positions",
        "data_source_ref": "storefront_section_positions",
        "content_type": "offer",
        "query_params": {"section_scope": "home.main"},
        "result_limit": 20,
        "sort_policy": {"order_by": ["sort_order", "position_code"]},
        "refresh_policy": {"mode": "publish_snapshot"},
    },
    {
        "binding_code": "binding.home.quick_nav.category_nav.groups",
        "target_type": "block_type",
        "target_code": "category_nav",
        "data_source_type": "group_collection",
        "data_source_ref": "active_groups",
        "content_type": "group",
        "query_params": {"group_kind": ["category", "collection"]},
        "result_limit": 12,
        "sort_policy": {"order_by": ["sort_order", "group_code"]},
        "refresh_policy": {"mode": "publish_snapshot"},
    },
    {
        "binding_code": "binding.product.recommendation.offers",
        "target_type": "region",
        "target_code": "product.recommendation",
        "data_source_type": "manual_positions",
        "data_source_ref": "storefront_section_positions",
        "content_type": "offer",
        "query_params": {"region_code": "product.recommendation"},
        "result_limit": 8,
        "sort_policy": {"order_by": ["sort_order", "position_code"]},
        "refresh_policy": {"mode": "publish_snapshot"},
    },
]

VISIBILITY_ROWS = [
    {
        "rule_code": "visibility.default.all_surfaces",
        "target_type": "global",
        "target_code": "client_presentation",
        "client_surface_codes": ["web_desktop", "web_mobile", "app"],
        "customer_segments": ["all"],
        "login_state": "any",
        "locale": None,
        "currency": None,
        "rule_expression": {"allow": True},
        "priority": 10,
    },
    {
        "rule_code": "visibility.home.main.active",
        "target_type": "region",
        "target_code": "home.main",
        "client_surface_codes": ["web_desktop", "web_mobile", "app"],
        "customer_segments": ["all"],
        "login_state": "any",
        "locale": None,
        "currency": None,
        "rule_expression": {"display_status": "visible"},
        "priority": 20,
    },
]

ACTION_ROWS = [
    {
        "policy_code": "action.offer_shelf.open_offer",
        "target_type": "block_type",
        "target_code": "offer_shelf",
        "action_type": "open_offer",
        "label": "查看商品",
        "target_url": None,
        "target_page_code": "product_detail",
        "target_ref": "offer_code",
        "open_mode": "same",
        "action_payload": {"param": "offer_code"},
    },
    {
        "policy_code": "action.offer_shelf.add_to_cart",
        "target_type": "block_type",
        "target_code": "offer_shelf",
        "action_type": "add_to_cart",
        "label": "加入购物车",
        "target_url": None,
        "target_page_code": None,
        "target_ref": "offer_code",
        "open_mode": "inline",
        "action_payload": {"requires_quantity": True},
    },
    {
        "policy_code": "action.hero_banner.open_link",
        "target_type": "block_type",
        "target_code": "hero_banner",
        "action_type": "open_link",
        "label": "查看活动",
        "target_url": None,
        "target_page_code": "campaign",
        "target_ref": "campaign_code",
        "open_mode": "same",
        "action_payload": {"param": "campaign_code"},
    },
]

TRACKING_ROWS = [
    {
        "policy_code": "tracking.offer_shelf.impression",
        "target_type": "block_type",
        "target_code": "offer_shelf",
        "event_name": "offer_shelf_impression",
        "event_type": "impression",
        "event_trigger": "view",
        "tracking_params": {"include": ["section_code", "position_code", "offer_code"]},
        "is_required": True,
    },
    {
        "policy_code": "tracking.offer_shelf.click",
        "target_type": "block_type",
        "target_code": "offer_shelf",
        "event_name": "offer_shelf_click",
        "event_type": "click",
        "event_trigger": "click",
        "tracking_params": {"include": ["section_code", "position_code", "offer_code"]},
        "is_required": True,
    },
    {
        "policy_code": "tracking.offer_shelf.add_to_cart",
        "target_type": "block_type",
        "target_code": "offer_shelf",
        "event_name": "add_to_cart",
        "event_type": "conversion",
        "event_trigger": "action_success",
        "tracking_params": {"include": ["offer_code", "quantity", "price_cents"]},
        "is_required": True,
    },
]


def _json(value: object) -> str:
    return json.dumps(value)


def upgrade() -> None:
    op.create_table(
        "d2c_client_surfaces",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("surface_code", sa.String(length=64), nullable=False),
        sa.Column("surface_name", sa.String(length=160), nullable=False),
        sa.Column("surface_type", sa.String(length=32), nullable=False),
        sa.Column("device_family", sa.String(length=32), nullable=False),
        sa.Column("breakpoint_profile", sa.JSON(), nullable=True),
        sa.Column("supported_renderer_keys", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("source_type", sa.String(length=32), server_default="manual", nullable=False),
        sa.Column("source_ref", sa.String(length=160), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("surface_code", name="uq_d2c_cp_surfaces_code"),
    )
    op.create_index("ix_d2c_cp_surfaces_type", "d2c_client_surfaces", ["surface_type", "is_active"])

    op.create_table(
        "d2c_client_data_bindings",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("binding_code", sa.String(length=96), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_code", sa.String(length=120), nullable=False),
        sa.Column("data_source_type", sa.String(length=32), nullable=False),
        sa.Column("data_source_ref", sa.String(length=160), nullable=True),
        sa.Column("content_type", sa.String(length=32), nullable=False),
        sa.Column("query_params", sa.JSON(), nullable=True),
        sa.Column("result_limit", sa.Integer(), nullable=True),
        sa.Column("sort_policy", sa.JSON(), nullable=True),
        sa.Column("refresh_policy", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("source_type", sa.String(length=32), server_default="manual", nullable=False),
        sa.Column("source_ref", sa.String(length=160), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "result_limit IS NULL OR result_limit > 0",
            name="ck_d2c_cp_bindings_limit",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("binding_code", name="uq_d2c_cp_bindings_code"),
    )
    op.create_index(
        "ix_d2c_cp_bindings_target",
        "d2c_client_data_bindings",
        ["target_type", "target_code", "is_active"],
    )
    op.create_index(
        "ix_d2c_cp_bindings_source",
        "d2c_client_data_bindings",
        ["data_source_type", "content_type"],
    )

    op.create_table(
        "d2c_client_visibility_rules",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("rule_code", sa.String(length=96), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_code", sa.String(length=120), nullable=False),
        sa.Column("client_surface_codes", sa.JSON(), nullable=True),
        sa.Column("customer_segments", sa.JSON(), nullable=True),
        sa.Column("login_state", sa.String(length=32), nullable=True),
        sa.Column("locale", sa.String(length=16), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=True),
        sa.Column("visible_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("visible_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rule_expression", sa.JSON(), nullable=True),
        sa.Column("priority", sa.Integer(), server_default="100", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("source_type", sa.String(length=32), server_default="manual", nullable=False),
        sa.Column("source_ref", sa.String(length=160), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("priority >= 0", name="ck_d2c_cp_vis_priority"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("rule_code", name="uq_d2c_cp_vis_code"),
    )
    op.create_index(
        "ix_d2c_cp_vis_target",
        "d2c_client_visibility_rules",
        ["target_type", "target_code", "is_active"],
    )
    op.create_index(
        "ix_d2c_cp_vis_window",
        "d2c_client_visibility_rules",
        ["visible_from", "visible_until"],
    )

    op.create_table(
        "d2c_client_action_policies",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("policy_code", sa.String(length=96), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_code", sa.String(length=120), nullable=False),
        sa.Column("action_type", sa.String(length=32), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=True),
        sa.Column("target_url", sa.Text(), nullable=True),
        sa.Column("target_page_code", sa.String(length=96), nullable=True),
        sa.Column("target_ref", sa.String(length=160), nullable=True),
        sa.Column("open_mode", sa.String(length=32), server_default="same", nullable=False),
        sa.Column("action_payload", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("source_type", sa.String(length=32), server_default="manual", nullable=False),
        sa.Column("source_ref", sa.String(length=160), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("policy_code", name="uq_d2c_cp_actions_code"),
    )
    op.create_index(
        "ix_d2c_cp_actions_target",
        "d2c_client_action_policies",
        ["target_type", "target_code", "is_active"],
    )
    op.create_index("ix_d2c_cp_actions_type", "d2c_client_action_policies", ["action_type"])

    op.create_table(
        "d2c_client_tracking_policies",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("policy_code", sa.String(length=96), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_code", sa.String(length=120), nullable=False),
        sa.Column("event_name", sa.String(length=96), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("event_trigger", sa.String(length=32), nullable=False),
        sa.Column("tracking_params", sa.JSON(), nullable=True),
        sa.Column("is_required", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("source_type", sa.String(length=32), server_default="manual", nullable=False),
        sa.Column("source_ref", sa.String(length=160), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("policy_code", name="uq_d2c_cp_tracking_code"),
    )
    op.create_index(
        "ix_d2c_cp_track_target",
        "d2c_client_tracking_policies",
        ["target_type", "target_code", "is_active"],
    )
    op.create_index(
        "ix_d2c_cp_track_event",
        "d2c_client_tracking_policies",
        ["event_name", "event_type"],
    )

    op.create_table(
        "d2c_published_client_surfaces",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("surface_code", sa.String(length=64), nullable=False),
        sa.Column("surface_name", sa.String(length=160), nullable=False),
        sa.Column("surface_type", sa.String(length=32), nullable=False),
        sa.Column("device_family", sa.String(length=32), nullable=False),
        sa.Column("breakpoint_profile", sa.JSON(), nullable=True),
        sa.Column("supported_renderer_keys", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_surface_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publish_version", "surface_code", name="uq_d2c_pub_cp_surfaces_code"),
    )
    op.create_index(
        "ix_d2c_pub_cp_surfaces_type",
        "d2c_published_client_surfaces",
        ["publish_version", "surface_type"],
    )

    op.create_table(
        "d2c_published_client_data_bindings",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("binding_code", sa.String(length=96), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_code", sa.String(length=120), nullable=False),
        sa.Column("data_source_type", sa.String(length=32), nullable=False),
        sa.Column("data_source_ref", sa.String(length=160), nullable=True),
        sa.Column("content_type", sa.String(length=32), nullable=False),
        sa.Column("query_params", sa.JSON(), nullable=True),
        sa.Column("result_limit", sa.Integer(), nullable=True),
        sa.Column("sort_policy", sa.JSON(), nullable=True),
        sa.Column("refresh_policy", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_binding_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publish_version", "binding_code", name="uq_d2c_pub_cp_bindings_code"),
    )
    op.create_index(
        "ix_d2c_pub_cp_bindings_target",
        "d2c_published_client_data_bindings",
        ["publish_version", "target_type", "target_code"],
    )

    op.create_table(
        "d2c_published_client_visibility_rules",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("rule_code", sa.String(length=96), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_code", sa.String(length=120), nullable=False),
        sa.Column("client_surface_codes", sa.JSON(), nullable=True),
        sa.Column("customer_segments", sa.JSON(), nullable=True),
        sa.Column("login_state", sa.String(length=32), nullable=True),
        sa.Column("locale", sa.String(length=16), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=True),
        sa.Column("visible_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("visible_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rule_expression", sa.JSON(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_rule_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publish_version", "rule_code", name="uq_d2c_pub_cp_vis_code"),
    )
    op.create_index(
        "ix_d2c_pub_cp_vis_target",
        "d2c_published_client_visibility_rules",
        ["publish_version", "target_type", "target_code", "priority"],
    )

    op.create_table(
        "d2c_published_client_action_policies",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("policy_code", sa.String(length=96), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_code", sa.String(length=120), nullable=False),
        sa.Column("action_type", sa.String(length=32), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=True),
        sa.Column("target_url", sa.Text(), nullable=True),
        sa.Column("target_page_code", sa.String(length=96), nullable=True),
        sa.Column("target_ref", sa.String(length=160), nullable=True),
        sa.Column("open_mode", sa.String(length=32), nullable=False),
        sa.Column("action_payload", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_policy_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publish_version", "policy_code", name="uq_d2c_pub_cp_actions_code"),
    )
    op.create_index(
        "ix_d2c_pub_cp_actions_target",
        "d2c_published_client_action_policies",
        ["publish_version", "target_type", "target_code"],
    )

    op.create_table(
        "d2c_published_client_tracking_policies",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("policy_code", sa.String(length=96), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_code", sa.String(length=120), nullable=False),
        sa.Column("event_name", sa.String(length=96), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("event_trigger", sa.String(length=32), nullable=False),
        sa.Column("tracking_params", sa.JSON(), nullable=True),
        sa.Column("is_required", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_policy_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publish_version", "policy_code", name="uq_d2c_pub_cp_tracking_code"),
    )
    op.create_index(
        "ix_d2c_pub_cp_track_target",
        "d2c_published_client_tracking_policies",
        ["publish_version", "target_type", "target_code"],
    )

    for row in SURFACE_ROWS:
        op.execute(
            sa.text(
                """
                INSERT INTO d2c_client_surfaces (
                    surface_code, surface_name, surface_type, device_family,
                    breakpoint_profile, supported_renderer_keys,
                    is_active, source_type, source_ref
                )
                VALUES (
                    :surface_code, :surface_name, :surface_type, :device_family,
                    CAST(:breakpoint_profile AS json),
                    CAST(:supported_renderer_keys AS json),
                    true, 'seed', 'client_presentation_protocol_services'
                )
                """
            ).bindparams(
                surface_code=row["surface_code"],
                surface_name=row["surface_name"],
                surface_type=row["surface_type"],
                device_family=row["device_family"],
                breakpoint_profile=_json(row["breakpoint_profile"]),
                supported_renderer_keys=_json(row["supported_renderer_keys"]),
            )
        )

    for row in DATA_BINDING_ROWS:
        op.execute(
            sa.text(
                """
                INSERT INTO d2c_client_data_bindings (
                    binding_code, target_type, target_code,
                    data_source_type, data_source_ref, content_type,
                    query_params, result_limit, sort_policy, refresh_policy,
                    is_active, source_type, source_ref
                )
                VALUES (
                    :binding_code, :target_type, :target_code,
                    :data_source_type, :data_source_ref, :content_type,
                    CAST(:query_params AS json), :result_limit,
                    CAST(:sort_policy AS json), CAST(:refresh_policy AS json),
                    true, 'seed', 'client_presentation_protocol_services'
                )
                """
            ).bindparams(
                binding_code=row["binding_code"],
                target_type=row["target_type"],
                target_code=row["target_code"],
                data_source_type=row["data_source_type"],
                data_source_ref=row["data_source_ref"],
                content_type=row["content_type"],
                query_params=_json(row["query_params"]),
                result_limit=row["result_limit"],
                sort_policy=_json(row["sort_policy"]),
                refresh_policy=_json(row["refresh_policy"]),
            )
        )

    for row in VISIBILITY_ROWS:
        op.execute(
            sa.text(
                """
                INSERT INTO d2c_client_visibility_rules (
                    rule_code, target_type, target_code,
                    client_surface_codes, customer_segments, login_state,
                    locale, currency, rule_expression, priority,
                    is_active, source_type, source_ref
                )
                VALUES (
                    :rule_code, :target_type, :target_code,
                    CAST(:client_surface_codes AS json),
                    CAST(:customer_segments AS json),
                    :login_state, :locale, :currency,
                    CAST(:rule_expression AS json), :priority,
                    true, 'seed', 'client_presentation_protocol_services'
                )
                """
            ).bindparams(
                rule_code=row["rule_code"],
                target_type=row["target_type"],
                target_code=row["target_code"],
                client_surface_codes=_json(row["client_surface_codes"]),
                customer_segments=_json(row["customer_segments"]),
                login_state=row["login_state"],
                locale=row["locale"],
                currency=row["currency"],
                rule_expression=_json(row["rule_expression"]),
                priority=row["priority"],
            )
        )

    for row in ACTION_ROWS:
        op.execute(
            sa.text(
                """
                INSERT INTO d2c_client_action_policies (
                    policy_code, target_type, target_code, action_type, label,
                    target_url, target_page_code, target_ref, open_mode,
                    action_payload, is_active, source_type, source_ref
                )
                VALUES (
                    :policy_code, :target_type, :target_code, :action_type, :label,
                    :target_url, :target_page_code, :target_ref, :open_mode,
                    CAST(:action_payload AS json),
                    true, 'seed', 'client_presentation_protocol_services'
                )
                """
            ).bindparams(
                policy_code=row["policy_code"],
                target_type=row["target_type"],
                target_code=row["target_code"],
                action_type=row["action_type"],
                label=row["label"],
                target_url=row["target_url"],
                target_page_code=row["target_page_code"],
                target_ref=row["target_ref"],
                open_mode=row["open_mode"],
                action_payload=_json(row["action_payload"]),
            )
        )

    for row in TRACKING_ROWS:
        op.execute(
            sa.text(
                """
                INSERT INTO d2c_client_tracking_policies (
                    policy_code, target_type, target_code,
                    event_name, event_type, event_trigger,
                    tracking_params, is_required,
                    is_active, source_type, source_ref
                )
                VALUES (
                    :policy_code, :target_type, :target_code,
                    :event_name, :event_type, :event_trigger,
                    CAST(:tracking_params AS json), :is_required,
                    true, 'seed', 'client_presentation_protocol_services'
                )
                """
            ).bindparams(
                policy_code=row["policy_code"],
                target_type=row["target_type"],
                target_code=row["target_code"],
                event_name=row["event_name"],
                event_type=row["event_type"],
                event_trigger=row["event_trigger"],
                tracking_params=_json(row["tracking_params"]),
                is_required=row["is_required"],
            )
        )


def downgrade() -> None:
    op.drop_index("ix_d2c_pub_cp_track_target", table_name="d2c_published_client_tracking_policies")
    op.drop_table("d2c_published_client_tracking_policies")
    op.drop_index("ix_d2c_pub_cp_actions_target", table_name="d2c_published_client_action_policies")
    op.drop_table("d2c_published_client_action_policies")
    op.drop_index("ix_d2c_pub_cp_vis_target", table_name="d2c_published_client_visibility_rules")
    op.drop_table("d2c_published_client_visibility_rules")
    op.drop_index("ix_d2c_pub_cp_bindings_target", table_name="d2c_published_client_data_bindings")
    op.drop_table("d2c_published_client_data_bindings")
    op.drop_index("ix_d2c_pub_cp_surfaces_type", table_name="d2c_published_client_surfaces")
    op.drop_table("d2c_published_client_surfaces")

    op.drop_index("ix_d2c_cp_track_event", table_name="d2c_client_tracking_policies")
    op.drop_index("ix_d2c_cp_track_target", table_name="d2c_client_tracking_policies")
    op.drop_table("d2c_client_tracking_policies")
    op.drop_index("ix_d2c_cp_actions_type", table_name="d2c_client_action_policies")
    op.drop_index("ix_d2c_cp_actions_target", table_name="d2c_client_action_policies")
    op.drop_table("d2c_client_action_policies")
    op.drop_index("ix_d2c_cp_vis_window", table_name="d2c_client_visibility_rules")
    op.drop_index("ix_d2c_cp_vis_target", table_name="d2c_client_visibility_rules")
    op.drop_table("d2c_client_visibility_rules")
    op.drop_index("ix_d2c_cp_bindings_source", table_name="d2c_client_data_bindings")
    op.drop_index("ix_d2c_cp_bindings_target", table_name="d2c_client_data_bindings")
    op.drop_table("d2c_client_data_bindings")
    op.drop_index("ix_d2c_cp_surfaces_type", table_name="d2c_client_surfaces")
    op.drop_table("d2c_client_surfaces")
