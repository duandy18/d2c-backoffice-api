"""PMS brand profile projection repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.brand_profiles import PmsBrandProfileProjection


def list_brand_profile_projections(session: Session) -> list[PmsBrandProfileProjection]:
    statement = select(PmsBrandProfileProjection).order_by(
        PmsBrandProfileProjection.brand_id,
        PmsBrandProfileProjection.pms_profile_id,
    )
    return list(session.scalars(statement).all())


__all__ = ["list_brand_profile_projections"]
