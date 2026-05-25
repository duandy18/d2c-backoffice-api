"""Backoffice client presentation routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.client_presentation.contracts.client_presentation_contract import (
    ClientPresentationActionPoliciesResponse,
    ClientPresentationActionPolicyContract,
    ClientPresentationActionPolicyCreateRequest,
    ClientPresentationBlockTypeContract,
    ClientPresentationBlockTypeCreateRequest,
    ClientPresentationBlockTypesResponse,
    ClientPresentationDataBindingContract,
    ClientPresentationDataBindingCreateRequest,
    ClientPresentationDataBindingsResponse,
    ClientPresentationHealthResponse,
    ClientPresentationPageContract,
    ClientPresentationPageCreateRequest,
    ClientPresentationPagesResponse,
    ClientPresentationRegionContract,
    ClientPresentationRegionCreateRequest,
    ClientPresentationRegionsResponse,
    ClientPresentationSurfaceContract,
    ClientPresentationSurfaceCreateRequest,
    ClientPresentationSurfacesResponse,
    ClientPresentationTrackingPoliciesResponse,
    ClientPresentationTrackingPolicyContract,
    ClientPresentationTrackingPolicyCreateRequest,
    ClientPresentationVisibilityRuleContract,
    ClientPresentationVisibilityRuleCreateRequest,
    ClientPresentationVisibilityRulesResponse,
)
from app.domains.client_presentation.services.client_presentation_service import (
    ClientPresentationDuplicateCodeError,
    ClientPresentationPageNotFoundError,
    create_client_presentation_action_policy,
    create_client_presentation_block_type,
    create_client_presentation_data_binding,
    create_client_presentation_page,
    create_client_presentation_region,
    create_client_presentation_surface,
    create_client_presentation_tracking_policy,
    create_client_presentation_visibility_rule,
    get_client_presentation_action_policies,
    get_client_presentation_block_types,
    get_client_presentation_data_bindings,
    get_client_presentation_health,
    get_client_presentation_pages,
    get_client_presentation_regions,
    get_client_presentation_surfaces,
    get_client_presentation_tracking_policies,
    get_client_presentation_visibility_rules,
)

router = APIRouter(
    prefix="/backoffice/client-presentation",
    tags=["backoffice-client-presentation"],
)
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


@router.get("/health", response_model=ClientPresentationHealthResponse)
def client_presentation_health(_: BackofficeClientDep) -> ClientPresentationHealthResponse:
    return get_client_presentation_health()


@router.get("/pages", response_model=ClientPresentationPagesResponse)
def client_presentation_pages_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationPagesResponse:
    return get_client_presentation_pages(session)


@router.post(
    "/pages",
    response_model=ClientPresentationPageContract,
    status_code=status.HTTP_201_CREATED,
)
def client_presentation_pages_create(
    payload: ClientPresentationPageCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationPageContract:
    try:
        return create_client_presentation_page(session, payload)
    except ClientPresentationDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/regions", response_model=ClientPresentationRegionsResponse)
def client_presentation_regions_list(
    _: BackofficeClientDep,
    session: SessionDep,
    page_code: Annotated[str | None, Query()] = None,
) -> ClientPresentationRegionsResponse:
    try:
        return get_client_presentation_regions(session, page_code)
    except ClientPresentationPageNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "/pages/{page_code}/regions",
    response_model=ClientPresentationRegionContract,
    status_code=status.HTTP_201_CREATED,
)
def client_presentation_regions_create(
    page_code: str,
    payload: ClientPresentationRegionCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationRegionContract:
    try:
        return create_client_presentation_region(session, page_code, payload)
    except ClientPresentationPageNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ClientPresentationDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/block-types", response_model=ClientPresentationBlockTypesResponse)
def client_presentation_block_types_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationBlockTypesResponse:
    return get_client_presentation_block_types(session)


@router.post(
    "/block-types",
    response_model=ClientPresentationBlockTypeContract,
    status_code=status.HTTP_201_CREATED,
)
def client_presentation_block_types_create(
    payload: ClientPresentationBlockTypeCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationBlockTypeContract:
    try:
        return create_client_presentation_block_type(session, payload)
    except ClientPresentationDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc



@router.get("/surfaces", response_model=ClientPresentationSurfacesResponse)
def client_presentation_surfaces_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationSurfacesResponse:
    return get_client_presentation_surfaces(session)


@router.post(
    "/surfaces",
    response_model=ClientPresentationSurfaceContract,
    status_code=status.HTTP_201_CREATED,
)
def client_presentation_surfaces_create(
    payload: ClientPresentationSurfaceCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationSurfaceContract:
    try:
        return create_client_presentation_surface(session, payload)
    except ClientPresentationDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/data-bindings", response_model=ClientPresentationDataBindingsResponse)
def client_presentation_data_bindings_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationDataBindingsResponse:
    return get_client_presentation_data_bindings(session)


@router.post(
    "/data-bindings",
    response_model=ClientPresentationDataBindingContract,
    status_code=status.HTTP_201_CREATED,
)
def client_presentation_data_bindings_create(
    payload: ClientPresentationDataBindingCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationDataBindingContract:
    try:
        return create_client_presentation_data_binding(session, payload)
    except ClientPresentationDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/visibility-rules", response_model=ClientPresentationVisibilityRulesResponse)
def client_presentation_visibility_rules_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationVisibilityRulesResponse:
    return get_client_presentation_visibility_rules(session)


@router.post(
    "/visibility-rules",
    response_model=ClientPresentationVisibilityRuleContract,
    status_code=status.HTTP_201_CREATED,
)
def client_presentation_visibility_rules_create(
    payload: ClientPresentationVisibilityRuleCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationVisibilityRuleContract:
    try:
        return create_client_presentation_visibility_rule(session, payload)
    except ClientPresentationDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/action-policies", response_model=ClientPresentationActionPoliciesResponse)
def client_presentation_action_policies_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationActionPoliciesResponse:
    return get_client_presentation_action_policies(session)


@router.post(
    "/action-policies",
    response_model=ClientPresentationActionPolicyContract,
    status_code=status.HTTP_201_CREATED,
)
def client_presentation_action_policies_create(
    payload: ClientPresentationActionPolicyCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationActionPolicyContract:
    try:
        return create_client_presentation_action_policy(session, payload)
    except ClientPresentationDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/tracking-policies", response_model=ClientPresentationTrackingPoliciesResponse)
def client_presentation_tracking_policies_list(
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationTrackingPoliciesResponse:
    return get_client_presentation_tracking_policies(session)


@router.post(
    "/tracking-policies",
    response_model=ClientPresentationTrackingPolicyContract,
    status_code=status.HTTP_201_CREATED,
)
def client_presentation_tracking_policies_create(
    payload: ClientPresentationTrackingPolicyCreateRequest,
    _: BackofficeClientDep,
    session: SessionDep,
) -> ClientPresentationTrackingPolicyContract:
    try:
        return create_client_presentation_tracking_policy(session, payload)
    except ClientPresentationDuplicateCodeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
