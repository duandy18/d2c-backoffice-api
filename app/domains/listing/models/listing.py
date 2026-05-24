"""D2C merchant listing configuration ORM models.

Listing configs are D2C-owned merchant decisions. They reference PMS projection
identity but do not own PMS product master data.

Content and media are split from listing identity so merchant display copy and
image ordering can evolve without turning the listing config row into a mixed
owner table.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProductListingConfig(Base):
    __tablename__ = "d2c_product_listing_configs"
    __table_args__ = (
        UniqueConstraint("pms_item_id", name="uq_d2c_product_listing_configs_pms_item_id"),
        UniqueConstraint("listing_code", name="uq_d2c_product_listing_configs_listing_code"),
        CheckConstraint(
            "sort_order >= 0",
            name="ck_d2c_product_listing_configs_sort_order_non_negative",
        ),
        CheckConstraint(
            "visible_until IS NULL OR visible_from IS NULL OR visible_until > visible_from",
            name="ck_d2c_product_listing_configs_visible_range_valid",
        ),
        Index(
            "ix_d2c_product_listing_configs_status",
            "listing_status",
            "display_status",
            "sell_status",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pms_item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_product_projection.pms_item_id", ondelete="RESTRICT"),
        nullable=False,
    )
    pms_sku: Mapped[str] = mapped_column(String(128), nullable=False)
    listing_code: Mapped[str] = mapped_column(String(96), nullable=False)
    listing_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="draft",
        server_default="draft",
    )
    display_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="hidden",
        server_default="hidden",
    )
    sell_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="not_sellable",
        server_default="not_sellable",
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    visible_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    visible_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class ProductListingContent(Base):
    __tablename__ = "d2c_product_listing_contents"
    __table_args__ = (
        UniqueConstraint(
            "product_listing_config_id",
            name="uq_d2c_product_listing_contents_product",
        ),
        Index("ix_d2c_product_listing_contents_status", "content_status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_listing_config_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_product_listing_configs.id", ondelete="CASCADE"),
        nullable=False,
    )
    display_title: Mapped[str] = mapped_column(String(200), nullable=False)
    subtitle: Mapped[str | None] = mapped_column(String(240), nullable=True)
    short_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    detail_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    seo_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    seo_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    selling_points: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    content_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="active",
        server_default="active",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class ProductListingMedia(Base):
    __tablename__ = "d2c_product_listing_media"
    __table_args__ = (
        CheckConstraint(
            "object_key IS NOT NULL OR url IS NOT NULL",
            name="ck_d2c_product_listing_media_location_present",
        ),
        CheckConstraint(
            "sort_order >= 0",
            name="ck_d2c_product_listing_media_sort_order_non_negative",
        ),
        Index("ix_d2c_product_listing_media_product", "product_listing_config_id"),
        Index(
            "ix_d2c_product_listing_media_usage_primary",
            "product_listing_config_id",
            "usage_type",
            "is_primary",
            "status",
        ),
        Index(
            "ix_d2c_product_listing_media_sort",
            "product_listing_config_id",
            "usage_type",
            "sort_order",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_listing_config_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_product_listing_configs.id", ondelete="CASCADE"),
        nullable=False,
    )
    media_type: Mapped[str] = mapped_column(String(32), nullable=False)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False)
    pms_asset_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    object_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    alt_text: Mapped[str | None] = mapped_column(String(240), nullable=True)
    usage_type: Mapped[str] = mapped_column(String(32), nullable=False)
    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
        server_default="100",
    )
    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="active",
        server_default="active",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class SkuListingConfig(Base):
    __tablename__ = "d2c_sku_listing_configs"
    __table_args__ = (
        UniqueConstraint(
            "pms_sku_code_id",
            "pms_item_uom_id",
            name="uq_d2c_sku_listing_configs_sku_code_uom",
        ),
        CheckConstraint(
            "sort_order >= 0",
            name="ck_d2c_sku_listing_configs_sort_order_non_negative",
        ),
        CheckConstraint(
            "visible_until IS NULL OR visible_from IS NULL OR visible_until > visible_from",
            name="ck_d2c_sku_listing_configs_visible_range_valid",
        ),
        Index("ix_d2c_sku_listing_configs_product", "product_listing_config_id"),
        Index(
            "ix_d2c_sku_listing_configs_status",
            "listing_status",
            "display_status",
            "sell_status",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_listing_config_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_product_listing_configs.id", ondelete="CASCADE"),
        nullable=False,
    )
    pms_item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_product_projection.pms_item_id", ondelete="RESTRICT"),
        nullable=False,
    )
    pms_sku_code_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_sku_code_projection.pms_sku_code_id", ondelete="RESTRICT"),
        nullable=False,
    )
    pms_item_uom_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_unit_projection.pms_item_uom_id", ondelete="RESTRICT"),
        nullable=False,
    )
    pms_barcode_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("d2c_pms_barcode_projection.pms_barcode_id", ondelete="SET NULL"),
        nullable=True,
    )
    sku_display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    sku_spec_text: Mapped[str | None] = mapped_column(String(240), nullable=True)
    listing_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="draft",
        server_default="draft",
    )
    display_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="hidden",
        server_default="hidden",
    )
    sell_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="not_sellable",
        server_default="not_sellable",
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    visible_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    visible_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class StorefrontCategory(Base):
    __tablename__ = "d2c_storefront_categories"
    __table_args__ = (
        UniqueConstraint("category_code", name="uq_d2c_storefront_categories_code"),
        CheckConstraint("level >= 1", name="ck_d2c_storefront_categories_level_positive"),
        CheckConstraint(
            "sort_order >= 0",
            name="ck_d2c_storefront_categories_sort_order_non_negative",
        ),
        Index("ix_d2c_storefront_categories_parent", "parent_category_id"),
        Index("ix_d2c_storefront_categories_display_status", "display_status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    category_code: Mapped[str] = mapped_column(String(96), nullable=False)
    category_name: Mapped[str] = mapped_column(String(160), nullable=False)
    parent_category_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("d2c_storefront_categories.id", ondelete="RESTRICT"),
        nullable=True,
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")
    display_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="hidden",
        server_default="hidden",
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class StorefrontCategoryBinding(Base):
    __tablename__ = "d2c_storefront_category_bindings"
    __table_args__ = (
        UniqueConstraint(
            "product_listing_config_id",
            "storefront_category_id",
            name="uq_d2c_storefront_category_bindings_product_category",
        ),
        CheckConstraint(
            "sort_order >= 0",
            name="ck_d2c_storefront_category_bindings_sort_order_non_negative",
        ),
        Index("ix_d2c_storefront_category_bindings_product", "product_listing_config_id"),
        Index("ix_d2c_storefront_category_bindings_category", "storefront_category_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_listing_config_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_product_listing_configs.id", ondelete="CASCADE"),
        nullable=False,
    )
    storefront_category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("d2c_storefront_categories.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
