from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.backoffice.catalog import router as backoffice_catalog_router
from app.api.routes.backoffice.listing import router as backoffice_listing_router
from app.api.routes.backoffice.pages import router as backoffice_pages_router
from app.api.routes.backoffice.pms_projection import router as backoffice_pms_projection_router
from app.api.routes.backoffice.pricing import router as backoffice_pricing_router
from app.api.routes.backoffice.promotions import router as backoffice_promotions_router
from app.api.routes.backoffice.publish import router as backoffice_publish_router
from app.api.routes.backoffice.published_export import router as backoffice_published_export_router
from app.api.routes.backoffice.storefront_categories import (
    router as backoffice_storefront_categories_router,
)
from app.api.routes.system.health import router as system_health_router

api_router = APIRouter()
api_router.include_router(backoffice_promotions_router)
api_router.include_router(backoffice_pricing_router)
api_router.include_router(backoffice_listing_router)
api_router.include_router(backoffice_storefront_categories_router)
api_router.include_router(backoffice_pms_projection_router)
api_router.include_router(backoffice_publish_router)
api_router.include_router(backoffice_published_export_router)
api_router.include_router(backoffice_catalog_router)
api_router.include_router(backoffice_pages_router)
api_router.include_router(system_health_router)
