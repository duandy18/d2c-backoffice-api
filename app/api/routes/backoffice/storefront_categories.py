"""Backoffice storefront category routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.storefront_categories.contracts.storefront_category_contract import (
    StorefrontCategoriesResponse,
    StorefrontCategoryBindingsResponse,
    StorefrontCategoryHealthResponse,
)
from app.domains.storefront_categories.services.storefront_category_service import (
    get_storefront_categories,
    get_storefront_category_bindings,
    get_storefront_category_health,
)

router = APIRouter(
    prefix="/backoffice/storefront-categories",
    tags=["backoffice-storefront-categories"],
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


@router.get("/health", response_model=StorefrontCategoryHealthResponse)
def storefront_categories_health(_: BackofficeClientDep) -> StorefrontCategoryHealthResponse:
    return get_storefront_category_health()


@router.get("", response_model=StorefrontCategoriesResponse)
def storefront_categories_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> StorefrontCategoriesResponse:
    return get_storefront_categories(session)


@router.get("/bindings", response_model=StorefrontCategoryBindingsResponse)
def storefront_category_bindings(
    _: BackofficeClientDep,
    session: SessionDep,
) -> StorefrontCategoryBindingsResponse:
    return get_storefront_category_bindings(session)
