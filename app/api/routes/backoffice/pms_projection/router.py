"""Aggregate router for backoffice PMS projection routes.

The HTTP prefix remains /backoffice/pms-projections.
Concrete route behavior is split by projection table.
"""

from fastapi import APIRouter

from app.api.routes.backoffice.pms_projection import (
    barcodes,
    health,
    products,
    sku_codes,
    sync_runs,
    units,
)

router = APIRouter(prefix="/backoffice/pms-projections", tags=["backoffice-pms-projections"])

for child_router in (
    health.router,
    products.router,
    units.router,
    sku_codes.router,
    barcodes.router,
    sync_runs.router,
):
    router.include_router(child_router)


__all__ = ["router"]
