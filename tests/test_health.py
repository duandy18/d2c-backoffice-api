from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_system_health_returns_backoffice_identity() -> None:
    client = TestClient(app)

    response = client.get("/system/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app_code": "d2c-backoffice",
        "service": "d2c-backoffice-api",
        "service_client_code": "d2c-backoffice-service",
        "api_path": "/api/d2c-backoffice",
        "web_path": "/backoffice",
    }
