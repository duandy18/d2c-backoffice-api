"""add_client_presentation_foundation.

Revision ID: 0022_client_found
Revises: 0021_client_pres
Create Date: 2026-05-25
"""

from __future__ import annotations

import json
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0022_client_found"
down_revision: str | Sequence[str] | None = "0021_client_pres"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


PAGE_ROWS = [
    {
        "page_code": "home",
        "page_type": "home",
        "route_path": "/",
        "title": "首页",
        "description": "顾客端商城首页",
        "seo_title": "D2C 商城首页",
        "seo_description": "D2C customer storefront home page",
        "sort_order": 10,
        "display_status": "visible",
        "is_active": True,
        "source_type": "seed",
        "source_ref": "client_presentation_foundation",
    },
    {
        "page_code": "category",
        "page_type": "category",
        "route_path": "/category/:group_code",
        "title": "分类页",
        "description": "顾客端分类/经营分组页面",
        "seo_title": "商品分类",
        "seo_description": "D2C customer category page",
        "sort_order": 20,
        "display_status": "visible",
        "is_active": True,
        "source_type": "seed",
        "source_ref": "client_presentation_foundation",
    },
    {
        "page_code": "product_detail",
        "page_type": "product_detail",
        "route_path": "/products/:offer_code",
        "title": "商品详情页",
        "description": "顾客端 Offer 商品详情页",
        "seo_title": "商品详情",
        "seo_description": "D2C customer product detail page",
        "sort_order": 30,
        "display_status": "visible",
        "is_active": True,
        "source_type": "seed",
        "source_ref": "client_presentation_foundation",
    },
    {
        "page_code": "search",
        "page_type": "search",
        "route_path": "/search",
        "title": "搜索页",
        "description": "顾客端搜索结果页",
        "seo_title": "搜索商品",
        "seo_description": "D2C customer search page",
        "sort_order": 40,
        "display_status": "visible",
        "is_active": True,
        "source_type": "seed",
        "source_ref": "client_presentation_foundation",
    },
    {
        "page_code": "campaign",
        "page_type": "campaign",
        "route_path": "/campaign/:campaign_code",
        "title": "专题活动页",
        "description": "顾客端专题/活动落地页",
        "seo_title": "专题活动",
        "seo_description": "D2C campaign landing page",
        "sort_order": 50,
        "display_status": "visible",
        "is_active": True,
        "source_type": "seed",
        "source_ref": "client_presentation_foundation",
    },
]

REGION_ROWS = [
    {
        "page_code": "home",
        "region_code": "home.hero",
        "region_type": "hero",
        "title": "首页头图区域",
        "description": "首页首屏主视觉",
        "sort_order": 10,
        "is_required": True,
        "max_blocks": 3,
        "allowed_block_types": ["hero_banner", "promo_strip"],
    },
    {
        "page_code": "home",
        "region_code": "home.quick_nav",
        "region_type": "navigation",
        "title": "首页快捷导航",
        "description": "首页分类/快捷入口",
        "sort_order": 20,
        "is_required": False,
        "max_blocks": 2,
        "allowed_block_types": ["category_nav", "image_grid"],
    },
    {
        "page_code": "home",
        "region_code": "home.main",
        "region_type": "main",
        "title": "首页主体区域",
        "description": "首页主商品货架",
        "sort_order": 30,
        "is_required": True,
        "max_blocks": 20,
        "allowed_block_types": ["offer_shelf", "ranking_list", "promo_strip"],
    },
    {
        "page_code": "home",
        "region_code": "home.recommendation",
        "region_type": "recommendation",
        "title": "首页推荐区域",
        "description": "猜你喜欢/推荐商品",
        "sort_order": 40,
        "is_required": False,
        "max_blocks": 8,
        "allowed_block_types": ["product_recommendation", "offer_shelf"],
    },
    {
        "page_code": "category",
        "region_code": "category.header",
        "region_type": "header",
        "title": "分类页头部",
        "description": "分类标题、说明和运营头图",
        "sort_order": 10,
        "is_required": True,
        "max_blocks": 3,
        "allowed_block_types": ["hero_banner", "promo_strip"],
    },
    {
        "page_code": "category",
        "region_code": "category.main",
        "region_type": "main",
        "title": "分类页主体",
        "description": "分类页商品列表/货架",
        "sort_order": 20,
        "is_required": True,
        "max_blocks": 20,
        "allowed_block_types": ["offer_shelf", "ranking_list"],
    },
    {
        "page_code": "product_detail",
        "region_code": "product.hero",
        "region_type": "product_hero",
        "title": "商品详情核心区域",
        "description": "商品图片、标题、价格、购买操作",
        "sort_order": 10,
        "is_required": True,
        "max_blocks": 4,
        "allowed_block_types": ["product_summary", "promo_strip"],
    },
    {
        "page_code": "product_detail",
        "region_code": "product.recommendation",
        "region_type": "recommendation",
        "title": "商品详情推荐区域",
        "description": "相关商品/搭配推荐",
        "sort_order": 40,
        "is_required": False,
        "max_blocks": 8,
        "allowed_block_types": ["product_recommendation", "offer_shelf"],
    },
]

BLOCK_TYPE_ROWS = [
    {
        "block_type": "hero_banner",
        "display_name": "头图 Banner",
        "description": "页面主视觉 Banner",
        "renderer_key": "storefront.hero_banner",
        "allowed_region_types": ["hero", "header"],
        "allowed_content_types": ["image", "campaign", "link"],
        "layout_schema": {
            "required": ["image_ratio"],
            "properties": {"image_ratio": ["16:9", "4:3"]},
        },
        "slot_schema": {"slots": ["title", "subtitle", "image_url", "target_url"]},
        "action_schema": {"actions": ["open_link", "open_page"]},
        "analytics_schema": {"events": ["impression", "click"]},
    },
    {
        "block_type": "promo_strip",
        "display_name": "促销条",
        "description": "轻量促销信息条",
        "renderer_key": "storefront.promo_strip",
        "allowed_region_types": ["hero", "header", "main"],
        "allowed_content_types": ["promotion", "coupon", "text"],
        "layout_schema": {
            "required": ["density"],
            "properties": {"density": ["compact", "standard"]},
        },
        "slot_schema": {"slots": ["badge", "title", "subtitle", "target_url"]},
        "action_schema": {"actions": ["open_link", "claim_coupon"]},
        "analytics_schema": {"events": ["impression", "click", "claim"]},
    },
    {
        "block_type": "category_nav",
        "display_name": "分类导航",
        "description": "顾客端分类/经营分组入口",
        "renderer_key": "storefront.category_nav",
        "allowed_region_types": ["navigation", "main"],
        "allowed_content_types": ["group"],
        "layout_schema": {"required": ["columns_mobile"], "properties": {"columns_mobile": [2, 4]}},
        "slot_schema": {"slots": ["groups"]},
        "action_schema": {"actions": ["open_category"]},
        "analytics_schema": {"events": ["impression", "click"]},
    },
    {
        "block_type": "offer_shelf",
        "display_name": "商品货架",
        "description": "由 Section / SectionPosition 支撑的商品货架",
        "renderer_key": "storefront.offer_shelf",
        "allowed_region_types": ["main", "recommendation"],
        "allowed_content_types": ["offer"],
        "layout_schema": {
            "required": ["display_type", "columns_desktop", "columns_tablet", "columns_mobile"],
            "properties": {"display_type": ["featured_grid", "product_grid", "horizontal_scroll"]},
        },
        "slot_schema": {"slots": ["positions"]},
        "action_schema": {"actions": ["open_offer", "add_to_cart"]},
        "analytics_schema": {"events": ["impression", "click", "add_to_cart"]},
    },
    {
        "block_type": "ranking_list",
        "display_name": "排行列表",
        "description": "热销、好评、新品排行",
        "renderer_key": "storefront.ranking_list",
        "allowed_region_types": ["main", "recommendation"],
        "allowed_content_types": ["offer"],
        "layout_schema": {
            "required": ["rank_type"],
            "properties": {"rank_type": ["sales", "review", "new"]},
        },
        "slot_schema": {"slots": ["positions"]},
        "action_schema": {"actions": ["open_offer", "add_to_cart"]},
        "analytics_schema": {"events": ["impression", "click", "add_to_cart"]},
    },
    {
        "block_type": "image_grid",
        "display_name": "图片宫格",
        "description": "图文入口宫格",
        "renderer_key": "storefront.image_grid",
        "allowed_region_types": ["navigation", "main"],
        "allowed_content_types": ["image", "link", "campaign"],
        "layout_schema": {"required": ["columns_desktop", "columns_mobile"]},
        "slot_schema": {"slots": ["items"]},
        "action_schema": {"actions": ["open_link", "open_page"]},
        "analytics_schema": {"events": ["impression", "click"]},
    },
    {
        "block_type": "rich_text",
        "display_name": "富文本",
        "description": "品牌故事、说明文本、活动说明",
        "renderer_key": "storefront.rich_text",
        "allowed_region_types": ["main", "footer"],
        "allowed_content_types": ["rich_text"],
        "layout_schema": {
            "required": ["text_align"],
            "properties": {"text_align": ["left", "center"]},
        },
        "slot_schema": {"slots": ["html", "text"]},
        "action_schema": {"actions": ["open_link"]},
        "analytics_schema": {"events": ["impression"]},
    },
    {
        "block_type": "coupon_strip",
        "display_name": "优惠券条",
        "description": "优惠券领取入口",
        "renderer_key": "storefront.coupon_strip",
        "allowed_region_types": ["main", "hero"],
        "allowed_content_types": ["coupon"],
        "layout_schema": {"required": ["density"]},
        "slot_schema": {"slots": ["coupons"]},
        "action_schema": {"actions": ["claim_coupon"]},
        "analytics_schema": {"events": ["impression", "claim"]},
    },
    {
        "block_type": "product_summary",
        "display_name": "商品详情摘要",
        "description": "商品详情页核心商品展示",
        "renderer_key": "storefront.product_summary",
        "allowed_region_types": ["product_hero"],
        "allowed_content_types": ["offer"],
        "layout_schema": {"required": ["image_ratio"]},
        "slot_schema": {"slots": ["offer"]},
        "action_schema": {"actions": ["add_to_cart", "buy_now"]},
        "analytics_schema": {"events": ["impression", "add_to_cart", "checkout_start"]},
    },
    {
        "block_type": "product_recommendation",
        "display_name": "商品推荐",
        "description": "推荐引擎或规则驱动商品推荐",
        "renderer_key": "storefront.product_recommendation",
        "allowed_region_types": ["recommendation", "main"],
        "allowed_content_types": ["offer"],
        "layout_schema": {"required": ["recommendation_type"]},
        "slot_schema": {"slots": ["offers"]},
        "action_schema": {"actions": ["open_offer", "add_to_cart"]},
        "analytics_schema": {"events": ["impression", "click", "add_to_cart"]},
    },
]


def upgrade() -> None:
    op.create_table(
        "d2c_client_pages",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("page_code", sa.String(length=96), nullable=False),
        sa.Column("page_type", sa.String(length=32), nullable=False),
        sa.Column("route_path", sa.String(length=240), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("seo_title", sa.String(length=200), nullable=True),
        sa.Column("seo_description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("display_status", sa.String(length=32), server_default="visible", nullable=False),
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
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_cp_pages_sort"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("page_code", name="uq_d2c_cp_pages_code"),
        sa.UniqueConstraint("route_path", name="uq_d2c_cp_pages_route"),
    )
    op.create_index(
        "ix_d2c_cp_pages_type",
        "d2c_client_pages",
        ["page_type", "display_status", "is_active"],
    )
    op.create_index("ix_d2c_cp_pages_sort", "d2c_client_pages", ["sort_order"])

    op.create_table(
        "d2c_client_regions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("page_id", sa.BigInteger(), nullable=False),
        sa.Column("region_code", sa.String(length=120), nullable=False),
        sa.Column("region_type", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), server_default="100", nullable=False),
        sa.Column("is_required", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("max_blocks", sa.Integer(), nullable=True),
        sa.Column("allowed_block_types", sa.JSON(), nullable=True),
        sa.Column("display_status", sa.String(length=32), server_default="visible", nullable=False),
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
        sa.CheckConstraint("sort_order >= 0", name="ck_d2c_cp_regions_sort"),
        sa.CheckConstraint("max_blocks IS NULL OR max_blocks > 0", name="ck_d2c_cp_regions_max"),
        sa.ForeignKeyConstraint(["page_id"], ["d2c_client_pages.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("region_code", name="uq_d2c_cp_regions_code"),
    )
    op.create_index("ix_d2c_cp_regions_page", "d2c_client_regions", ["page_id", "sort_order"])
    op.create_index(
        "ix_d2c_cp_regions_type",
        "d2c_client_regions",
        ["region_type", "display_status", "is_active"],
    )

    op.create_table(
        "d2c_client_block_types",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("block_type", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("renderer_key", sa.String(length=160), nullable=False),
        sa.Column(
            "data_contract_version",
            sa.String(length=32),
            server_default="v1",
            nullable=False,
        ),
        sa.Column("allowed_region_types", sa.JSON(), nullable=True),
        sa.Column("allowed_content_types", sa.JSON(), nullable=True),
        sa.Column("layout_schema", sa.JSON(), nullable=True),
        sa.Column("slot_schema", sa.JSON(), nullable=True),
        sa.Column("action_schema", sa.JSON(), nullable=True),
        sa.Column("analytics_schema", sa.JSON(), nullable=True),
        sa.Column("display_status", sa.String(length=32), server_default="visible", nullable=False),
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
        sa.UniqueConstraint("block_type", name="uq_d2c_cp_block_types_code"),
        sa.UniqueConstraint("renderer_key", name="uq_d2c_cp_block_types_renderer"),
    )
    op.create_index(
        "ix_d2c_cp_block_types_status",
        "d2c_client_block_types",
        ["display_status", "is_active"],
    )

    op.create_table(
        "d2c_published_client_pages",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("page_code", sa.String(length=96), nullable=False),
        sa.Column("page_type", sa.String(length=32), nullable=False),
        sa.Column("route_path", sa.String(length=240), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("seo_title", sa.String(length=200), nullable=True),
        sa.Column("seo_description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("display_status", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_page_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publish_version", "page_code", name="uq_d2c_pub_cp_pages_code"),
    )
    op.create_index(
        "ix_d2c_pub_cp_pages_sort",
        "d2c_published_client_pages",
        ["publish_version", "sort_order"],
    )

    op.create_table(
        "d2c_published_client_regions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("page_code", sa.String(length=96), nullable=False),
        sa.Column("region_code", sa.String(length=120), nullable=False),
        sa.Column("region_type", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("is_required", sa.Boolean(), nullable=False),
        sa.Column("max_blocks", sa.Integer(), nullable=True),
        sa.Column("allowed_block_types", sa.JSON(), nullable=True),
        sa.Column("display_status", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_region_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publish_version", "region_code", name="uq_d2c_pub_cp_regions_code"),
    )
    op.create_index(
        "ix_d2c_pub_cp_regions_page",
        "d2c_published_client_regions",
        ["publish_version", "page_code", "sort_order"],
    )

    op.create_table(
        "d2c_published_client_block_types",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("publish_version", sa.String(length=64), nullable=False),
        sa.Column("block_type", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("renderer_key", sa.String(length=160), nullable=False),
        sa.Column("data_contract_version", sa.String(length=32), nullable=False),
        sa.Column("allowed_region_types", sa.JSON(), nullable=True),
        sa.Column("allowed_content_types", sa.JSON(), nullable=True),
        sa.Column("layout_schema", sa.JSON(), nullable=True),
        sa.Column("slot_schema", sa.JSON(), nullable=True),
        sa.Column("action_schema", sa.JSON(), nullable=True),
        sa.Column("analytics_schema", sa.JSON(), nullable=True),
        sa.Column("display_status", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_block_type_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publish_version", "block_type", name="uq_d2c_pub_cp_blocks_code"),
    )
    op.create_index(
        "ix_d2c_pub_cp_blocks_renderer",
        "d2c_published_client_block_types",
        ["publish_version", "renderer_key"],
    )

    page_table = sa.table(
        "d2c_client_pages",
        sa.column("page_code"),
        sa.column("page_type"),
        sa.column("route_path"),
        sa.column("title"),
        sa.column("description"),
        sa.column("seo_title"),
        sa.column("seo_description"),
        sa.column("sort_order"),
        sa.column("display_status"),
        sa.column("is_active"),
        sa.column("source_type"),
        sa.column("source_ref"),
    )
    op.bulk_insert(page_table, PAGE_ROWS)

    for row in REGION_ROWS:
        op.execute(
            sa.text(
                """
                INSERT INTO d2c_client_regions (
                    page_id,
                    region_code,
                    region_type,
                    title,
                    description,
                    sort_order,
                    is_required,
                    max_blocks,
                    allowed_block_types,
                    display_status,
                    is_active,
                    source_type,
                    source_ref
                )
                VALUES (
                    (SELECT id FROM d2c_client_pages WHERE page_code = :page_code),
                    :region_code,
                    :region_type,
                    :title,
                    :description,
                    :sort_order,
                    :is_required,
                    :max_blocks,
                    CAST(:allowed_block_types AS json),
                    'visible',
                    true,
                    'seed',
                    'client_presentation_foundation'
                )
                """
            ).bindparams(
                page_code=row["page_code"],
                region_code=row["region_code"],
                region_type=row["region_type"],
                title=row["title"],
                description=row["description"],
                sort_order=row["sort_order"],
                is_required=row["is_required"],
                max_blocks=row["max_blocks"],
                allowed_block_types=json.dumps(row["allowed_block_types"]),
            )
        )

    for row in BLOCK_TYPE_ROWS:
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
                    'client_presentation_foundation'
                )
                """
            ).bindparams(
                block_type=row["block_type"],
                display_name=row["display_name"],
                description=row["description"],
                renderer_key=row["renderer_key"],
                allowed_region_types=json.dumps(row["allowed_region_types"]),
                allowed_content_types=json.dumps(row["allowed_content_types"]),
                layout_schema=json.dumps(row["layout_schema"]),
                slot_schema=json.dumps(row["slot_schema"]),
                action_schema=json.dumps(row["action_schema"]),
                analytics_schema=json.dumps(row["analytics_schema"]),
            )
        )


def downgrade() -> None:
    op.drop_index("ix_d2c_pub_cp_blocks_renderer", table_name="d2c_published_client_block_types")
    op.drop_table("d2c_published_client_block_types")
    op.drop_index("ix_d2c_pub_cp_regions_page", table_name="d2c_published_client_regions")
    op.drop_table("d2c_published_client_regions")
    op.drop_index("ix_d2c_pub_cp_pages_sort", table_name="d2c_published_client_pages")
    op.drop_table("d2c_published_client_pages")

    op.drop_index("ix_d2c_cp_block_types_status", table_name="d2c_client_block_types")
    op.drop_table("d2c_client_block_types")
    op.drop_index("ix_d2c_cp_regions_type", table_name="d2c_client_regions")
    op.drop_index("ix_d2c_cp_regions_page", table_name="d2c_client_regions")
    op.drop_table("d2c_client_regions")
    op.drop_index("ix_d2c_cp_pages_sort", table_name="d2c_client_pages")
    op.drop_index("ix_d2c_cp_pages_type", table_name="d2c_client_pages")
    op.drop_table("d2c_client_pages")
