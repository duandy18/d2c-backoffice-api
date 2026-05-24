"""PMS projection health service."""

from app.domains.pms_projection.contracts.health import PmsProjectionHealthResponse


def get_pms_projection_health() -> PmsProjectionHealthResponse:
    return PmsProjectionHealthResponse(
        status="ok",
        module="pms_projection",
        surface="merchant_read",
    )


__all__ = ["get_pms_projection_health"]
