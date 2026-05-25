"""Client presentation services."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domains.client_presentation.contracts.client_presentation_contract import (
    ClientPresentationBlockTypeContract,
    ClientPresentationBlockTypeCreateRequest,
    ClientPresentationBlockTypesResponse,
    ClientPresentationHealthResponse,
    ClientPresentationPageContract,
    ClientPresentationPageCreateRequest,
    ClientPresentationPagesResponse,
    ClientPresentationRegionContract,
    ClientPresentationRegionCreateRequest,
    ClientPresentationRegionsResponse,
)
from app.domains.client_presentation.models.client_presentation import (
    ClientPresentationBlockType,
    ClientPresentationPage,
    ClientPresentationRegion,
)
from app.domains.client_presentation.repos.client_presentation_repo import (
    create_block_type,
    create_page,
    create_region,
    get_block_type_by_code,
    get_page_by_code,
    get_region_by_code,
    list_all_region_rows,
    list_block_types,
    list_pages,
    list_region_rows_by_page_id,
)


class ClientPresentationDuplicateCodeError(Exception):
    pass


class ClientPresentationPageNotFoundError(Exception):
    pass


def get_client_presentation_health() -> ClientPresentationHealthResponse:
    return ClientPresentationHealthResponse(
        status="ok",
        module="client_presentation",
        owner_tables=[
            "d2c_client_pages",
            "d2c_client_regions",
            "d2c_client_block_types",
        ],
        published_tables=[
            "d2c_published_client_pages",
            "d2c_published_client_regions",
            "d2c_published_client_block_types",
        ],
    )


def _as_list(value: list[str] | None) -> list[str]:
    return value or []


def _build_page_contract(page: ClientPresentationPage) -> ClientPresentationPageContract:
    return ClientPresentationPageContract(
        id=page.id,
        page_code=page.page_code,
        page_type=page.page_type,
        route_path=page.route_path,
        title=page.title,
        description=page.description,
        seo_title=page.seo_title,
        seo_description=page.seo_description,
        sort_order=page.sort_order,
        display_status=page.display_status,
        is_active=page.is_active,
        source_type=page.source_type,
        source_ref=page.source_ref,
        created_at=page.created_at,
        updated_at=page.updated_at,
    )


def get_client_presentation_pages(session: Session) -> ClientPresentationPagesResponse:
    pages = [_build_page_contract(page) for page in list_pages(session)]
    return ClientPresentationPagesResponse(count=len(pages), pages=pages)


def create_client_presentation_page(
    session: Session,
    payload: ClientPresentationPageCreateRequest,
) -> ClientPresentationPageContract:
    if get_page_by_code(session, payload.page_code) is not None:
        raise ClientPresentationDuplicateCodeError("client_page_already_exists")

    page = ClientPresentationPage(
        page_code=payload.page_code,
        page_type=payload.page_type,
        route_path=payload.route_path,
        title=payload.title,
        description=payload.description,
        seo_title=payload.seo_title,
        seo_description=payload.seo_description,
        sort_order=payload.sort_order,
        display_status=payload.display_status,
        is_active=payload.is_active,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )

    try:
        create_page(session, page)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ClientPresentationDuplicateCodeError("client_page_already_exists") from exc

    return _build_page_contract(page)


def _build_region_contract(
    region: ClientPresentationRegion,
    page: ClientPresentationPage,
) -> ClientPresentationRegionContract:
    return ClientPresentationRegionContract(
        id=region.id,
        page_id=region.page_id,
        page_code=page.page_code,
        region_code=region.region_code,
        region_type=region.region_type,
        title=region.title,
        description=region.description,
        sort_order=region.sort_order,
        is_required=region.is_required,
        max_blocks=region.max_blocks,
        allowed_block_types=_as_list(region.allowed_block_types),
        display_status=region.display_status,
        is_active=region.is_active,
        source_type=region.source_type,
        source_ref=region.source_ref,
        created_at=region.created_at,
        updated_at=region.updated_at,
    )


def get_client_presentation_regions(
    session: Session,
    page_code: str | None = None,
) -> ClientPresentationRegionsResponse:
    if page_code is None:
        rows = list_all_region_rows(session)
    else:
        page = get_page_by_code(session, page_code)
        if page is None:
            raise ClientPresentationPageNotFoundError("client_page_not_found")
        rows = list_region_rows_by_page_id(session, page.id)

    regions = [_build_region_contract(region, page) for region, page in rows]
    return ClientPresentationRegionsResponse(count=len(regions), regions=regions)


def create_client_presentation_region(
    session: Session,
    page_code: str,
    payload: ClientPresentationRegionCreateRequest,
) -> ClientPresentationRegionContract:
    page = get_page_by_code(session, page_code)
    if page is None:
        raise ClientPresentationPageNotFoundError("client_page_not_found")

    if get_region_by_code(session, payload.region_code) is not None:
        raise ClientPresentationDuplicateCodeError("client_region_already_exists")

    region = ClientPresentationRegion(
        page_id=page.id,
        region_code=payload.region_code,
        region_type=payload.region_type,
        title=payload.title,
        description=payload.description,
        sort_order=payload.sort_order,
        is_required=payload.is_required,
        max_blocks=payload.max_blocks,
        allowed_block_types=payload.allowed_block_types,
        display_status=payload.display_status,
        is_active=payload.is_active,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )

    try:
        create_region(session, region)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ClientPresentationDuplicateCodeError("client_region_already_exists") from exc

    return _build_region_contract(region, page)


def _build_block_type_contract(
    block_type: ClientPresentationBlockType,
) -> ClientPresentationBlockTypeContract:
    return ClientPresentationBlockTypeContract(
        id=block_type.id,
        block_type=block_type.block_type,
        display_name=block_type.display_name,
        description=block_type.description,
        renderer_key=block_type.renderer_key,
        data_contract_version=block_type.data_contract_version,
        allowed_region_types=_as_list(block_type.allowed_region_types),
        allowed_content_types=_as_list(block_type.allowed_content_types),
        layout_schema=block_type.layout_schema,
        slot_schema=block_type.slot_schema,
        action_schema=block_type.action_schema,
        analytics_schema=block_type.analytics_schema,
        display_status=block_type.display_status,
        is_active=block_type.is_active,
        source_type=block_type.source_type,
        source_ref=block_type.source_ref,
        created_at=block_type.created_at,
        updated_at=block_type.updated_at,
    )


def get_client_presentation_block_types(session: Session) -> ClientPresentationBlockTypesResponse:
    block_types = [_build_block_type_contract(row) for row in list_block_types(session)]
    return ClientPresentationBlockTypesResponse(count=len(block_types), block_types=block_types)


def create_client_presentation_block_type(
    session: Session,
    payload: ClientPresentationBlockTypeCreateRequest,
) -> ClientPresentationBlockTypeContract:
    if get_block_type_by_code(session, payload.block_type) is not None:
        raise ClientPresentationDuplicateCodeError("client_block_type_already_exists")

    block_type = ClientPresentationBlockType(
        block_type=payload.block_type,
        display_name=payload.display_name,
        description=payload.description,
        renderer_key=payload.renderer_key,
        data_contract_version=payload.data_contract_version,
        allowed_region_types=payload.allowed_region_types,
        allowed_content_types=payload.allowed_content_types,
        layout_schema=payload.layout_schema,
        slot_schema=payload.slot_schema,
        action_schema=payload.action_schema,
        analytics_schema=payload.analytics_schema,
        display_status=payload.display_status,
        is_active=payload.is_active,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )

    try:
        create_block_type(session, block_type)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ClientPresentationDuplicateCodeError("client_block_type_already_exists") from exc

    return _build_block_type_contract(block_type)
