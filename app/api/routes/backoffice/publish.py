"""Backoffice publish routes; HTTP paths are /backoffice/publish/*."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.publish.contracts.publish_contract import (
    BackofficePublishHealthResponse,
    PublishStorefrontRequest,
    PublishStorefrontResponse,
    PublishVersionsResponse,
)
from app.domains.publish.services.publish_service import (
    get_backoffice_publish_health,
    get_publish_versions,
)
from app.domains.published_snapshot.services.published_snapshot_service import (
    create_storefront_snapshot,
)

router = APIRouter(prefix="/backoffice/publish", tags=["backoffice-publish"])
SessionDep = Annotated[Session, Depends(get_session)]


def require_backoffice_client(
    x_backoffice_client: Annotated[str | None, Header(alias="X-Backoffice-Client")] = None,
) -> None:
    if x_backoffice_client != "d2c-backoffice":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="backoffice_client_required",
        )


BackofficeClientDep = Annotated[None, Depends(require_backoffice_client)]


@router.get("/health", response_model=BackofficePublishHealthResponse)
def backoffice_publish_health(_: BackofficeClientDep) -> BackofficePublishHealthResponse:
    return get_backoffice_publish_health()


@router.get("/versions", response_model=PublishVersionsResponse)
def backoffice_publish_versions(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PublishVersionsResponse:
    return get_publish_versions(session)


@router.post("", response_model=PublishStorefrontResponse, status_code=status.HTTP_201_CREATED)
def backoffice_publish_storefront(
    payload: PublishStorefrontRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> PublishStorefrontResponse:
    version = create_storefront_snapshot(
        session,
        publish_version=payload.publish_version,
        published_by=payload.published_by,
        note=payload.note,
    )
    return PublishStorefrontResponse(
        publish_version=version.publish_version,
        publish_scope=version.publish_scope,
        status=version.status,
        published_at=version.published_at,
    )
