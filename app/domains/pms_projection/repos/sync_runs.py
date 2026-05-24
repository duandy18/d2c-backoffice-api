"""PMS projection sync run repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.pms_projection.models.sync_runs import PmsProjectionSyncRun


def list_projection_sync_runs(session: Session) -> list[PmsProjectionSyncRun]:
    statement = select(PmsProjectionSyncRun).order_by(PmsProjectionSyncRun.id.desc())
    return list(session.scalars(statement).all())


__all__ = ["list_projection_sync_runs"]
