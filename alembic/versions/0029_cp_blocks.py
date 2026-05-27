"""add client region block contract

Revision ID: 0029_cp_blocks
Revises: 0028_merchant_nav
Create Date: 2026-05-27
"""

from __future__ import annotations

import json
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0029_cp_blocks"
down_revision: str | Sequence[str] | None = "0028_merchant_nav"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


PC_WEB_BLOCK_TYPES = [
    {
        "block_type": "title",
        "display_name": "页面标题",
        "description": "PC Web 页面标题内容块",
        "renderer_key": "pc_web.title",
        "allowed_region_types": ["main", "hero"],
        "allowed_content_types": ["text"],
        "layout_schema": {
            "required": ["text_align"],
            "properties": {"text_align": ["left", "center"]},
        },
        "slot_schema": {"slots": ["title", "subtitle", "description"]},
        "action_schema": {"actions": []},
        "analytics_schema": {"events": ["impression"]},
    },
    {
        "block_type": "ad_banner",
        "display_name": "广告位",
        "description": "PC Web 广告 Banner 内容块",
        "renderer_key": "pc_web.ad_banner",
        "allowed_region_types": ["hero", "main"],
        "allowed_content_types": ["image", "campaign", "link"],
        "layout_schema": {
            "required": ["image_ratio"],
            "properties": {"image_ratio": ["16:5", "16:9", "4:3"]},
        },
        "slot_schema": {"slots": ["items"]},
        "action_schema": {"actions": ["open_link", "open_page"]},
        "analytics_schema": {"events": ["impression", "click"]},
    },
    {
        "block_type": "promotion_strip",
        "display_name": "促销折扣",
        "description": "PC Web 促销 / 折扣展示内容块",
        "renderer_key": "pc_web.promotion_strip",
        "allowed_region_types": ["hero", "main"],
        "allowed_content_types": ["promotion", "coupon", "text"],
        "layout_schema": {
            "required": ["density"],
            "properties": {"density": ["compact", "standard"]},
        },
        "slot_schema": {"slots": ["promotion_code", "coupon_code", "title", "subtitle"]},
        "action_schema": {"actions": ["open_link", "claim_coupon"]},
        "analytics_schema": {"events": ["impression", "click", "claim"]},
    },
]

PC_WEB_HOME_BLOCKS = [
    {
        "region_code": "home.main",
        "block_code": "home.title.main",
        "block_type": "title",
        "title": "精选宠物好物",
        "subtitle": "为你的猫狗挑选可靠商品",
        "description": "PC Web 首页标题内容块",
        "sort_order": 10,
        "content_source_type": "manual_inline",
        "content_source_ref": None,
        "content_payload": {
            "title": "精选宠物好物",
            "subtitle": "为你的猫狗挑选可靠商品",
            "description": "每日更新热卖、促销与新品",
        },
    },
    {
        "region_code": "home.main",
        "block_code": "home.ad.main",
        "block_type": "ad_banner",
        "title": "首页广告位",
        "subtitle": "PC Web 首页主广告",
        "description": "由页面装修控制广告素材与跳转",
        "sort_order": 20,
        "content_source_type": "manual_inline",
        "content_source_ref": None,
        "content_payload": {
            "items": [
                {
                    "title": "猫砂满减活动",
                    "image_url": "https://example.test/d2c/home-ad-banner.png",
                    "alt_text": "猫砂满减活动",
                    "link_type": "campaign",
                    "link_ref": "campaign.cat_litter_2026",
                }
            ]
        },
    },
    {
        "region_code": "home.main",
        "block_code": "home.category.nav",
        "block_type": "category_nav",
        "title": "分类入口",
        "subtitle": "按商品分类快速浏览",
        "description": "分类入口由页面装修协议挂载",
        "sort_order": 30,
        "content_source_type": "data_binding",
        "content_source_ref": "binding.home.quick_nav.category_nav.groups",
        "content_payload": None,
    },
    {
        "region_code": "home.main",
        "block_code": "home.offer_shelf.cat_litter",
        "block_type": "offer_shelf",
        "title": "猫砂热卖",
        "subtitle": "精选猫砂商品货架",
        "description": "商品货架引用 storefront section 和 section positions",
        "sort_order": 40,
        "content_source_type": "data_binding",
        "content_source_ref": "binding.home.main.offer_shelf.manual",
        "content_payload": None,
    },
    {
        "region_code": "home.main",
        "block_code": "home.promotion.weekend",
        "block_type": "promotion_strip",
        "title": "周末限时折扣",
        "subtitle": "促销折扣展示位",
        "description": "促销内容由营销中心与页面装修共同支撑",
        "sort_order": 50,
        "content_source_type": "manual_inline",
        "content_source_ref": None,
        "content_payload": {
            "title": "周末限时折扣",
            "promotion_code": "promo_weekend_10off",
            "coupon_code": None,
            "link_type": "campaign",
            "link_ref": "campaign.weekend_2026",
        },
    },
]


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def upgrade() -> None:
    op.create_table(
        "d2c_client_region_blocks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("region_id", sa.BigInteger(), nullable=False),
        sa.Column("block_code", sa.String(length=120), nullable=False),
        sa.Column("block_type", sa.String(length=64), nullable=False),
        sa.Column("renderer_key", sa.String(length=160), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("subtitle", sa.String(length=240), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("display_status", sa.String(length=32), server_default="visible", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("visible_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("visible_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "content_source_type",
            sa.String(length=32),
            server_default="manual_inline",
            nullable=False,
        ),
        sa.Column("content_source_ref", sa.String(length=160), nullable=True),
        sa.Column("content_payload", sa.JSON(), nullable=True),
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
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_cp_region_blocks_sort"),
        sa.CheckConstraint(
            "visible_until IS NULL OR visible_from IS NULL OR visible_until > visible_from",
            name="ck_d2c_cp_region_blocks_range",
        ),
        sa.ForeignKeyConstraint(["region_id"], ["d2c_client_regions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("block_code", name="uq_d2c_cp_region_blocks_code"),
    )
    op.create_index(
        "ix_d2c_cp_region_blocks_region",
        "d2c_client_region_blocks",
        ["region_id", "sort_order"],
    )
    op.create_index(
        "ix_d2c_cp_region_blocks_type",
        "d2c_client_region_blocks",
        ["block_type", "display_status", "is_active"],
    )
    op.create_index(
        "ix_d2c_cp_region_blocks_renderer",
        "d2c_client_region_blocks",
        ["renderer_key"],
    )

    op.create_table(
        "d2c_published_client_region_blocks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("page_code", sa.String(length=96), nullable=False),
        sa.Column("region_code", sa.String(length=120), nullable=False),
        sa.Column("block_code", sa.String(length=120), nullable=False),
        sa.Column("block_type", sa.String(length=64), nullable=False),
        sa.Column("renderer_key", sa.String(length=160), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("subtitle", sa.String(length=240), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("display_status", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("visible_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("visible_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("content_source_type", sa.String(length=32), nullable=False),
        sa.Column("content_source_ref", sa.String(length=160), nullable=True),
        sa.Column("content_payload", sa.JSON(), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_region_block_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "publish_version", "block_code", name="uq_d2c_pub_cp_region_blocks_code"
        ),
    )
    op.create_index(
        "ix_d2c_pub_cp_region_blocks_region",
        "d2c_published_client_region_blocks",
        ["publish_version", "page_code", "region_code", "sort_order"],
    )
    op.create_index(
        "ix_d2c_pub_cp_region_blocks_renderer",
        "d2c_published_client_region_blocks",
        ["publish_version", "renderer_key"],
    )

    for row in PC_WEB_BLOCK_TYPES:
        op.execute(
            sa.text(
                """
                INSERT INTO d2c_client_block_types (
                    block_type,
                    display_name,
                    description,
                    renderer_key,
                    data_contract_version,
                    allowed_region_types,
                    allowed_content_types,
                    layout_schema,
                    slot_schema,
                    action_schema,
                    analytics_schema,
                    display_status,
                    is_active,
                    source_type,
                    source_ref
                )
                VALUES (
                    :block_type,
                    :display_name,
                    :description,
                    :renderer_key,
                    'v1',
                    CAST(:allowed_region_types AS json),
                    CAST(:allowed_content_types AS json),
                    CAST(:layout_schema AS json),
                    CAST(:slot_schema AS json),
                    CAST(:action_schema AS json),
                    CAST(:analytics_schema AS json),
                    'visible',
                    true,
                    'seed',
                    'pc_web_region_blocks'
                )
                ON CONFLICT (block_type) DO UPDATE
                SET
                    display_name = EXCLUDED.display_name,
                    description = EXCLUDED.description,
                    renderer_key = EXCLUDED.renderer_key,
                    allowed_region_types = EXCLUDED.allowed_region_types,
                    allowed_content_types = EXCLUDED.allowed_content_types,
                    layout_schema = EXCLUDED.layout_schema,
                    slot_schema = EXCLUDED.slot_schema,
                    action_schema = EXCLUDED.action_schema,
                    analytics_schema = EXCLUDED.analytics_schema,
                    updated_at = now()
                """
            ).bindparams(
                block_type=row["block_type"],
                display_name=row["display_name"],
                description=row["description"],
                renderer_key=row["renderer_key"],
                allowed_region_types=_json(row["allowed_region_types"]),
                allowed_content_types=_json(row["allowed_content_types"]),
                layout_schema=_json(row["layout_schema"]),
                slot_schema=_json(row["slot_schema"]),
                action_schema=_json(row["action_schema"]),
                analytics_schema=_json(row["analytics_schema"]),
            )
        )

    op.execute(
        sa.text(
            """
            UPDATE d2c_client_regions
            SET
                allowed_block_types = CAST(
                    '["title","ad_banner","category_nav","offer_shelf","promotion_strip","promo_strip","ranking_list"]'
                    AS json
                ),
                updated_at = now()
            WHERE region_code = 'home.main'
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE d2c_client_surfaces
            SET
                supported_renderer_keys = CAST(
                    '[
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
                      "pc_web.title",
                      "pc_web.ad_banner",
                      "pc_web.promotion_strip"
                    ]'
                    AS json
                ),
                updated_at = now()
            WHERE surface_code = 'web_desktop'
            """
        )
    )

    for row in PC_WEB_HOME_BLOCKS:
        block_type_select = (
            "(SELECT renderer_key FROM d2c_client_block_types WHERE block_type = :block_type)"
        )
        op.execute(
            sa.text(
                f"""
                INSERT INTO d2c_client_region_blocks (
                    region_id,
                    block_code,
                    block_type,
                    renderer_key,
                    title,
                    subtitle,
                    description,
                    sort_order,
                    display_status,
                    is_active,
                    content_source_type,
                    content_source_ref,
                    content_payload,
                    source_type,
                    source_ref
                )
                VALUES (
                    (SELECT id FROM d2c_client_regions WHERE region_code = :region_code),
                    :block_code,
                    :block_type,
                    {block_type_select},
                    :title,
                    :subtitle,
                    :description,
                    :sort_order,
                    'visible',
                    true,
                    :content_source_type,
                    :content_source_ref,
                    CAST(:content_payload AS json),
                    'seed',
                    'pc_web_home_contract'
                )
                ON CONFLICT (block_code) DO UPDATE
                SET
                    region_id = EXCLUDED.region_id,
                    block_type = EXCLUDED.block_type,
                    renderer_key = EXCLUDED.renderer_key,
                    title = EXCLUDED.title,
                    subtitle = EXCLUDED.subtitle,
                    description = EXCLUDED.description,
                    sort_order = EXCLUDED.sort_order,
                    display_status = EXCLUDED.display_status,
                    is_active = EXCLUDED.is_active,
                    content_source_type = EXCLUDED.content_source_type,
                    content_source_ref = EXCLUDED.content_source_ref,
                    content_payload = EXCLUDED.content_payload,
                    updated_at = now()
                """
            ).bindparams(
                region_code=row["region_code"],
                block_code=row["block_code"],
                block_type=row["block_type"],
                title=row["title"],
                subtitle=row["subtitle"],
                description=row["description"],
                sort_order=row["sort_order"],
                content_source_type=row["content_source_type"],
                content_source_ref=row["content_source_ref"],
                content_payload=_json(row["content_payload"]),
            )
        )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM d2c_client_region_blocks
        WHERE source_ref = 'pc_web_home_contract'
           OR block_code IN (
             'home.title.main',
             'home.ad.main',
             'home.category.nav',
             'home.offer_shelf.cat_litter',
             'home.promotion.weekend'
           )
        """
    )
    op.execute(
        """
        DELETE FROM d2c_client_block_types
        WHERE source_ref = 'pc_web_region_blocks'
           OR block_type IN ('title', 'ad_banner', 'promotion_strip')
        """
    )
    op.drop_index(
        "ix_d2c_pub_cp_region_blocks_renderer",
        table_name="d2c_published_client_region_blocks",
    )
    op.drop_index(
        "ix_d2c_pub_cp_region_blocks_region",
        table_name="d2c_published_client_region_blocks",
    )
    op.drop_table("d2c_published_client_region_blocks")

    op.drop_index(
        "ix_d2c_cp_region_blocks_renderer",
        table_name="d2c_client_region_blocks",
    )
    op.drop_index(
        "ix_d2c_cp_region_blocks_type",
        table_name="d2c_client_region_blocks",
    )
    op.drop_index(
        "ix_d2c_cp_region_blocks_region",
        table_name="d2c_client_region_blocks",
    )
    op.drop_table("d2c_client_region_blocks")
