"""Backoffice publish repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.publish.models.publish_version import PublishVersion


def list_publish_versions(session: Session) -> list[PublishVersion]:
    statement = select(PublishVersion).order_by(PublishVersion.id.desc())
    return list(session.scalars(statement).all())
