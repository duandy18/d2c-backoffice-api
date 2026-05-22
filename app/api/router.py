from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.system.health import router as system_health_router

api_router = APIRouter()
api_router.include_router(system_health_router)
