"""Backoffice storefront category API contracts."""

from datetime import datetime

from pydantic import BaseModel, Field


class StorefrontCategoryHealthResponse(BaseModel):
    status: str
    module: str
    surface: str


class StorefrontCategoryContract(BaseModel):
    id: int
    category_code: str
    category_name: str
    parent_category_id: int | None
    level: int
    display_status: str
    sort_order: int
    image_url: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime


class StorefrontCategoriesResponse(BaseModel):
    count: int = Field(..., ge=0)
    categories: list[StorefrontCategoryContract]


class StorefrontCategoryBindingContract(BaseModel):
    id: int
    product_listing_config_id: int
    storefront_category_id: int
    is_primary: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime


class StorefrontCategoryBindingsResponse(BaseModel):
    count: int = Field(..., ge=0)
    bindings: list[StorefrontCategoryBindingContract]
