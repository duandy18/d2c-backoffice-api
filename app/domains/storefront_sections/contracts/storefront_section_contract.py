"""Backoffice storefront section API contracts."""

from datetime import datetime

from pydantic import BaseModel, Field


class BackofficeStorefrontSectionCreateRequest(BaseModel):
    section_code: str = Field(..., min_length=1, max_length=96)
    section_type: str = Field(default="offer_shelf", min_length=1, max_length=32)
    group_code: str | None = Field(default=None, max_length=96)
    title: str = Field(..., min_length=1, max_length=160)
    subtitle: str | None = Field(default=None, max_length=240)
    description: str | None = None
    sort_order: int = Field(default=100, ge=0)
    display_status: str = Field(default="visible", min_length=1, max_length=32)
    is_active: bool = True
    source_type: str = Field(default="manual", min_length=1, max_length=32)
    source_ref: str | None = Field(default=None, max_length=160)


class BackofficeStorefrontSection(BaseModel):
    id: int
    section_code: str
    section_type: str
    group_id: int | None
    group_code: str | None
    title: str
    subtitle: str | None
    description: str | None
    sort_order: int
    display_status: str
    is_active: bool
    source_type: str
    source_ref: str | None
    created_at: datetime
    updated_at: datetime


class BackofficeStorefrontSectionsResponse(BaseModel):
    count: int = Field(..., ge=0)
    sections: list[BackofficeStorefrontSection]


class BackofficeStorefrontSectionLayoutUpsertRequest(BaseModel):
    display_type: str = Field(default="product_grid", min_length=1, max_length=32)
    columns_desktop: int = Field(default=4, ge=1)
    columns_tablet: int = Field(default=2, ge=1)
    columns_mobile: int = Field(default=1, ge=1)
    card_size: str = Field(default="standard", min_length=1, max_length=32)
    image_ratio: str = Field(default="1:1", min_length=1, max_length=16)
    show_promotion_badge: bool = True
    show_sales_summary: bool = True
    show_review_summary: bool = True
    show_compare_price: bool = True
    show_quantity_stepper: bool = True
    max_items: int | None = Field(default=None, ge=1)


class BackofficeStorefrontSectionLayout(BaseModel):
    id: int
    section_id: int
    section_code: str
    display_type: str
    columns_desktop: int
    columns_tablet: int
    columns_mobile: int
    card_size: str
    image_ratio: str
    show_promotion_badge: bool
    show_sales_summary: bool
    show_review_summary: bool
    show_compare_price: bool
    show_quantity_stepper: bool
    max_items: int | None
    created_at: datetime
    updated_at: datetime


class BackofficeStorefrontSectionsHealthResponse(BaseModel):
    status: str
    module: str
    owner_tables: list[str]
