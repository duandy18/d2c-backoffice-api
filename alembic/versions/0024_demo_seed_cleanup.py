"""clean_demo_seed_data.

Revision ID: 0024_demo_seed
Revises: 0023_client_proto
Create Date: 2026-05-26
"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op

revision: str = "0024_demo_seed"
down_revision: str | Sequence[str] | None = "0023_client_proto"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Clean engineering verification rows and normalize storefront demo seed data."""

    # 1) Remove client-presentation verification owner rows.
    # Delete children first where there is a page FK, then delete the verify page.
    op.execute(
        """
        DELETE FROM d2c_client_regions
        WHERE source_type = 'verify'
           OR region_code LIKE 'verify-%'
        """
    )
    op.execute(
        """
        DELETE FROM d2c_client_pages
        WHERE source_type = 'verify'
           OR page_code LIKE 'verify-%'
        """
    )
    op.execute(
        """
        DELETE FROM d2c_client_block_types
        WHERE source_type = 'verify'
           OR block_type LIKE 'verify_%'
           OR renderer_key LIKE 'storefront.verify_%'
        """
    )
    op.execute(
        """
        DELETE FROM d2c_client_surfaces
        WHERE source_type = 'verify'
           OR surface_code LIKE 'verify-%'
        """
    )
    op.execute(
        """
        DELETE FROM d2c_client_data_bindings
        WHERE source_type = 'verify'
           OR binding_code LIKE 'verify-%'
        """
    )
    op.execute(
        """
        DELETE FROM d2c_client_visibility_rules
        WHERE source_type = 'verify'
           OR rule_code LIKE 'verify-%'
        """
    )
    op.execute(
        """
        DELETE FROM d2c_client_action_policies
        WHERE source_type = 'verify'
           OR policy_code LIKE 'verify-%'
        """
    )
    op.execute(
        """
        DELETE FROM d2c_client_tracking_policies
        WHERE source_type = 'verify'
           OR policy_code LIKE 'verify-%'
        """
    )

    # 2) Remove engineering-only storefront demo rows.
    # These rows were useful for wiring verification but should not remain as public demo content.
    op.execute(
        """
        DELETE FROM d2c_storefront_section_positions sp
        USING d2c_storefront_sections s
        WHERE sp.section_id = s.id
          AND s.section_code IN (
            'section-real-sec-pos-80a55d0b',
            'section-ui-smoke-b9797c93'
          )
        """
    )
    op.execute(
        """
        DELETE FROM d2c_storefront_section_positions sp
        USING d2c_offers o
        WHERE sp.offer_id = o.id
          AND o.offer_code IN (
            'offer-real-sec-pos-80a55d0b',
            'offer-ui-smoke-b9797c93'
          )
        """
    )
    op.execute(
        """
        DELETE FROM d2c_storefront_section_layouts sl
        USING d2c_storefront_sections s
        WHERE sl.section_id = s.id
          AND s.section_code IN (
            'section-real-sec-pos-80a55d0b',
            'section-ui-smoke-b9797c93'
          )
        """
    )
    op.execute(
        """
        DELETE FROM d2c_offer_prices pr
        USING d2c_offers o
        WHERE pr.offer_id = o.id
          AND o.offer_code IN (
            'offer-real-sec-pos-80a55d0b',
            'offer-ui-smoke-b9797c93'
          )
        """
    )
    op.execute(
        """
        DELETE FROM d2c_offers
        WHERE offer_code IN (
          'offer-real-sec-pos-80a55d0b',
          'offer-ui-smoke-b9797c93'
        )
        """
    )
    op.execute(
        """
        DELETE FROM d2c_storefront_sections
        WHERE section_code IN (
          'section-real-sec-pos-80a55d0b',
          'section-ui-smoke-b9797c93'
        )
        """
    )

    # 3) Promote the cat-litter row into a stable demo seed.
    op.execute(
        """
        UPDATE d2c_storefront_sections
        SET
          section_code = 'home.cat_litter.featured',
          title = '精选猫砂',
          subtitle = '适合日常补货的猫砂推荐',
          description = '商家后台发布的首页精选猫砂货架。',
          sort_order = 10,
          display_status = 'visible',
          is_active = true,
          source_type = 'seed',
          source_ref = 'demo_home_cat_litter'
        WHERE section_code = 'section-real-cat-litter-180406'
        """
    )
    op.execute(
        """
        UPDATE d2c_offers
        SET
          offer_code = 'offer.cat_litter.tofu_6l',
          title = '豆腐猫砂 6L',
          subtitle = '低尘除味，适合日常补货',
          description = '结团快、低粉尘，适合多猫家庭日常使用。',
          image_url = NULL,
          display_status = 'visible',
          sell_status = 'sellable',
          publish_status = 'published',
          source_type = 'seed',
          sort_order = 10
        WHERE offer_code = 'offer-real-cat-litter-180406'
        """
    )
    op.execute(
        """
        UPDATE d2c_offer_prices pr
        SET
          price_code = 'price.cat_litter.tofu_6l.usd',
          channel = 'storefront',
          currency = 'USD',
          price_cents = 1099,
          compare_at_price_cents = 1399,
          is_active = true,
          priority = 10
        FROM d2c_offers o
        WHERE pr.offer_id = o.id
          AND o.offer_code = 'offer.cat_litter.tofu_6l'
        """
    )

    # 4) Ensure the stable demo offer is actually positioned into the stable demo section.
    op.execute(
        """
        DELETE FROM d2c_storefront_section_positions sp
        USING d2c_storefront_sections s, d2c_offers o
        WHERE sp.section_id = s.id
          AND sp.offer_id = o.id
          AND s.section_code = 'home.cat_litter.featured'
          AND o.offer_code = 'offer.cat_litter.tofu_6l'
          AND sp.position_code <> 'pos.home.cat_litter.tofu_6l'
        """
    )
    op.execute(
        """
        INSERT INTO d2c_storefront_section_positions (
          section_id,
          offer_id,
          position_code,
          sort_order,
          position_type,
          is_featured,
          is_active,
          source_type,
          source_ref
        )
        SELECT
          s.id,
          o.id,
          'pos.home.cat_litter.tofu_6l',
          10,
          'manual',
          true,
          true,
          'seed',
          'demo_home_cat_litter'
        FROM d2c_storefront_sections s
        JOIN d2c_offers o
          ON o.offer_code = 'offer.cat_litter.tofu_6l'
        WHERE s.section_code = 'home.cat_litter.featured'
        ON CONFLICT (position_code) DO UPDATE
        SET
          section_id = EXCLUDED.section_id,
          offer_id = EXCLUDED.offer_id,
          sort_order = EXCLUDED.sort_order,
          position_type = EXCLUDED.position_type,
          is_featured = EXCLUDED.is_featured,
          is_active = EXCLUDED.is_active,
          source_type = EXCLUDED.source_type,
          source_ref = EXCLUDED.source_ref
        """
    )

    # 5) Normalize layout for the stable demo section.
    op.execute(
        """
        INSERT INTO d2c_storefront_section_layouts (
          section_id,
          display_type,
          columns_desktop,
          columns_tablet,
          columns_mobile,
          card_size,
          image_ratio,
          show_promotion_badge,
          show_sales_summary,
          show_review_summary,
          show_compare_price,
          show_quantity_stepper,
          max_items
        )
        SELECT
          s.id,
          'featured_grid',
          2,
          2,
          1,
          'large',
          '4:3',
          true,
          true,
          true,
          true,
          true,
          8
        FROM d2c_storefront_sections s
        WHERE s.section_code = 'home.cat_litter.featured'
        ON CONFLICT (section_id) DO UPDATE
        SET
          display_type = EXCLUDED.display_type,
          columns_desktop = EXCLUDED.columns_desktop,
          columns_tablet = EXCLUDED.columns_tablet,
          columns_mobile = EXCLUDED.columns_mobile,
          card_size = EXCLUDED.card_size,
          image_ratio = EXCLUDED.image_ratio,
          show_promotion_badge = EXCLUDED.show_promotion_badge,
          show_sales_summary = EXCLUDED.show_sales_summary,
          show_review_summary = EXCLUDED.show_review_summary,
          show_compare_price = EXCLUDED.show_compare_price,
          show_quantity_stepper = EXCLUDED.show_quantity_stepper,
          max_items = EXCLUDED.max_items
        """
    )

    # 6) Keep the demo cat-litter shelf in home.main only.
    # Recommendation blocks should be filled by a dedicated recommendation model later.
    op.execute(
        """
        UPDATE d2c_client_regions
        SET allowed_block_types = CAST('["product_recommendation"]' AS json)
        WHERE region_code = 'home.recommendation'
        """
    )



def downgrade() -> None:
    """No-op downgrade.

    This migration removes engineering verification/demo rows from local owner data.
    Reintroducing those rows on downgrade would pollute storefront demos again, so
    downgrade intentionally leaves cleaned data in place.
    """
