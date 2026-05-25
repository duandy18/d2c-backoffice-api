from __future__ import annotations

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.core.config import load_settings
from app.core.database import Base
from app.domains.backoffice_pages.models.backoffice_page import BackofficePage  # noqa: F401
from app.domains.groups.models.group import Group  # noqa: F401
from app.domains.listing.models.listing import (  # noqa: F401
    ProductListingConfig,
    ProductListingContent,
    ProductListingMedia,
    SkuListingConfig,
    StorefrontCategory,
    StorefrontCategoryBinding,
)
from app.domains.offers.models.offer import (  # noqa: F401
    Offer,
    OfferComponent,
    OfferPosition,
    OfferPrice,
)
from app.domains.pms_projection.models import (  # noqa: F401
    PmsBarcodeProjection,
    PmsBrandAssetProjection,
    PmsBrandProfileProjection,
    PmsDisplayCategoryProjection,
    PmsItemAssetProjection,
    PmsItemContentProjection,
    PmsItemDisplayCategoryBindingProjection,
    PmsProductProjection,
    PmsProjectionSyncRun,
    PmsSkuCodeProjection,
    PmsUnitProjection,
)
from app.domains.pricing.models.price_config import PriceConfig  # noqa: F401
from app.domains.promotions.models.promotion_rule import (  # noqa: F401
    Coupon,
    PromotionRule,
    PromotionTarget,
)
from app.domains.publish.models.publish_version import PublishVersion  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = load_settings()
config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
