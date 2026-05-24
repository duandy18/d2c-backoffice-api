from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.backoffice.catalog import router as backoffice_catalog_router
from app.api.routes.backoffice.pages import router as backoffice_pages_router
from app.api.routes.backoffice.promotions import router as backoffice_promotions_router
from app.api.routes.system.health import router as system_health_router

api_router = APIRouter()
api_router.include_router(backoffice_promotions_router)
api_router.include_router(backoffice_catalog_router)
api_router.include_router(backoffice_pages_router)
api_router.include_router(system_health_router)
