"""PMS projection sync action service."""

from sqlalchemy.orm import Session

from app.core.config import load_settings
from app.domains.pms_projection.clients.pms_projection_feed_client import PmsProjectionFeedClient
from app.domains.pms_projection.contracts.sync_actions import (
    PmsProjectionSyncScopeResponse,
)
from app.domains.pms_projection.services.pms_projection_sync_service import (
    PmsProjectionSyncService,
)


def sync_pms_projection_scope(
    session: Session,
    *,
    scope: str,
    requested_by: str = "backoffice-ui",
) -> PmsProjectionSyncScopeResponse:
    settings = load_settings()
    client = PmsProjectionFeedClient(
        base_url=settings.pms_api_base_url,
        service_client_code=settings.pms_service_client_code,
        page_limit=settings.pms_projection_sync_page_limit,
    )
    result = PmsProjectionSyncService(session=session, feed_reader=client).sync_scope(
        scope,
        requested_by=requested_by,
    )

    return PmsProjectionSyncScopeResponse(
        scope=result.scope,
        endpoint=result.endpoint,
        source_base_url=result.source_base_url,
        source_endpoint=result.source_endpoint,
        status=result.status,
        started_at=result.started_at,
        finished_at=result.finished_at,
        requested_by=result.requested_by,
        rows_fetched=result.rows_fetched,
        rows_upserted=result.rows_upserted,
        rows_deleted=result.rows_deleted,
        error_code=result.error_code,
        error_message=result.error_message,
    )


__all__ = ["sync_pms_projection_scope"]
