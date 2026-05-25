"""Backoffice storefront section routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.storefront_sections.contracts.storefront_section_contract import (
    BackofficeStorefrontSection,
    BackofficeStorefrontSectionCreateRequest,
    BackofficeStorefrontSectionLayout,
    BackofficeStorefrontSectionLayoutUpsertRequest,
    BackofficeStorefrontSectionsHealthResponse,
    BackofficeStorefrontSectionsResponse,
)
from app.domains.storefront_sections.services.storefront_section_service import (
    BackofficeStorefrontSectionDuplicateCodeError,
    BackofficeStorefrontSectionGroupNotFoundError,
    BackofficeStorefrontSectionNotFoundError,
    create_backoffice_storefront_section,
    get_backoffice_storefront_sections,
    get_storefront_sections_health,
    upsert_backoffice_storefront_section_layout,
)

router = APIRouter(
    prefix="/backoffice/storefront-sections", tags=["backoffice-storefront-sections"]
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


@router.get("/health", response_model=BackofficeStorefrontSectionsHealthResponse)
def backoffice_storefront_sections_health(
    _: BackofficeClientDep,
) -> BackofficeStorefrontSectionsHealthResponse:
    return get_storefront_sections_health()


@router.get("", response_model=BackofficeStorefrontSectionsResponse)
def backoffice_storefront_sections_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeStorefrontSectionsResponse:
    return get_backoffice_storefront_sections(session)


@router.post("", response_model=BackofficeStorefrontSection, status_code=status.HTTP_201_CREATED)
def backoffice_storefront_sections_create(
    payload: BackofficeStorefrontSectionCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeStorefrontSection:
    try:
        return create_backoffice_storefront_section(session, payload)
    except BackofficeStorefrontSectionGroupNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BackofficeStorefrontSectionDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/{section_code}/layout", response_model=BackofficeStorefrontSectionLayout)
def backoffice_storefront_section_layout_upsert(
    section_code: str,
    payload: BackofficeStorefrontSectionLayoutUpsertRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> BackofficeStorefrontSectionLayout:
    try:
        return upsert_backoffice_storefront_section_layout(session, section_code, payload)
    except BackofficeStorefrontSectionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
