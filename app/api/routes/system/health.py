from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import load_settings

router = APIRouter(prefix="/system", tags=["system"])


class HealthResponse(BaseModel):
    status: str
    app_code: str
    service: str
    service_client_code: str
    api_path: str
    web_path: str


@router.get("/health", response_model=HealthResponse)
def system_health() -> HealthResponse:
    settings = load_settings()
    return HealthResponse(
        status="ok",
        app_code=settings.app_code,
        service=settings.service_name,
        service_client_code=settings.service_client_code,
        api_path=settings.api_path,
        web_path=settings.web_path,
    )
