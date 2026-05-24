"""Backoffice PMS projection routes; HTTP paths are /backoffice/pms-projections/*."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.pms_projection.contracts.pms_projection_contract import (
    PmsBarcodeProjectionsResponse,
    PmsBrandAssetsProjectionResponse,
    PmsBrandProfilesProjectionResponse,
    PmsDisplayCategoriesProjectionResponse,
    PmsItemAssetsProjectionResponse,
    PmsItemContentsProjectionResponse,
    PmsItemDisplayCategoryBindingsProjectionResponse,
    PmsProductProjectionsResponse,
    PmsProjectionHealthResponse,
    PmsProjectionSyncRunsResponse,
    PmsSkuCodeProjectionsResponse,
    PmsUnitProjectionsResponse,
)
from app.domains.pms_projection.services.pms_projection_service import (
    get_pms_barcode_projections,
    get_pms_brand_asset_projections,
    get_pms_brand_profile_projections,
    get_pms_display_category_projections,
    get_pms_item_asset_projections,
    get_pms_item_content_projections,
    get_pms_item_display_category_binding_projections,
    get_pms_product_projections,
    get_pms_projection_health,
    get_pms_projection_sync_runs,
    get_pms_sku_code_projections,
    get_pms_unit_projections,
)

router = APIRouter(prefix="/backoffice/pms-projections", tags=["backoffice-pms-projections"])
SessionDep = Annotated[Session, Depends(get_session)]


def require_backoffice_client(
    x_backoffice_client: Annotated[str | None, Header(alias="X-Backoffice-Client")] = None,
) -> None:
    if x_backoffice_client != "d2c-backoffice":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="backoffice_client_required",
        )


BackofficeClientDep = Annotated[None, Depends(require_backoffice_client)]


@router.get("/health", response_model=PmsProjectionHealthResponse)
def pms_projection_health(_: BackofficeClientDep) -> PmsProjectionHealthResponse:
    return get_pms_projection_health()


@router.get("/products", response_model=PmsProductProjectionsResponse)
def pms_projection_products(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProductProjectionsResponse:
    return get_pms_product_projections(session)


@router.get("/units", response_model=PmsUnitProjectionsResponse)
def pms_projection_units(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsUnitProjectionsResponse:
    return get_pms_unit_projections(session)


@router.get("/sku-codes", response_model=PmsSkuCodeProjectionsResponse)
def pms_projection_sku_codes(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsSkuCodeProjectionsResponse:
    return get_pms_sku_code_projections(session)


@router.get("/barcodes", response_model=PmsBarcodeProjectionsResponse)
def pms_projection_barcodes(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsBarcodeProjectionsResponse:
    return get_pms_barcode_projections(session)


@router.get("/item-contents", response_model=PmsItemContentsProjectionResponse)
def pms_projection_item_contents(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsItemContentsProjectionResponse:
    return get_pms_item_content_projections(session)


@router.get("/item-assets", response_model=PmsItemAssetsProjectionResponse)
def pms_projection_item_assets(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsItemAssetsProjectionResponse:
    return get_pms_item_asset_projections(session)


@router.get("/display-categories", response_model=PmsDisplayCategoriesProjectionResponse)
def pms_projection_display_categories(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsDisplayCategoriesProjectionResponse:
    return get_pms_display_category_projections(session)


@router.get(
    "/item-display-category-bindings",
    response_model=PmsItemDisplayCategoryBindingsProjectionResponse,
)
def pms_projection_item_display_category_bindings(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsItemDisplayCategoryBindingsProjectionResponse:
    return get_pms_item_display_category_binding_projections(session)


@router.get("/brand-profiles", response_model=PmsBrandProfilesProjectionResponse)
def pms_projection_brand_profiles(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsBrandProfilesProjectionResponse:
    return get_pms_brand_profile_projections(session)


@router.get("/brand-assets", response_model=PmsBrandAssetsProjectionResponse)
def pms_projection_brand_assets(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsBrandAssetsProjectionResponse:
    return get_pms_brand_asset_projections(session)


@router.get("/sync-runs", response_model=PmsProjectionSyncRunsResponse)
def pms_projection_sync_runs(
    _: BackofficeClientDep,
    session: SessionDep,
) -> PmsProjectionSyncRunsResponse:
    return get_pms_projection_sync_runs(session)
