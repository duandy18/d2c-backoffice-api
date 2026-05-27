"""Client presentation services."""

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

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
    ClientPresentationHomeBlockCreateRequest,
    ClientPresentationHomeBlockUpdateRequest,
    ClientPresentationHomeDraftResponse,
    ClientPresentationHomeDraftSummary,
    ClientPresentationHomePlannerOptionsResponse,
    ClientPresentationHomeRegionCreateRequest,
    ClientPresentationHomeRegionUpdateRequest,
    ClientPresentationPageContract,
    ClientPresentationPageCreateRequest,
    ClientPresentationPagesResponse,
    ClientPresentationPlannerBlockTypeOption,
    ClientPresentationPlannerField,
    ClientPresentationPlannerOption,
    ClientPresentationPlannerRegionTypeOption,
    ClientPresentationPreviewBlock,
    ClientPresentationPreviewPage,
    ClientPresentationPreviewPosition,
    ClientPresentationPreviewRegion,
    ClientPresentationPreviewResponse,
    ClientPresentationPublishRuntimeStatusResponse,
    ClientPresentationRegionBlockContract,
    ClientPresentationRegionBlockCreateRequest,
    ClientPresentationRegionBlocksResponse,
    ClientPresentationRegionContract,
    ClientPresentationRegionCreateRequest,
    ClientPresentationRegionsResponse,
    ClientPresentationRuntimeSnapshotCount,
    ClientPresentationSurfaceContract,
    ClientPresentationSurfaceCreateRequest,
    ClientPresentationSurfacesResponse,
    ClientPresentationTrackingPoliciesResponse,
    ClientPresentationTrackingPolicyContract,
    ClientPresentationTrackingPolicyCreateRequest,
    ClientPresentationValidationIssue,
    ClientPresentationValidationReportResponse,
    ClientPresentationVisibilityRuleContract,
    ClientPresentationVisibilityRuleCreateRequest,
    ClientPresentationVisibilityRulesResponse,
)
from app.domains.client_presentation.models.client_presentation import (
    ClientPresentationActionPolicy,
    ClientPresentationBlockType,
    ClientPresentationDataBinding,
    ClientPresentationPage,
    ClientPresentationRegion,
    ClientPresentationRegionBlock,
    ClientPresentationSurface,
    ClientPresentationTrackingPolicy,
    ClientPresentationVisibilityRule,
)
from app.domains.client_presentation.repos.client_presentation_repo import (
    create_action_policy,
    create_block_type,
    create_data_binding,
    create_page,
    create_region,
    create_region_block,
    create_surface,
    create_tracking_policy,
    create_visibility_rule,
    get_action_policy_by_code,
    get_block_type_by_code,
    get_data_binding_by_code,
    get_page_by_code,
    get_region_block_by_code,
    get_region_by_code,
    get_surface_by_code,
    get_tracking_policy_by_code,
    get_visibility_rule_by_code,
    list_action_policies,
    list_all_region_rows,
    list_block_types,
    list_data_bindings,
    list_pages,
    list_region_block_rows,
    list_region_rows_by_page_id,
    list_surfaces,
    list_tracking_policies,
    list_visibility_rules,
    update_region,
    update_region_block,
)
from app.domains.publish.models.publish_version import PublishVersion
from app.domains.published_snapshot.models.published_snapshot import (
    PublishedClientActionPolicy,
    PublishedClientBlockType,
    PublishedClientDataBinding,
    PublishedClientPage,
    PublishedClientRegion,
    PublishedClientRegionBlock,
    PublishedClientSurface,
    PublishedClientTrackingPolicy,
    PublishedClientVisibilityRule,
    PublishedStorefrontSection,
    PublishedStorefrontSectionLayout,
    PublishedStorefrontSectionPosition,
)
from app.domains.storefront_sections.models.storefront_section import (
    StorefrontSection,
    StorefrontSectionLayout,
    StorefrontSectionPosition,
)
from app.domains.storefront_sections.repos.storefront_section_repo import (
    get_layout_by_section_id,
    list_section_position_rows,
    list_section_rows,
)


class ClientPresentationDuplicateCodeError(Exception):
    pass


class ClientPresentationPageNotFoundError(Exception):
    pass


class ClientPresentationPlannerValidationError(Exception):
    pass


def get_client_presentation_health() -> ClientPresentationHealthResponse:
    return ClientPresentationHealthResponse(
        status="ok",
        module="client_presentation",
        owner_tables=[
            "d2c_client_pages",
            "d2c_client_regions",
            "d2c_client_block_types",
            "d2c_client_region_blocks",
            "d2c_client_surfaces",
            "d2c_client_data_bindings",
            "d2c_client_visibility_rules",
            "d2c_client_action_policies",
            "d2c_client_tracking_policies",
        ],
        published_tables=[
            "d2c_published_client_pages",
            "d2c_published_client_regions",
            "d2c_published_client_block_types",
            "d2c_published_client_region_blocks",
            "d2c_published_client_surfaces",
            "d2c_published_client_data_bindings",
            "d2c_published_client_visibility_rules",
            "d2c_published_client_action_policies",
            "d2c_published_client_tracking_policies",
        ],
    )


def _as_list(value: list[str] | None) -> list[str]:
    return value or []


HOME_PAGE_CODE = "home"
PC_WEB_SURFACE_CODE = "web_desktop"

HOME_REGION_TYPE_RULES: dict[str, dict[str, object]] = {
    "hero": {
        "label": "头图区",
        "description": "用于主视觉、广告位和促销提醒。",
        "allowed_block_types": ["title", "ad_banner", "promotion_strip", "promo_strip"],
        "default_max_blocks": 3,
        "default_is_required": True,
    },
    "navigation": {
        "label": "快捷导航区",
        "description": "用于分类入口、图文导航等快速入口。",
        "allowed_block_types": ["category_nav", "image_grid"],
        "default_max_blocks": 2,
        "default_is_required": False,
    },
    "main": {
        "label": "主体区",
        "description": "用于首页核心内容，包括标题、广告、分类、货架和促销。",
        "allowed_block_types": [
            "title",
            "ad_banner",
            "category_nav",
            "offer_shelf",
            "promotion_strip",
            "promo_strip",
            "ranking_list",
        ],
        "default_max_blocks": 20,
        "default_is_required": True,
    },
    "recommendation": {
        "label": "推荐区",
        "description": "用于推荐商品、猜你喜欢和补充货架。",
        "allowed_block_types": ["offer_shelf", "product_recommendation"],
        "default_max_blocks": 8,
        "default_is_required": False,
    },
    "footer": {
        "label": "页尾区",
        "description": "用于服务说明、链接组和页尾内容。",
        "allowed_block_types": ["rich_text", "image_grid"],
        "default_max_blocks": 4,
        "default_is_required": False,
    },
}

HOME_BLOCK_SOURCE_TYPES: dict[str, list[str]] = {
    "title": ["manual_inline"],
    "ad_banner": ["manual_inline"],
    "category_nav": ["data_binding"],
    "offer_shelf": ["data_binding", "storefront_section"],
    "promotion_strip": ["manual_inline", "data_binding"],
    "promo_strip": ["manual_inline", "data_binding"],
    "product_recommendation": ["data_binding"],
    "ranking_list": ["data_binding"],
    "image_grid": ["manual_inline", "data_binding"],
    "rich_text": ["manual_inline"],
}


def _field_was_set(payload: object, field_name: str) -> bool:
    fields_set = getattr(payload, "model_fields_set", set())
    return field_name in fields_set


def _planner_option(
    value: str, label: str, description: str | None = None
) -> ClientPresentationPlannerOption:
    return ClientPresentationPlannerOption(value=value, label=label, description=description)


def _home_region_rule(region_type: str) -> dict[str, object]:
    rule = HOME_REGION_TYPE_RULES.get(region_type)
    if rule is None:
        raise ClientPresentationPlannerValidationError("home_region_type_not_allowed")
    return rule


def _home_allowed_block_types(region_type: str) -> list[str]:
    return list(_home_region_rule(region_type)["allowed_block_types"])


def _home_allowed_block_type_set() -> set[str]:
    return {
        block_type
        for rule in HOME_REGION_TYPE_RULES.values()
        for block_type in list(rule["allowed_block_types"])
    }


def _home_region_code_exists(session: Session, region_code: str) -> bool:
    return get_region_by_code(session, region_code) is not None


def _next_home_region_code(session: Session, region_type: str) -> str:
    base_code = f"{HOME_PAGE_CODE}.{region_type}"
    if not _home_region_code_exists(session, base_code):
        return base_code

    for index in range(1, 1000):
        candidate = f"{base_code}.{index:03d}"
        if not _home_region_code_exists(session, candidate):
            return candidate

    raise ClientPresentationPlannerValidationError("home_region_code_exhausted")


def _next_home_block_code(session: Session, region_code: str, block_type: str) -> str:
    base_code = f"{region_code}.{block_type}"
    for index in range(1, 1000):
        candidate = f"{base_code}.{index:03d}"
        if get_region_block_by_code(session, candidate) is None:
            return candidate

    raise ClientPresentationPlannerValidationError("home_block_code_exhausted")


def _assert_home_region(region: ClientPresentationRegion) -> None:
    if not region.region_code.startswith(f"{HOME_PAGE_CODE}."):
        raise ClientPresentationPageNotFoundError("client_region_not_in_home")


def _validate_home_visible_range(
    visible_from: object | None,
    visible_until: object | None,
) -> None:
    if visible_from is not None and visible_until is not None and visible_until <= visible_from:
        raise ClientPresentationPlannerValidationError("home_block_visible_range_invalid")


def _validate_home_block_content(
    *,
    block_type: str,
    content_source_type: str,
    content_source_ref: str | None,
    content_payload: dict[str, object] | None,
) -> None:
    allowed_sources = HOME_BLOCK_SOURCE_TYPES.get(block_type, ["manual_inline"])
    if content_source_type not in allowed_sources:
        raise ClientPresentationPlannerValidationError("home_block_content_source_type_not_allowed")

    if content_source_type in {"data_binding", "storefront_section"} and not content_source_ref:
        raise ClientPresentationPlannerValidationError("home_block_content_source_ref_required")

    if block_type == "title":
        if content_source_type != "manual_inline":
            raise ClientPresentationPlannerValidationError(
                "home_title_block_must_use_manual_inline"
            )
        if not isinstance(content_payload, dict) or not content_payload.get("title"):
            raise ClientPresentationPlannerValidationError("home_title_block_title_required")

    if block_type == "ad_banner":
        if content_source_type != "manual_inline":
            raise ClientPresentationPlannerValidationError("home_ad_banner_must_use_manual_inline")
        items = content_payload.get("items") if isinstance(content_payload, dict) else None
        if not isinstance(items, list) or len(items) == 0:
            raise ClientPresentationPlannerValidationError("home_ad_banner_items_required")
        first_item = items[0]
        if not isinstance(first_item, dict) or not first_item.get("image_url"):
            raise ClientPresentationPlannerValidationError("home_ad_banner_image_url_required")

    if block_type in {"promotion_strip", "promo_strip"} and content_source_type == "manual_inline":
        if not isinstance(content_payload, dict) or not (
            content_payload.get("title") or content_payload.get("promotion_code")
        ):
            raise ClientPresentationPlannerValidationError("home_promotion_content_required")


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


def _build_region_block_contract(
    region_block: ClientPresentationRegionBlock,
    region: ClientPresentationRegion,
    page: ClientPresentationPage,
) -> ClientPresentationRegionBlockContract:
    return ClientPresentationRegionBlockContract(
        id=region_block.id,
        region_id=region_block.region_id,
        page_code=page.page_code,
        region_code=region.region_code,
        block_code=region_block.block_code,
        block_type=region_block.block_type,
        renderer_key=region_block.renderer_key,
        title=region_block.title,
        subtitle=region_block.subtitle,
        description=region_block.description,
        sort_order=region_block.sort_order,
        display_status=region_block.display_status,
        is_active=region_block.is_active,
        visible_from=region_block.visible_from,
        visible_until=region_block.visible_until,
        content_source_type=region_block.content_source_type,
        content_source_ref=region_block.content_source_ref,
        content_payload=region_block.content_payload,
        source_type=region_block.source_type,
        source_ref=region_block.source_ref,
        created_at=region_block.created_at,
        updated_at=region_block.updated_at,
    )


def get_client_presentation_region_blocks(
    session: Session,
    region_code: str | None = None,
) -> ClientPresentationRegionBlocksResponse:
    if region_code is None:
        rows = list_region_block_rows(session)
    else:
        region = get_region_by_code(session, region_code)
        if region is None:
            raise ClientPresentationPageNotFoundError("client_region_not_found")
        rows = list_region_block_rows(session, region.id)

    region_blocks = [
        _build_region_block_contract(region_block, region, page)
        for region_block, region, page in rows
    ]
    return ClientPresentationRegionBlocksResponse(
        count=len(region_blocks),
        region_blocks=region_blocks,
    )


def create_client_presentation_region_block(
    session: Session,
    region_code: str,
    payload: ClientPresentationRegionBlockCreateRequest,
) -> ClientPresentationRegionBlockContract:
    region = get_region_by_code(session, region_code)
    if region is None:
        raise ClientPresentationPageNotFoundError("client_region_not_found")

    page = session.get(ClientPresentationPage, region.page_id)
    if page is None:
        raise ClientPresentationPageNotFoundError("client_page_not_found")

    if get_region_block_by_code(session, payload.block_code) is not None:
        raise ClientPresentationDuplicateCodeError("client_region_block_already_exists")

    block_type = get_block_type_by_code(session, payload.block_type)
    if block_type is None:
        raise ClientPresentationDuplicateCodeError("client_block_type_not_registered")

    allowed = _as_list(region.allowed_block_types)
    if allowed and payload.block_type not in allowed:
        raise ClientPresentationDuplicateCodeError("client_region_block_type_not_allowed")

    if (
        payload.visible_from is not None
        and payload.visible_until is not None
        and payload.visible_until <= payload.visible_from
    ):
        raise ClientPresentationDuplicateCodeError("client_region_block_visible_range_invalid")

    region_block = ClientPresentationRegionBlock(
        region_id=region.id,
        block_code=payload.block_code,
        block_type=payload.block_type,
        renderer_key=block_type.renderer_key,
        title=payload.title,
        subtitle=payload.subtitle,
        description=payload.description,
        sort_order=payload.sort_order,
        display_status=payload.display_status,
        is_active=payload.is_active,
        visible_from=payload.visible_from,
        visible_until=payload.visible_until,
        content_source_type=payload.content_source_type,
        content_source_ref=payload.content_source_ref,
        content_payload=payload.content_payload,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )

    try:
        create_region_block(session, region_block)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ClientPresentationDuplicateCodeError("client_region_block_already_exists") from exc

    return _build_region_block_contract(region_block, region, page)


def _as_dict(value: dict[str, object] | None) -> dict[str, object] | None:
    return value


def _build_surface_contract(
    surface: ClientPresentationSurface,
) -> ClientPresentationSurfaceContract:
    return ClientPresentationSurfaceContract(
        id=surface.id,
        surface_code=surface.surface_code,
        surface_name=surface.surface_name,
        surface_type=surface.surface_type,
        device_family=surface.device_family,
        breakpoint_profile=surface.breakpoint_profile,
        supported_renderer_keys=_as_list(surface.supported_renderer_keys),
        is_active=surface.is_active,
        source_type=surface.source_type,
        source_ref=surface.source_ref,
        created_at=surface.created_at,
        updated_at=surface.updated_at,
    )


def get_client_presentation_surfaces(session: Session) -> ClientPresentationSurfacesResponse:
    surfaces = [_build_surface_contract(row) for row in list_surfaces(session)]
    return ClientPresentationSurfacesResponse(count=len(surfaces), surfaces=surfaces)


def create_client_presentation_surface(
    session: Session,
    payload: ClientPresentationSurfaceCreateRequest,
) -> ClientPresentationSurfaceContract:
    if get_surface_by_code(session, payload.surface_code) is not None:
        raise ClientPresentationDuplicateCodeError("client_surface_already_exists")

    surface = ClientPresentationSurface(
        surface_code=payload.surface_code,
        surface_name=payload.surface_name,
        surface_type=payload.surface_type,
        device_family=payload.device_family,
        breakpoint_profile=payload.breakpoint_profile,
        supported_renderer_keys=payload.supported_renderer_keys,
        is_active=payload.is_active,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )

    try:
        create_surface(session, surface)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ClientPresentationDuplicateCodeError("client_surface_already_exists") from exc

    return _build_surface_contract(surface)


def _build_data_binding_contract(
    binding: ClientPresentationDataBinding,
) -> ClientPresentationDataBindingContract:
    return ClientPresentationDataBindingContract(
        id=binding.id,
        binding_code=binding.binding_code,
        target_type=binding.target_type,
        target_code=binding.target_code,
        data_source_type=binding.data_source_type,
        data_source_ref=binding.data_source_ref,
        content_type=binding.content_type,
        query_params=_as_dict(binding.query_params),
        result_limit=binding.result_limit,
        sort_policy=_as_dict(binding.sort_policy),
        refresh_policy=_as_dict(binding.refresh_policy),
        is_active=binding.is_active,
        source_type=binding.source_type,
        source_ref=binding.source_ref,
        created_at=binding.created_at,
        updated_at=binding.updated_at,
    )


def get_client_presentation_data_bindings(
    session: Session,
) -> ClientPresentationDataBindingsResponse:
    bindings = [_build_data_binding_contract(row) for row in list_data_bindings(session)]
    return ClientPresentationDataBindingsResponse(count=len(bindings), data_bindings=bindings)


def create_client_presentation_data_binding(
    session: Session,
    payload: ClientPresentationDataBindingCreateRequest,
) -> ClientPresentationDataBindingContract:
    if get_data_binding_by_code(session, payload.binding_code) is not None:
        raise ClientPresentationDuplicateCodeError("client_data_binding_already_exists")

    binding = ClientPresentationDataBinding(
        binding_code=payload.binding_code,
        target_type=payload.target_type,
        target_code=payload.target_code,
        data_source_type=payload.data_source_type,
        data_source_ref=payload.data_source_ref,
        content_type=payload.content_type,
        query_params=payload.query_params,
        result_limit=payload.result_limit,
        sort_policy=payload.sort_policy,
        refresh_policy=payload.refresh_policy,
        is_active=payload.is_active,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )

    try:
        create_data_binding(session, binding)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ClientPresentationDuplicateCodeError("client_data_binding_already_exists") from exc

    return _build_data_binding_contract(binding)


def _build_visibility_rule_contract(
    rule: ClientPresentationVisibilityRule,
) -> ClientPresentationVisibilityRuleContract:
    return ClientPresentationVisibilityRuleContract(
        id=rule.id,
        rule_code=rule.rule_code,
        target_type=rule.target_type,
        target_code=rule.target_code,
        client_surface_codes=_as_list(rule.client_surface_codes),
        customer_segments=_as_list(rule.customer_segments),
        login_state=rule.login_state,
        locale=rule.locale,
        currency=rule.currency,
        visible_from=rule.visible_from,
        visible_until=rule.visible_until,
        rule_expression=_as_dict(rule.rule_expression),
        priority=rule.priority,
        is_active=rule.is_active,
        source_type=rule.source_type,
        source_ref=rule.source_ref,
        created_at=rule.created_at,
        updated_at=rule.updated_at,
    )


def get_client_presentation_visibility_rules(
    session: Session,
) -> ClientPresentationVisibilityRulesResponse:
    rules = [_build_visibility_rule_contract(row) for row in list_visibility_rules(session)]
    return ClientPresentationVisibilityRulesResponse(count=len(rules), visibility_rules=rules)


def create_client_presentation_visibility_rule(
    session: Session,
    payload: ClientPresentationVisibilityRuleCreateRequest,
) -> ClientPresentationVisibilityRuleContract:
    if get_visibility_rule_by_code(session, payload.rule_code) is not None:
        raise ClientPresentationDuplicateCodeError("client_visibility_rule_already_exists")

    rule = ClientPresentationVisibilityRule(
        rule_code=payload.rule_code,
        target_type=payload.target_type,
        target_code=payload.target_code,
        client_surface_codes=payload.client_surface_codes,
        customer_segments=payload.customer_segments,
        login_state=payload.login_state,
        locale=payload.locale,
        currency=payload.currency,
        visible_from=payload.visible_from,
        visible_until=payload.visible_until,
        rule_expression=payload.rule_expression,
        priority=payload.priority,
        is_active=payload.is_active,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )

    try:
        create_visibility_rule(session, rule)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ClientPresentationDuplicateCodeError("client_visibility_rule_already_exists") from exc

    return _build_visibility_rule_contract(rule)


def _build_action_policy_contract(
    policy: ClientPresentationActionPolicy,
) -> ClientPresentationActionPolicyContract:
    return ClientPresentationActionPolicyContract(
        id=policy.id,
        policy_code=policy.policy_code,
        target_type=policy.target_type,
        target_code=policy.target_code,
        action_type=policy.action_type,
        label=policy.label,
        target_url=policy.target_url,
        target_page_code=policy.target_page_code,
        target_ref=policy.target_ref,
        open_mode=policy.open_mode,
        action_payload=_as_dict(policy.action_payload),
        is_active=policy.is_active,
        source_type=policy.source_type,
        source_ref=policy.source_ref,
        created_at=policy.created_at,
        updated_at=policy.updated_at,
    )


def get_client_presentation_action_policies(
    session: Session,
) -> ClientPresentationActionPoliciesResponse:
    policies = [_build_action_policy_contract(row) for row in list_action_policies(session)]
    return ClientPresentationActionPoliciesResponse(count=len(policies), action_policies=policies)


def create_client_presentation_action_policy(
    session: Session,
    payload: ClientPresentationActionPolicyCreateRequest,
) -> ClientPresentationActionPolicyContract:
    if get_action_policy_by_code(session, payload.policy_code) is not None:
        raise ClientPresentationDuplicateCodeError("client_action_policy_already_exists")

    policy = ClientPresentationActionPolicy(
        policy_code=payload.policy_code,
        target_type=payload.target_type,
        target_code=payload.target_code,
        action_type=payload.action_type,
        label=payload.label,
        target_url=payload.target_url,
        target_page_code=payload.target_page_code,
        target_ref=payload.target_ref,
        open_mode=payload.open_mode,
        action_payload=payload.action_payload,
        is_active=payload.is_active,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )

    try:
        create_action_policy(session, policy)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ClientPresentationDuplicateCodeError("client_action_policy_already_exists") from exc

    return _build_action_policy_contract(policy)


def _build_tracking_policy_contract(
    policy: ClientPresentationTrackingPolicy,
) -> ClientPresentationTrackingPolicyContract:
    return ClientPresentationTrackingPolicyContract(
        id=policy.id,
        policy_code=policy.policy_code,
        target_type=policy.target_type,
        target_code=policy.target_code,
        event_name=policy.event_name,
        event_type=policy.event_type,
        event_trigger=policy.event_trigger,
        tracking_params=_as_dict(policy.tracking_params),
        is_required=policy.is_required,
        is_active=policy.is_active,
        source_type=policy.source_type,
        source_ref=policy.source_ref,
        created_at=policy.created_at,
        updated_at=policy.updated_at,
    )


def get_client_presentation_tracking_policies(
    session: Session,
) -> ClientPresentationTrackingPoliciesResponse:
    policies = [_build_tracking_policy_contract(row) for row in list_tracking_policies(session)]
    return ClientPresentationTrackingPoliciesResponse(
        count=len(policies),
        tracking_policies=policies,
    )


def create_client_presentation_tracking_policy(
    session: Session,
    payload: ClientPresentationTrackingPolicyCreateRequest,
) -> ClientPresentationTrackingPolicyContract:
    if get_tracking_policy_by_code(session, payload.policy_code) is not None:
        raise ClientPresentationDuplicateCodeError("client_tracking_policy_already_exists")

    policy = ClientPresentationTrackingPolicy(
        policy_code=payload.policy_code,
        target_type=payload.target_type,
        target_code=payload.target_code,
        event_name=payload.event_name,
        event_type=payload.event_type,
        event_trigger=payload.event_trigger,
        tracking_params=payload.tracking_params,
        is_required=payload.is_required,
        is_active=payload.is_active,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )

    try:
        create_tracking_policy(session, policy)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ClientPresentationDuplicateCodeError("client_tracking_policy_already_exists") from exc

    return _build_tracking_policy_contract(policy)


def _known_client_targets(session: Session) -> dict[str, set[str]]:
    pages = {row.page_code for row in list_pages(session)}
    regions = {row.region_code for row, _page in list_all_region_rows(session)}
    block_types = {row.block_type for row in list_block_types(session)}
    region_blocks = {row.block_code for row, _region, _page in list_region_block_rows(session)}
    sections = {section.section_code for section, _group in list_section_rows(session)}
    return {
        "global": {"client_presentation"},
        "page": pages,
        "region": regions,
        "block_type": block_types,
        "region_block": region_blocks,
        "section": sections,
    }


def _target_exists(targets: dict[str, set[str]], target_type: str, target_code: str) -> bool:
    if target_type == "global":
        return True
    return target_code in targets.get(target_type, set())


def _count_owner(session: Session, model: type[object]) -> int:
    return int(session.scalar(select(func.count()).select_from(model)) or 0)


def _count_snapshot(
    session: Session,
    model: type[object],
    publish_version: str | None,
) -> int:
    if publish_version is None:
        return 0
    return int(
        session.scalar(
            select(func.count()).select_from(model).where(model.publish_version == publish_version)
        )
        or 0
    )


def _latest_publish_version(session: Session) -> PublishVersion | None:
    statement = (
        select(PublishVersion)
        .where(PublishVersion.status == "published")
        .where(PublishVersion.publish_scope.in_(("storefront", "all")))
        .order_by(PublishVersion.published_at.desc().nullslast(), PublishVersion.id.desc())
        .limit(1)
    )
    return session.scalar(statement)


def get_client_presentation_validation_report(
    session: Session,
) -> ClientPresentationValidationReportResponse:
    issues: list[ClientPresentationValidationIssue] = []

    pages = {row.page_code for row in list_pages(session)}
    regions = {row.region_code: row for row, _page in list_all_region_rows(session)}
    region_blocks = {
        row.block_code: (row, region) for row, region, _page in list_region_block_rows(session)
    }
    block_types = {row.block_type: row for row in list_block_types(session)}
    renderer_keys = {row.renderer_key for row in block_types.values()}
    targets = _known_client_targets(session)

    for region in regions.values():
        for block_type in _as_list(region.allowed_block_types):
            if block_type not in block_types:
                issues.append(
                    ClientPresentationValidationIssue(
                        severity="blocking",
                        code="region_block_type_missing",
                        message="Region references a block type that is not registered.",
                        target_type="region",
                        target_code=region.region_code,
                    )
                )

    surfaces = list_surfaces(session)
    for surface in surfaces:
        for renderer_key in _as_list(surface.supported_renderer_keys):
            if renderer_key not in renderer_keys:
                issues.append(
                    ClientPresentationValidationIssue(
                        severity="blocking",
                        code="surface_renderer_missing",
                        message="Surface references a renderer key without a block type.",
                        target_type="surface",
                        target_code=surface.surface_code,
                    )
                )

    region_block_counts: dict[str, int] = {}
    sections = {section.section_code for section, _group in list_section_rows(session)}
    for region_block, region in region_blocks.values():
        region_block_counts[region.region_code] = region_block_counts.get(region.region_code, 0) + 1

        block_type = block_types.get(region_block.block_type)
        if block_type is None:
            issues.append(
                ClientPresentationValidationIssue(
                    severity="blocking",
                    code="region_block_type_missing",
                    message="Region block references an unregistered block type.",
                    target_type="region_block",
                    target_code=region_block.block_code,
                )
            )
            continue

        if region_block.renderer_key != block_type.renderer_key:
            issues.append(
                ClientPresentationValidationIssue(
                    severity="blocking",
                    code="region_block_renderer_mismatch",
                    message="Region block renderer key must match its block type.",
                    target_type="region_block",
                    target_code=region_block.block_code,
                )
            )

        allowed = _as_list(region.allowed_block_types)
        if allowed and region_block.block_type not in allowed:
            issues.append(
                ClientPresentationValidationIssue(
                    severity="blocking",
                    code="region_block_type_not_allowed",
                    message="Region block type is not allowed by its region.",
                    target_type="region_block",
                    target_code=region_block.block_code,
                )
            )

        supported_by_any_surface = any(
            region_block.renderer_key in _as_list(surface.supported_renderer_keys)
            for surface in surfaces
        )
        if not supported_by_any_surface:
            issues.append(
                ClientPresentationValidationIssue(
                    severity="blocking",
                    code="region_block_renderer_not_supported",
                    message="Region block renderer is not supported by any registered surface.",
                    target_type="region_block",
                    target_code=region_block.block_code,
                )
            )

        if (
            region_block.content_source_type == "storefront_section"
            and region_block.content_source_ref not in sections
        ):
            issues.append(
                ClientPresentationValidationIssue(
                    severity="blocking",
                    code="region_block_section_missing",
                    message="Region block references a missing storefront section.",
                    target_type="region_block",
                    target_code=region_block.block_code,
                )
            )

    for region in regions.values():
        if (
            region.max_blocks is not None
            and region_block_counts.get(region.region_code, 0) > region.max_blocks
        ):
            issues.append(
                ClientPresentationValidationIssue(
                    severity="blocking",
                    code="region_max_blocks_exceeded",
                    message="Region contains more blocks than allowed.",
                    target_type="region",
                    target_code=region.region_code,
                )
            )

    for binding in list_data_bindings(session):
        if not _target_exists(targets, binding.target_type, binding.target_code):
            issues.append(
                ClientPresentationValidationIssue(
                    severity="blocking",
                    code="data_binding_target_missing",
                    message="Data binding target is not a known client presentation target.",
                    target_type=binding.target_type,
                    target_code=binding.target_code,
                )
            )

    for rule in list_visibility_rules(session):
        if not _target_exists(targets, rule.target_type, rule.target_code):
            issues.append(
                ClientPresentationValidationIssue(
                    severity="blocking",
                    code="visibility_target_missing",
                    message="Visibility rule target is not a known client presentation target.",
                    target_type=rule.target_type,
                    target_code=rule.target_code,
                )
            )

    for policy in list_action_policies(session):
        if not _target_exists(targets, policy.target_type, policy.target_code):
            issues.append(
                ClientPresentationValidationIssue(
                    severity="blocking",
                    code="action_target_missing",
                    message="Action policy target is not a known client presentation target.",
                    target_type=policy.target_type,
                    target_code=policy.target_code,
                )
            )
        if policy.target_page_code is not None and policy.target_page_code not in pages:
            issues.append(
                ClientPresentationValidationIssue(
                    severity="blocking",
                    code="action_target_page_missing",
                    message="Action policy target page is not registered.",
                    target_type="action_policy",
                    target_code=policy.policy_code,
                )
            )

    for policy in list_tracking_policies(session):
        if not _target_exists(targets, policy.target_type, policy.target_code):
            issues.append(
                ClientPresentationValidationIssue(
                    severity="blocking",
                    code="tracking_target_missing",
                    message="Tracking policy target is not a known client presentation target.",
                    target_type=policy.target_type,
                    target_code=policy.target_code,
                )
            )

    blocking_count = sum(1 for issue in issues if issue.severity == "blocking")
    warning_count = sum(1 for issue in issues if issue.severity == "warning")

    return ClientPresentationValidationReportResponse(
        can_publish=blocking_count == 0,
        issue_count=len(issues),
        blocking_issue_count=blocking_count,
        warning_issue_count=warning_count,
        checked_counts={
            "pages": len(pages),
            "regions": len(regions),
            "block_types": len(block_types),
            "region_blocks": len(region_blocks),
            "surfaces": len(surfaces),
            "data_bindings": len(list_data_bindings(session)),
            "visibility_rules": len(list_visibility_rules(session)),
            "action_policies": len(list_action_policies(session)),
            "tracking_policies": len(list_tracking_policies(session)),
            "sections": len(list_section_rows(session)),
        },
        issues=issues,
    )


def _layout_payload(layout: StorefrontSectionLayout | None) -> dict[str, object] | None:
    if layout is None:
        return None
    return {
        "display_type": layout.display_type,
        "columns_desktop": layout.columns_desktop,
        "columns_tablet": layout.columns_tablet,
        "columns_mobile": layout.columns_mobile,
        "card_size": layout.card_size,
        "image_ratio": layout.image_ratio,
        "show_promotion_badge": layout.show_promotion_badge,
        "show_sales_summary": layout.show_sales_summary,
        "show_review_summary": layout.show_review_summary,
        "show_compare_price": layout.show_compare_price,
        "show_quantity_stepper": layout.show_quantity_stepper,
        "max_items": layout.max_items,
    }


def _preview_positions(
    session: Session,
    section: StorefrontSection,
) -> list[ClientPresentationPreviewPosition]:
    return [
        ClientPresentationPreviewPosition(
            position_code=position.position_code,
            offer_code=offer.offer_code,
            sort_order=position.sort_order,
            position_type=position.position_type,
            is_featured=position.is_featured,
            is_active=position.is_active,
        )
        for position, offer in list_section_position_rows(session, section.id)
    ]


def get_client_presentation_preview(
    session: Session,
    *,
    page_code: str,
    surface_code: str | None = None,
) -> ClientPresentationPreviewResponse:
    page = get_page_by_code(session, page_code)
    if page is None:
        raise ClientPresentationPageNotFoundError("client_page_not_found")

    region_rows = list_region_rows_by_page_id(session, page.id)
    sections = {section.section_code: section for section, _group in list_section_rows(session)}
    region_blocks = [
        region_block for region_block, _region, _page in list_region_block_rows(session)
    ]
    bindings = list_data_bindings(session)
    visibility_rules = list_visibility_rules(session)
    action_policies = list_action_policies(session)
    tracking_policies = list_tracking_policies(session)

    preview_regions: list[ClientPresentationPreviewRegion] = []

    for region, _page in region_rows:
        allowed_block_types = _as_list(region.allowed_block_types)
        blocks: list[ClientPresentationPreviewBlock] = []

        for region_block in region_blocks:
            if region_block.region_id != region.id:
                continue
            if allowed_block_types and region_block.block_type not in allowed_block_types:
                continue

            section = (
                sections.get(region_block.content_source_ref)
                if region_block.content_source_type == "storefront_section"
                and region_block.content_source_ref is not None
                else None
            )
            layout = get_layout_by_section_id(session, section.id) if section is not None else None
            data_binding_codes = [
                binding.binding_code
                for binding in bindings
                if (
                    binding.target_type == "block_type"
                    and binding.target_code == region_block.block_type
                )
                or (binding.target_type == "region" and binding.target_code == region.region_code)
                or (
                    binding.target_type == "region_block"
                    and binding.target_code == region_block.block_code
                )
                or (
                    section is not None
                    and binding.target_type == "section"
                    and binding.target_code == section.section_code
                )
            ]
            visibility_rule_codes = [
                rule.rule_code
                for rule in visibility_rules
                if rule.target_type == "global"
                or (rule.target_type == "region" and rule.target_code == region.region_code)
                or (
                    rule.target_type == "block_type" and rule.target_code == region_block.block_type
                )
                or (
                    rule.target_type == "region_block"
                    and rule.target_code == region_block.block_code
                )
                or (
                    section is not None
                    and rule.target_type == "section"
                    and rule.target_code == section.section_code
                )
            ]
            action_policy_codes = [
                policy.policy_code
                for policy in action_policies
                if (
                    policy.target_type == "block_type"
                    and policy.target_code == region_block.block_type
                )
                or (
                    policy.target_type == "region_block"
                    and policy.target_code == region_block.block_code
                )
            ]
            tracking_policy_codes = [
                policy.policy_code
                for policy in tracking_policies
                if (
                    policy.target_type == "block_type"
                    and policy.target_code == region_block.block_type
                )
                or (
                    policy.target_type == "region_block"
                    and policy.target_code == region_block.block_code
                )
            ]

            blocks.append(
                ClientPresentationPreviewBlock(
                    block_code=region_block.block_code,
                    block_type=region_block.block_type,
                    renderer_key=region_block.renderer_key,
                    title=region_block.title,
                    layout=_layout_payload(layout),
                    content_source_type=region_block.content_source_type,
                    content_source_ref=region_block.content_source_ref,
                    content_payload=region_block.content_payload,
                    data_binding_codes=data_binding_codes,
                    visibility_rule_codes=visibility_rule_codes,
                    action_policy_codes=action_policy_codes,
                    tracking_policy_codes=tracking_policy_codes,
                    positions=_preview_positions(session, section) if section is not None else [],
                )
            )

        preview_regions.append(
            ClientPresentationPreviewRegion(
                region_code=region.region_code,
                region_type=region.region_type,
                title=region.title,
                sort_order=region.sort_order,
                allowed_block_types=allowed_block_types,
                blocks=blocks,
            )
        )

    return ClientPresentationPreviewResponse(
        page_code=page.page_code,
        surface_code=surface_code,
        generated_from="owner",
        page=ClientPresentationPreviewPage(
            page_code=page.page_code,
            page_type=page.page_type,
            route_path=page.route_path,
            title=page.title,
            regions=preview_regions,
        ),
    )


def _page_region_blocks(
    session: Session,
    page: ClientPresentationPage,
) -> list[ClientPresentationRegionBlock]:
    region_ids = {region.id for region, _page in list_region_rows_by_page_id(session, page.id)}
    return [
        region_block
        for region_block, _region, _page in list_region_block_rows(session)
        if region_block.region_id in region_ids
    ]


def get_client_presentation_pc_web_home_draft(
    session: Session,
) -> ClientPresentationHomeDraftResponse:
    page_code = "home"
    surface_code = "web_desktop"

    page = get_page_by_code(session, page_code)
    if page is None:
        raise ClientPresentationPageNotFoundError("client_page_not_found")

    surface = get_surface_by_code(session, surface_code)
    if surface is None:
        raise ClientPresentationPageNotFoundError("client_surface_not_found")

    preview = get_client_presentation_preview(
        session,
        page_code=page_code,
        surface_code=surface_code,
    )
    validation = get_client_presentation_validation_report(session)
    runtime_status = get_client_presentation_publish_runtime_status(session)

    page_region_blocks = _page_region_blocks(session, page)
    region_block_count = len(page_region_blocks)
    active_region_block_count = sum(1 for row in page_region_blocks if row.is_active)
    visible_region_block_count = sum(
        1 for row in page_region_blocks if row.is_active and row.display_status == "visible"
    )

    summary = ClientPresentationHomeDraftSummary(
        surface_code=surface.surface_code,
        page_code=page.page_code,
        region_count=len(preview.page.regions),
        region_block_count=region_block_count,
        active_region_block_count=active_region_block_count,
        visible_region_block_count=visible_region_block_count,
        validation_blocking_issue_count=validation.blocking_issue_count,
        runtime_sync_status=runtime_status.runtime_sync_status,
        latest_publish_version=runtime_status.latest_publish_version,
    )

    return ClientPresentationHomeDraftResponse(
        surface_code=surface.surface_code,
        page_code=page.page_code,
        generated_from="owner",
        summary=summary,
        page=preview.page,
        validation=validation,
        runtime_status=runtime_status,
    )


def _home_region_form_fields() -> list[ClientPresentationPlannerField]:
    return [
        ClientPresentationPlannerField(
            name="region_type",
            label="区域类型",
            control="select",
            required=True,
            options=[
                _planner_option(
                    value=key, label=str(value["label"]), description=str(value["description"])
                )
                for key, value in HOME_REGION_TYPE_RULES.items()
            ],
        ),
        ClientPresentationPlannerField(
            name="title",
            label="区域名称",
            control="input",
            input_type="text",
            required=True,
            max_length=160,
        ),
        ClientPresentationPlannerField(
            name="description",
            label="区域说明",
            control="textarea",
            input_type="text",
        ),
        ClientPresentationPlannerField(
            name="sort_order",
            label="排序",
            control="input",
            input_type="number",
            required=True,
            default_value=100,
            min_value=0,
        ),
        ClientPresentationPlannerField(
            name="max_blocks",
            label="最大 Block 数",
            control="input",
            input_type="number",
            min_value=1,
        ),
        ClientPresentationPlannerField(
            name="display_status",
            label="展示状态",
            control="select",
            required=True,
            default_value="visible",
            options=[
                _planner_option("visible", "可见"),
                _planner_option("hidden", "隐藏"),
            ],
        ),
        ClientPresentationPlannerField(
            name="is_active",
            label="启用",
            control="select",
            required=True,
            default_value=True,
            options=[
                _planner_option("true", "启用"),
                _planner_option("false", "停用"),
            ],
        ),
    ]


def _home_block_fields(
    block_type: ClientPresentationBlockType,
) -> list[ClientPresentationPlannerField]:
    base_fields = [
        ClientPresentationPlannerField(
            name="title",
            label="Block 名称",
            control="input",
            input_type="text",
            required=True,
            max_length=160,
        ),
        ClientPresentationPlannerField(
            name="subtitle",
            label="副标题",
            control="input",
            input_type="text",
            max_length=240,
        ),
        ClientPresentationPlannerField(
            name="description",
            label="说明",
            control="textarea",
            input_type="text",
        ),
        ClientPresentationPlannerField(
            name="sort_order",
            label="排序",
            control="input",
            input_type="number",
            required=True,
            default_value=100,
            min_value=0,
        ),
        ClientPresentationPlannerField(
            name="display_status",
            label="展示状态",
            control="select",
            required=True,
            default_value="visible",
            options=[
                _planner_option("visible", "可见"),
                _planner_option("hidden", "隐藏"),
            ],
        ),
        ClientPresentationPlannerField(
            name="is_active",
            label="启用",
            control="select",
            required=True,
            default_value=True,
            options=[
                _planner_option("true", "启用"),
                _planner_option("false", "停用"),
            ],
        ),
        ClientPresentationPlannerField(
            name="content_source_type",
            label="内容来源",
            control="select",
            required=True,
            default_value=HOME_BLOCK_SOURCE_TYPES.get(block_type.block_type, ["manual_inline"])[0],
            options=[
                _planner_option(value=source_type, label=source_type)
                for source_type in HOME_BLOCK_SOURCE_TYPES.get(
                    block_type.block_type, ["manual_inline"]
                )
            ],
        ),
        ClientPresentationPlannerField(
            name="content_source_ref",
            label="内容来源引用",
            control="input",
            input_type="text",
            max_length=160,
        ),
    ]

    if block_type.block_type == "title":
        base_fields.extend(
            [
                ClientPresentationPlannerField(
                    name="content_payload.title",
                    label="标题文案",
                    control="input",
                    input_type="text",
                    required=True,
                    max_length=160,
                ),
                ClientPresentationPlannerField(
                    name="content_payload.subtitle",
                    label="副标题文案",
                    control="input",
                    input_type="text",
                    max_length=240,
                ),
            ]
        )

    if block_type.block_type == "ad_banner":
        base_fields.extend(
            [
                ClientPresentationPlannerField(
                    name="content_payload.items[0].image_url",
                    label="广告图片 URL",
                    control="input",
                    input_type="url",
                    required=True,
                ),
                ClientPresentationPlannerField(
                    name="content_payload.items[0].link_ref",
                    label="跳转目标",
                    control="input",
                    input_type="text",
                ),
            ]
        )

    return base_fields


def get_client_presentation_pc_web_home_planner_options(
    session: Session,
) -> ClientPresentationHomePlannerOptionsResponse:
    page = get_page_by_code(session, HOME_PAGE_CODE)
    if page is None:
        raise ClientPresentationPageNotFoundError("client_page_not_found")

    surface = get_surface_by_code(session, PC_WEB_SURFACE_CODE)
    if surface is None:
        raise ClientPresentationPageNotFoundError("client_surface_not_found")

    region_types = [
        ClientPresentationPlannerRegionTypeOption(
            region_type=region_type,
            display_name=str(rule["label"]),
            description=str(rule["description"]),
            allowed_block_types=list(rule["allowed_block_types"]),
            default_max_blocks=rule["default_max_blocks"],
            default_is_required=bool(rule["default_is_required"]),
        )
        for region_type, rule in HOME_REGION_TYPE_RULES.items()
    ]

    allowed_home_block_types = _home_allowed_block_type_set()
    supported_renderer_keys = set(_as_list(surface.supported_renderer_keys))
    block_types = [
        ClientPresentationPlannerBlockTypeOption(
            block_type=block_type.block_type,
            display_name=block_type.display_name,
            description=block_type.description,
            renderer_key=block_type.renderer_key,
            allowed_region_types=_as_list(block_type.allowed_region_types),
            allowed_content_types=_as_list(block_type.allowed_content_types),
            content_source_types=HOME_BLOCK_SOURCE_TYPES.get(
                block_type.block_type,
                ["manual_inline"],
            ),
            fields=_home_block_fields(block_type),
        )
        for block_type in list_block_types(session)
        if block_type.is_active
        and block_type.display_status == "visible"
        and block_type.block_type in allowed_home_block_types
        and block_type.renderer_key in supported_renderer_keys
    ]

    return ClientPresentationHomePlannerOptionsResponse(
        surface_code=surface.surface_code,
        page_code=page.page_code,
        region_types=region_types,
        block_types=block_types,
        region_form_fields=_home_region_form_fields(),
        system_fields=[
            "page_code",
            "surface_code",
            "region_code",
            "allowed_block_types",
            "block_code",
            "renderer_key",
        ],
    )


def create_client_presentation_pc_web_home_region(
    session: Session,
    payload: ClientPresentationHomeRegionCreateRequest,
) -> ClientPresentationHomeDraftResponse:
    page = get_page_by_code(session, HOME_PAGE_CODE)
    if page is None:
        raise ClientPresentationPageNotFoundError("client_page_not_found")

    rule = _home_region_rule(payload.region_type)
    region = ClientPresentationRegion(
        page_id=page.id,
        region_code=_next_home_region_code(session, payload.region_type),
        region_type=payload.region_type,
        title=payload.title,
        description=payload.description,
        sort_order=payload.sort_order,
        is_required=(
            bool(rule["default_is_required"])
            if payload.is_required is None
            else payload.is_required
        ),
        max_blocks=(
            rule["default_max_blocks"] if payload.max_blocks is None else payload.max_blocks
        ),
        allowed_block_types=list(rule["allowed_block_types"]),
        display_status=payload.display_status,
        is_active=payload.is_active,
        source_type="planner",
        source_ref="pc_web_home_planner",
    )

    try:
        create_region(session, region)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ClientPresentationDuplicateCodeError("client_region_already_exists") from exc

    return get_client_presentation_pc_web_home_draft(session)


def update_client_presentation_pc_web_home_region(
    session: Session,
    region_code: str,
    payload: ClientPresentationHomeRegionUpdateRequest,
) -> ClientPresentationHomeDraftResponse:
    region = get_region_by_code(session, region_code)
    if region is None:
        raise ClientPresentationPageNotFoundError("client_region_not_found")
    _assert_home_region(region)

    if _field_was_set(payload, "title") and payload.title is not None:
        region.title = payload.title
    if _field_was_set(payload, "description"):
        region.description = payload.description
    if _field_was_set(payload, "sort_order") and payload.sort_order is not None:
        region.sort_order = payload.sort_order
    if _field_was_set(payload, "is_required") and payload.is_required is not None:
        region.is_required = payload.is_required
    if _field_was_set(payload, "max_blocks"):
        region.max_blocks = payload.max_blocks
    if _field_was_set(payload, "display_status") and payload.display_status is not None:
        region.display_status = payload.display_status
    if _field_was_set(payload, "is_active") and payload.is_active is not None:
        region.is_active = payload.is_active

    update_region(session, region)
    session.commit()
    return get_client_presentation_pc_web_home_draft(session)


def create_client_presentation_pc_web_home_block(
    session: Session,
    region_code: str,
    payload: ClientPresentationHomeBlockCreateRequest,
) -> ClientPresentationHomeDraftResponse:
    region = get_region_by_code(session, region_code)
    if region is None:
        raise ClientPresentationPageNotFoundError("client_region_not_found")
    _assert_home_region(region)

    block_type = get_block_type_by_code(session, payload.block_type)
    if block_type is None:
        raise ClientPresentationPlannerValidationError("home_block_type_not_registered")

    allowed = _as_list(region.allowed_block_types)
    if allowed and payload.block_type not in allowed:
        raise ClientPresentationPlannerValidationError("home_block_type_not_allowed")

    _validate_home_visible_range(payload.visible_from, payload.visible_until)
    _validate_home_block_content(
        block_type=payload.block_type,
        content_source_type=payload.content_source_type,
        content_source_ref=payload.content_source_ref,
        content_payload=payload.content_payload,
    )

    region_block = ClientPresentationRegionBlock(
        region_id=region.id,
        block_code=_next_home_block_code(session, region.region_code, payload.block_type),
        block_type=payload.block_type,
        renderer_key=block_type.renderer_key,
        title=payload.title,
        subtitle=payload.subtitle,
        description=payload.description,
        sort_order=payload.sort_order,
        display_status=payload.display_status,
        is_active=payload.is_active,
        visible_from=payload.visible_from,
        visible_until=payload.visible_until,
        content_source_type=payload.content_source_type,
        content_source_ref=payload.content_source_ref,
        content_payload=payload.content_payload,
        source_type="planner",
        source_ref="pc_web_home_planner",
    )

    try:
        create_region_block(session, region_block)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ClientPresentationDuplicateCodeError("client_region_block_already_exists") from exc

    return get_client_presentation_pc_web_home_draft(session)


def update_client_presentation_pc_web_home_block(
    session: Session,
    block_code: str,
    payload: ClientPresentationHomeBlockUpdateRequest,
) -> ClientPresentationHomeDraftResponse:
    region_block = get_region_block_by_code(session, block_code)
    if region_block is None:
        raise ClientPresentationPageNotFoundError("client_region_block_not_found")

    region = session.get(ClientPresentationRegion, region_block.region_id)
    if region is None:
        raise ClientPresentationPageNotFoundError("client_region_not_found")
    _assert_home_region(region)

    if _field_was_set(payload, "title") and payload.title is not None:
        region_block.title = payload.title
    if _field_was_set(payload, "subtitle"):
        region_block.subtitle = payload.subtitle
    if _field_was_set(payload, "description"):
        region_block.description = payload.description
    if _field_was_set(payload, "sort_order") and payload.sort_order is not None:
        region_block.sort_order = payload.sort_order
    if _field_was_set(payload, "display_status") and payload.display_status is not None:
        region_block.display_status = payload.display_status
    if _field_was_set(payload, "is_active") and payload.is_active is not None:
        region_block.is_active = payload.is_active
    if _field_was_set(payload, "visible_from"):
        region_block.visible_from = payload.visible_from
    if _field_was_set(payload, "visible_until"):
        region_block.visible_until = payload.visible_until
    if _field_was_set(payload, "content_source_type") and payload.content_source_type is not None:
        region_block.content_source_type = payload.content_source_type
    if _field_was_set(payload, "content_source_ref"):
        region_block.content_source_ref = payload.content_source_ref
    if _field_was_set(payload, "content_payload"):
        region_block.content_payload = payload.content_payload

    _validate_home_visible_range(region_block.visible_from, region_block.visible_until)
    _validate_home_block_content(
        block_type=region_block.block_type,
        content_source_type=region_block.content_source_type,
        content_source_ref=region_block.content_source_ref,
        content_payload=region_block.content_payload,
    )

    update_region_block(session, region_block)
    session.commit()
    return get_client_presentation_pc_web_home_draft(session)


def get_client_presentation_publish_runtime_status(
    session: Session,
) -> ClientPresentationPublishRuntimeStatusResponse:
    latest = _latest_publish_version(session)
    publish_version = latest.publish_version if latest is not None else None

    snapshot_counts = [
        ClientPresentationRuntimeSnapshotCount(
            name="client_pages",
            owner_count=_count_owner(session, ClientPresentationPage),
            latest_snapshot_count=_count_snapshot(session, PublishedClientPage, publish_version),
        ),
        ClientPresentationRuntimeSnapshotCount(
            name="client_regions",
            owner_count=_count_owner(session, ClientPresentationRegion),
            latest_snapshot_count=_count_snapshot(session, PublishedClientRegion, publish_version),
        ),
        ClientPresentationRuntimeSnapshotCount(
            name="client_block_types",
            owner_count=_count_owner(session, ClientPresentationBlockType),
            latest_snapshot_count=_count_snapshot(
                session, PublishedClientBlockType, publish_version
            ),
        ),
        ClientPresentationRuntimeSnapshotCount(
            name="client_region_blocks",
            owner_count=_count_owner(session, ClientPresentationRegionBlock),
            latest_snapshot_count=_count_snapshot(
                session, PublishedClientRegionBlock, publish_version
            ),
        ),
        ClientPresentationRuntimeSnapshotCount(
            name="client_surfaces",
            owner_count=_count_owner(session, ClientPresentationSurface),
            latest_snapshot_count=_count_snapshot(session, PublishedClientSurface, publish_version),
        ),
        ClientPresentationRuntimeSnapshotCount(
            name="client_data_bindings",
            owner_count=_count_owner(session, ClientPresentationDataBinding),
            latest_snapshot_count=_count_snapshot(
                session, PublishedClientDataBinding, publish_version
            ),
        ),
        ClientPresentationRuntimeSnapshotCount(
            name="client_visibility_rules",
            owner_count=_count_owner(session, ClientPresentationVisibilityRule),
            latest_snapshot_count=_count_snapshot(
                session, PublishedClientVisibilityRule, publish_version
            ),
        ),
        ClientPresentationRuntimeSnapshotCount(
            name="client_action_policies",
            owner_count=_count_owner(session, ClientPresentationActionPolicy),
            latest_snapshot_count=_count_snapshot(
                session, PublishedClientActionPolicy, publish_version
            ),
        ),
        ClientPresentationRuntimeSnapshotCount(
            name="client_tracking_policies",
            owner_count=_count_owner(session, ClientPresentationTrackingPolicy),
            latest_snapshot_count=_count_snapshot(
                session, PublishedClientTrackingPolicy, publish_version
            ),
        ),
        ClientPresentationRuntimeSnapshotCount(
            name="storefront_sections",
            owner_count=_count_owner(session, StorefrontSection),
            latest_snapshot_count=_count_snapshot(
                session, PublishedStorefrontSection, publish_version
            ),
        ),
        ClientPresentationRuntimeSnapshotCount(
            name="storefront_section_layouts",
            owner_count=_count_owner(session, StorefrontSectionLayout),
            latest_snapshot_count=_count_snapshot(
                session, PublishedStorefrontSectionLayout, publish_version
            ),
        ),
        ClientPresentationRuntimeSnapshotCount(
            name="storefront_section_positions",
            owner_count=_count_owner(session, StorefrontSectionPosition),
            latest_snapshot_count=_count_snapshot(
                session, PublishedStorefrontSectionPosition, publish_version
            ),
        ),
    ]

    return ClientPresentationPublishRuntimeStatusResponse(
        latest_publish_version=publish_version,
        latest_published_at=latest.published_at if latest is not None else None,
        runtime_sync_status="backoffice_snapshot_ready",
        runtime_sync_note=(
            "d2c-backoffice-api owns publish snapshots; d2c-api runtime sync status "
            "is verified by downstream sync jobs."
        ),
        snapshot_counts=snapshot_counts,
    )
