from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.parametrize(
    "origin",
    [
        "http://127.0.0.1:5288",
        "http://localhost:5288",
    ],
)
def test_backoffice_web_origins_can_preflight_health(origin: str) -> None:
    client = TestClient(app)

    response = client.options(
        "/system/health",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin


@pytest.mark.parametrize(
    "origin",
    [
        "http://127.0.0.1:5277",
        "http://localhost:5277",
        "http://127.0.0.1:5177",
        "http://localhost:5177",
        "http://127.0.0.1:5178",
        "http://localhost:5178",
    ],
)
def test_storefront_and_retired_origins_are_not_allowed(origin: str) -> None:
    client = TestClient(app)

    response = client.options(
        "/system/health",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
        },
    )

    assert "access-control-allow-origin" not in response.headers
