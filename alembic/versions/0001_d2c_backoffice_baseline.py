"""d2c_backoffice_baseline

Revision ID: 0001_d2c_backoffice_baseline
Revises:
Create Date: 2026-05-23
"""

from __future__ import annotations

from collections.abc import Sequence

revision: str = "0001_d2c_backoffice_baseline"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create baseline revision for the independent D2C backoffice database."""


def downgrade() -> None:
    """Downgrade baseline revision."""
