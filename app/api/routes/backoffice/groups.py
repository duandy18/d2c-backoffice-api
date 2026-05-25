"""Backoffice group routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.groups.contracts.group_contract import (
    BackofficeGroupContract,
    BackofficeGroupCreateRequest,
    BackofficeGroupsResponse,
)
from app.domains.groups.services.group_service import (
    BackofficeGroupDuplicateCodeError,
    create_backoffice_group,
    get_backoffice_groups,
)

router = APIRouter(prefix="/backoffice/groups", tags=["backoffice-groups"])
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


@router.get("", response_model=BackofficeGroupsResponse)
def backoffice_groups_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeGroupsResponse:
    return get_backoffice_groups(session)


@router.post("", response_model=BackofficeGroupContract, status_code=status.HTTP_201_CREATED)
def backoffice_groups_create(
    payload: BackofficeGroupCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeGroupContract:
    try:
        return create_backoffice_group(session, payload)
    except BackofficeGroupDuplicateCodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
