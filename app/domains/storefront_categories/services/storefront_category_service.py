"""Backoffice storefront category services."""

from sqlalchemy.orm import Session

from app.domains.listing.models.listing import StorefrontCategory, StorefrontCategoryBinding
from app.domains.storefront_categories.contracts.storefront_category_contract import (
    StorefrontCategoriesResponse,
    StorefrontCategoryBindingContract,
    StorefrontCategoryBindingsResponse,
    StorefrontCategoryContract,
    StorefrontCategoryHealthResponse,
)
from app.domains.storefront_categories.repos.storefront_category_repo import (
    list_storefront_categories,
    list_storefront_category_bindings,
)


def get_storefront_category_health() -> StorefrontCategoryHealthResponse:
    return StorefrontCategoryHealthResponse(
        status="ok",
        module="storefront_categories",
        surface="merchant_management",
    )


def _build_category(row: StorefrontCategory) -> StorefrontCategoryContract:
    return StorefrontCategoryContract(
        id=row.id,
        category_code=row.category_code,
        category_name=row.category_name,
        parent_category_id=row.parent_category_id,
        level=row.level,
        display_status=row.display_status,
        sort_order=row.sort_order,
        image_url=row.image_url,
        description=row.description,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def get_storefront_categories(session: Session) -> StorefrontCategoriesResponse:
    rows = [_build_category(row) for row in list_storefront_categories(session)]
    return StorefrontCategoriesResponse(count=len(rows), categories=rows)


def _build_binding(row: StorefrontCategoryBinding) -> StorefrontCategoryBindingContract:
    return StorefrontCategoryBindingContract(
        id=row.id,
        product_listing_config_id=row.product_listing_config_id,
        storefront_category_id=row.storefront_category_id,
        is_primary=row.is_primary,
        sort_order=row.sort_order,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def get_storefront_category_bindings(session: Session) -> StorefrontCategoryBindingsResponse:
    rows = [_build_binding(row) for row in list_storefront_category_bindings(session)]
    return StorefrontCategoryBindingsResponse(count=len(rows), bindings=rows)
