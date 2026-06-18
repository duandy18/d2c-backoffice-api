"""raise home main region max blocks

Revision ID: 0034_home_main_max
Revises: 0033_customer_service_pages
Create Date: 2026-05-29
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

revision: str = "0034_home_main_max"
down_revision: str | Sequence[str] | None = "0033_customer_service_pages"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Allow the seeded PC Web home main region to remain publishable.

    The current seed and authoring tests can create more than the original
    home.main max_blocks=20 limit. This migration raises only the home.main
    capacity, preserving validation semantics for all other regions.
    """

    op.execute(
        """
        UPDATE d2c_client_regions
        SET max_blocks = GREATEST(COALESCE(max_blocks, 0), 40),
            updated_at = now()
        WHERE region_code = 'home.main'
        """
    )


def downgrade() -> None:
    """Restore the original home.main seed capacity."""

    op.execute(
        """
        UPDATE d2c_client_regions
        SET max_blocks = 20,
            updated_at = now()
        WHERE region_code = 'home.main'
          AND max_blocks = 40
        """
    )
