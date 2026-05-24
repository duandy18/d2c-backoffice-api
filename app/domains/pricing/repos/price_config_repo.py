"""Backoffice pricing repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pricing.models.price_config import PriceConfig


def list_price_configs(session: Session) -> list[PriceConfig]:
    statement = select(PriceConfig).order_by(
        PriceConfig.is_active.desc(),
        PriceConfig.priority,
        PriceConfig.id,
    )
    return list(session.scalars(statement).all())
