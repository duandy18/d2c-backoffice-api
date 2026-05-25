"""Client presentation services."""

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
from app.domains.client_presentation.models.client_presentation import (
    ClientPresentationActionPolicy,
    ClientPresentationBlockType,
    ClientPresentationDataBinding,
    ClientPresentationPage,
    ClientPresentationRegion,
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
    create_surface,
    create_tracking_policy,
    create_visibility_rule,
    get_action_policy_by_code,
    get_block_type_by_code,
    get_data_binding_by_code,
    get_page_by_code,
    get_region_by_code,
    get_surface_by_code,
    get_tracking_policy_by_code,
    get_visibility_rule_by_code,
    list_action_policies,
    list_all_region_rows,
    list_block_types,
    list_data_bindings,
    list_pages,
    list_region_rows_by_page_id,
    list_surfaces,
    list_tracking_policies,
    list_visibility_rules,
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
            "d2c_published_client_surfaces",
            "d2c_published_client_data_bindings",
            "d2c_published_client_visibility_rules",
            "d2c_published_client_action_policies",
            "d2c_published_client_tracking_policies",
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
        raise ClientPresentationDuplicateCodeError(
            "client_data_binding_already_exists"
        ) from exc

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
        raise ClientPresentationDuplicateCodeError(
            "client_visibility_rule_already_exists"
        ) from exc

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
        raise ClientPresentationDuplicateCodeError(
            "client_action_policy_already_exists"
        ) from exc

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
        raise ClientPresentationDuplicateCodeError(
            "client_tracking_policy_already_exists"
        ) from exc

    return _build_tracking_policy_contract(policy)
