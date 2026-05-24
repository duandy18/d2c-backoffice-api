"""Backoffice storefront category repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.listing.models.listing import StorefrontCategory, StorefrontCategoryBinding


def list_storefront_categories(session: Session) -> list[StorefrontCategory]:
    statement = select(StorefrontCategory).order_by(
        StorefrontCategory.level,
        StorefrontCategory.sort_order,
        StorefrontCategory.id,
    )
    return list(session.scalars(statement).all())


def list_storefront_category_bindings(session: Session) -> list[StorefrontCategoryBinding]:
    statement = select(StorefrontCategoryBinding).order_by(
        StorefrontCategoryBinding.storefront_category_id,
        StorefrontCategoryBinding.sort_order,
        StorefrontCategoryBinding.id,
    )
    return list(session.scalars(statement).all())
