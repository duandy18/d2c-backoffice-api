"""Backoffice publish services."""

from sqlalchemy.orm import Session

from app.domains.publish.contracts.publish_contract import (
    BackofficePublishHealthResponse,
    PublishVersionContract,
    PublishVersionsResponse,
)
from app.domains.publish.models.publish_version import PublishVersion
from app.domains.publish.repos.publish_repo import list_publish_versions


def get_backoffice_publish_health() -> BackofficePublishHealthResponse:
    return BackofficePublishHealthResponse(
        status="ok",
        module="backoffice_publish",
        surface="merchant_management",
    )


def _build_publish_version(row: PublishVersion) -> PublishVersionContract:
    return PublishVersionContract(
        id=row.id,
        publish_version=row.publish_version,
        publish_scope=row.publish_scope,
        status=row.status,
        source=row.source,
        started_at=row.started_at,
        published_at=row.published_at,
        published_by=row.published_by,
        note=row.note,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def get_publish_versions(session: Session) -> PublishVersionsResponse:
    rows = [_build_publish_version(row) for row in list_publish_versions(session)]
    return PublishVersionsResponse(count=len(rows), publish_versions=rows)
