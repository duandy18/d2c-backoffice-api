from __future__ import annotations

from app.core.config import load_settings


def test_default_settings_are_backoffice_specific() -> None:
    settings = load_settings()

    assert settings.app_code == "d2c-backoffice"
    assert settings.service_name == "d2c-backoffice-api"
    assert settings.service_client_code == "d2c-backoffice-service"
    assert settings.api_port == 8026
    assert settings.pms_api_base_url == "http://127.0.0.1:8005"
    assert settings.pms_service_client_code == "d2c-backoffice-service"
    assert settings.pms_projection_sync_page_limit == 500
    assert settings.api_path == "/api/d2c-backoffice"
    assert settings.web_path == "/backoffice"
    assert settings.cors_allow_origins == (
        "http://127.0.0.1:5288",
        "http://localhost:5288",
    )
