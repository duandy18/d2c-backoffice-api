from __future__ import annotations

from dataclasses import dataclass
from os import getenv


def _read_csv_env(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    raw_value = getenv(name)
    if raw_value is None or raw_value.strip() == "":
        return default

    return tuple(item.strip() for item in raw_value.split(",") if item.strip())


def _read_int_env(name: str, default: int) -> int:
    raw_value = getenv(name)
    if raw_value is None or raw_value.strip() == "":
        return default
    return int(raw_value)


@dataclass(frozen=True)
class D2CBackofficeSettings:
    environment: str = "local"
    app_code: str = "d2c-backoffice"
    service_name: str = "d2c-backoffice-api"
    service_client_code: str = "d2c-backoffice-service"
    api_path: str = "/api/d2c-backoffice"
    web_path: str = "/backoffice"
    api_port: int = 8026
    database_url: str = (
        "postgresql+psycopg://d2c_backoffice:d2c_backoffice@127.0.0.1:5433/"
        "d2c_backoffice"
    )
    test_database_url: str = (
        "postgresql+psycopg://d2c_backoffice:d2c_backoffice@127.0.0.1:5433/"
        "d2c_backoffice_test"
    )
    pms_api_base_url: str = "http://127.0.0.1:8005"
    pms_service_client_code: str = "d2c-backoffice-service"
    pms_projection_sync_page_limit: int = 500
    cors_allow_origins: tuple[str, ...] = (
        "http://127.0.0.1:5288",
        "http://localhost:5288",
    )


def load_settings() -> D2CBackofficeSettings:
    return D2CBackofficeSettings(
        environment=getenv("D2C_BACKOFFICE_ENVIRONMENT", D2CBackofficeSettings.environment),
        app_code=getenv("D2C_BACKOFFICE_APP_CODE", D2CBackofficeSettings.app_code),
        service_name=getenv("D2C_BACKOFFICE_SERVICE_NAME", D2CBackofficeSettings.service_name),
        service_client_code=getenv(
            "D2C_BACKOFFICE_SERVICE_CLIENT_CODE",
            D2CBackofficeSettings.service_client_code,
        ),
        api_path=getenv("D2C_BACKOFFICE_API_PATH", D2CBackofficeSettings.api_path),
        web_path=getenv("D2C_BACKOFFICE_WEB_PATH", D2CBackofficeSettings.web_path),
        api_port=int(getenv("D2C_BACKOFFICE_API_PORT", str(D2CBackofficeSettings.api_port))),
        database_url=getenv(
            "D2C_BACKOFFICE_DATABASE_URL",
            D2CBackofficeSettings.database_url,
        ),
        test_database_url=getenv(
            "D2C_BACKOFFICE_TEST_DATABASE_URL",
            D2CBackofficeSettings.test_database_url,
        ),
        pms_api_base_url=getenv(
            "D2C_BACKOFFICE_PMS_API_BASE_URL",
            D2CBackofficeSettings.pms_api_base_url,
        ),
        pms_service_client_code=getenv(
            "D2C_BACKOFFICE_PMS_SERVICE_CLIENT_CODE",
            D2CBackofficeSettings.pms_service_client_code,
        ),
        pms_projection_sync_page_limit=_read_int_env(
            "D2C_BACKOFFICE_PMS_PROJECTION_SYNC_PAGE_LIMIT",
            D2CBackofficeSettings.pms_projection_sync_page_limit,
        ),
        cors_allow_origins=_read_csv_env(
            "D2C_BACKOFFICE_CORS_ALLOW_ORIGINS",
            D2CBackofficeSettings.cors_allow_origins,
        ),
    )
