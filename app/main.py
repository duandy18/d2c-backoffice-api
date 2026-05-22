from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import load_settings


def create_app() -> FastAPI:
    settings = load_settings()

    app = FastAPI(
        title="D2C Backoffice API",
        description="D2C merchant backoffice API service.",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allow_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    return app


app = create_app()
