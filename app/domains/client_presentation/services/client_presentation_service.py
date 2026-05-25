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
    ClientPresentationPageContract,
    ClientPresentationPageCreateRequest,
    ClientPresentationPagesResponse,
    ClientPresentationPreviewBlock,
    ClientPresentationPreviewPage,
    ClientPresentationPreviewPosition,
    ClientPresentationPreviewRegion,
    ClientPresentationPreviewResponse,
    ClientPresentationPublishRuntimeStatusResponse,
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
from app.domains.publish.models.publish_version import PublishVersion
from app.domains.published_snapshot.models.published_snapshot import (
    PublishedClientActionPolicy,
    PublishedClientBlockType,
    PublishedClientDataBinding,
    PublishedClientPage,
    PublishedClientRegion,
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



def _known_client_targets(session: Session) -> dict[str, set[str]]:
    pages = {row.page_code for row in list_pages(session)}
    regions = {row.region_code for row, _page in list_all_region_rows(session)}
    block_types = {row.block_type for row in list_block_types(session)}
    sections = {section.section_code for section, _group in list_section_rows(session)}
    return {
        "global": {"client_presentation"},
        "page": pages,
        "region": regions,
        "block_type": block_types,
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

    for surface in list_surfaces(session):
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
            "surfaces": len(list_surfaces(session)),
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
    sections = [section for section, _group in list_section_rows(session)]
    bindings = list_data_bindings(session)
    visibility_rules = list_visibility_rules(session)
    action_policies = list_action_policies(session)
    tracking_policies = list_tracking_policies(session)

    preview_regions: list[ClientPresentationPreviewRegion] = []

    for region, _page in region_rows:
        allowed_block_types = _as_list(region.allowed_block_types)
        blocks: list[ClientPresentationPreviewBlock] = []

        for section in sections:
            if section.section_type not in allowed_block_types:
                continue

            layout = get_layout_by_section_id(session, section.id)
            data_binding_codes = [
                binding.binding_code
                for binding in bindings
                if (
                    binding.target_type == "block_type"
                    and binding.target_code == section.section_type
                )
                or (binding.target_type == "region" and binding.target_code == region.region_code)
                or (
                    binding.target_type == "section"
                    and binding.target_code == section.section_code
                )
            ]
            visibility_rule_codes = [
                rule.rule_code
                for rule in visibility_rules
                if rule.target_type == "global"
                or (rule.target_type == "region" and rule.target_code == region.region_code)
                or (rule.target_type == "block_type" and rule.target_code == section.section_type)
                or (rule.target_type == "section" and rule.target_code == section.section_code)
            ]
            action_policy_codes = [
                policy.policy_code
                for policy in action_policies
                if policy.target_type == "block_type" and policy.target_code == section.section_type
            ]
            tracking_policy_codes = [
                policy.policy_code
                for policy in tracking_policies
                if policy.target_type == "block_type" and policy.target_code == section.section_type
            ]

            blocks.append(
                ClientPresentationPreviewBlock(
                    block_code=section.section_code,
                    block_type=section.section_type,
                    title=section.title,
                    layout=_layout_payload(layout),
                    data_binding_codes=data_binding_codes,
                    visibility_rule_codes=visibility_rule_codes,
                    action_policy_codes=action_policy_codes,
                    tracking_policy_codes=tracking_policy_codes,
                    positions=_preview_positions(session, section),
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
