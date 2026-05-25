"""Backoffice client presentation routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.client_presentation.contracts.client_presentation_contract import (
    ClientPresentationBlockTypeContract,
    ClientPresentationBlockTypeCreateRequest,
    ClientPresentationBlockTypesResponse,
    ClientPresentationHealthResponse,
    ClientPresentationPageContract,
    ClientPresentationPageCreateRequest,
    ClientPresentationPagesResponse,
    ClientPresentationRegionContract,
    ClientPresentationRegionCreateRequest,
    ClientPresentationRegionsResponse,
)
from app.domains.client_presentation.services.client_presentation_service import (
    ClientPresentationDuplicateCodeError,
    ClientPresentationPageNotFoundError,
    create_client_presentation_block_type,
    create_client_presentation_page,
    create_client_presentation_region,
    get_client_presentation_block_types,
    get_client_presentation_health,
    get_client_presentation_pages,
    get_client_presentation_regions,
)

router = APIRouter(
    prefix="/backoffice/client-presentation",
    tags=["backoffice-client-presentation"],
)
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


@router.get("/health", response_model=ClientPresentationHealthResponse)
def client_presentation_health(_: BackofficeClientDep) -> ClientPresentationHealthResponse:
    return get_client_presentation_health()


@router.get("/pages", response_model=ClientPresentationPagesResponse)
def client_presentation_pages_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationPagesResponse:
    return get_client_presentation_pages(session)


@router.post(
    "/pages",
    response_model=ClientPresentationPageContract,
    status_code=status.HTTP_201_CREATED,
)
def client_presentation_pages_create(
    payload: ClientPresentationPageCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationPageContract:
    try:
        return create_client_presentation_page(session, payload)
    except ClientPresentationDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/regions", response_model=ClientPresentationRegionsResponse)
def client_presentation_regions_list(
    _: BackofficeClientDep,
    session: SessionDep,
    page_code: Annotated[str | None, Query()] = None,
) -> ClientPresentationRegionsResponse:
    try:
        return get_client_presentation_regions(session, page_code)
    except ClientPresentationPageNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "/pages/{page_code}/regions",
    response_model=ClientPresentationRegionContract,
    status_code=status.HTTP_201_CREATED,
)
def client_presentation_regions_create(
    page_code: str,
    payload: ClientPresentationRegionCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationRegionContract:
    try:
        return create_client_presentation_region(session, page_code, payload)
    except ClientPresentationPageNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ClientPresentationDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/block-types", response_model=ClientPresentationBlockTypesResponse)
def client_presentation_block_types_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationBlockTypesResponse:
    return get_client_presentation_block_types(session)


@router.post(
    "/block-types",
    response_model=ClientPresentationBlockTypeContract,
    status_code=status.HTTP_201_CREATED,
)
def client_presentation_block_types_create(
    payload: ClientPresentationBlockTypeCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationBlockTypeContract:
    try:
        return create_client_presentation_block_type(session, payload)
    except ClientPresentationDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
