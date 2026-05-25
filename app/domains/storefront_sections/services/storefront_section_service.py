"""Backoffice storefront section services."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domains.groups.repos.group_repo import get_group_by_code
from app.domains.storefront_sections.contracts.storefront_section_contract import (
    BackofficeStorefrontSection,
    BackofficeStorefrontSectionCreateRequest,
    BackofficeStorefrontSectionLayout,
    BackofficeStorefrontSectionLayoutUpsertRequest,
    BackofficeStorefrontSectionsHealthResponse,
    BackofficeStorefrontSectionsResponse,
)
from app.domains.storefront_sections.models.storefront_section import (
    StorefrontSection,
    StorefrontSectionLayout,
)
from app.domains.storefront_sections.repos.storefront_section_repo import (
    create_layout,
    create_section,
    get_layout_by_section_id,
    get_section_by_code,
    list_section_rows,
)


class BackofficeStorefrontSectionDuplicateCodeError(Exception):
    pass


class BackofficeStorefrontSectionNotFoundError(Exception):
    pass


class BackofficeStorefrontSectionGroupNotFoundError(Exception):
    pass


def get_storefront_sections_health() -> BackofficeStorefrontSectionsHealthResponse:
    return BackofficeStorefrontSectionsHealthResponse(
        status="ok",
        module="storefront_sections",
        owner_tables=[
            "d2c_storefront_sections",
            "d2c_storefront_section_layouts",
        ],
    )


def _build_section_contract(
    section: StorefrontSection,
    group_code: str | None,
) -> BackofficeStorefrontSection:
    return BackofficeStorefrontSection(
        id=section.id,
        section_code=section.section_code,
        section_type=section.section_type,
        group_id=section.group_id,
        group_code=group_code,
        title=section.title,
        subtitle=section.subtitle,
        description=section.description,
        sort_order=section.sort_order,
        display_status=section.display_status,
        is_active=section.is_active,
        source_type=section.source_type,
        source_ref=section.source_ref,
        created_at=section.created_at,
        updated_at=section.updated_at,
    )


def get_backoffice_storefront_sections(session: Session) -> BackofficeStorefrontSectionsResponse:
    sections = [
        _build_section_contract(section, group.group_code if group is not None else None)
        for section, group in list_section_rows(session)
    ]
    return BackofficeStorefrontSectionsResponse(count=len(sections), sections=sections)


def create_backoffice_storefront_section(
    session: Session,
    payload: BackofficeStorefrontSectionCreateRequest,
) -> BackofficeStorefrontSection:
    if get_section_by_code(session, payload.section_code) is not None:
        raise BackofficeStorefrontSectionDuplicateCodeError("section_code_already_exists")

    group_id: int | None = None
    group_code: str | None = None
    if payload.group_code is not None:
        group = get_group_by_code(session, payload.group_code)
        if group is None:
            raise BackofficeStorefrontSectionGroupNotFoundError("group_not_found")
        group_id = group.id
        group_code = group.group_code

    section = StorefrontSection(
        section_code=payload.section_code,
        section_type=payload.section_type,
        group_id=group_id,
        title=payload.title,
        subtitle=payload.subtitle,
        description=payload.description,
        sort_order=payload.sort_order,
        display_status=payload.display_status,
        is_active=payload.is_active,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )

    try:
        create_section(session, section)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise BackofficeStorefrontSectionDuplicateCodeError("section_code_already_exists") from exc

    return _build_section_contract(section, group_code)


def _build_layout_contract(
    layout: StorefrontSectionLayout,
    section_code: str,
) -> BackofficeStorefrontSectionLayout:
    return BackofficeStorefrontSectionLayout(
        id=layout.id,
        section_id=layout.section_id,
        section_code=section_code,
        display_type=layout.display_type,
        columns_desktop=layout.columns_desktop,
        columns_tablet=layout.columns_tablet,
        columns_mobile=layout.columns_mobile,
        card_size=layout.card_size,
        image_ratio=layout.image_ratio,
        show_promotion_badge=layout.show_promotion_badge,
        show_sales_summary=layout.show_sales_summary,
        show_review_summary=layout.show_review_summary,
        show_compare_price=layout.show_compare_price,
        show_quantity_stepper=layout.show_quantity_stepper,
        max_items=layout.max_items,
        created_at=layout.created_at,
        updated_at=layout.updated_at,
    )


def upsert_backoffice_storefront_section_layout(
    session: Session,
    section_code: str,
    payload: BackofficeStorefrontSectionLayoutUpsertRequest,
) -> BackofficeStorefrontSectionLayout:
    section = get_section_by_code(session, section_code)
    if section is None:
        raise BackofficeStorefrontSectionNotFoundError("section_not_found")

    layout = get_layout_by_section_id(session, section.id)
    if layout is None:
        layout = StorefrontSectionLayout(
            section_id=section.id,
            display_type=payload.display_type,
            columns_desktop=payload.columns_desktop,
            columns_tablet=payload.columns_tablet,
            columns_mobile=payload.columns_mobile,
            card_size=payload.card_size,
            image_ratio=payload.image_ratio,
            show_promotion_badge=payload.show_promotion_badge,
            show_sales_summary=payload.show_sales_summary,
            show_review_summary=payload.show_review_summary,
            show_compare_price=payload.show_compare_price,
            show_quantity_stepper=payload.show_quantity_stepper,
            max_items=payload.max_items,
        )
        create_layout(session, layout)

    layout.display_type = payload.display_type
    layout.columns_desktop = payload.columns_desktop
    layout.columns_tablet = payload.columns_tablet
    layout.columns_mobile = payload.columns_mobile
    layout.card_size = payload.card_size
    layout.image_ratio = payload.image_ratio
    layout.show_promotion_badge = payload.show_promotion_badge
    layout.show_sales_summary = payload.show_sales_summary
    layout.show_review_summary = payload.show_review_summary
    layout.show_compare_price = payload.show_compare_price
    layout.show_quantity_stepper = payload.show_quantity_stepper
    layout.max_items = payload.max_items

    session.commit()
    return _build_layout_contract(layout, section.section_code)
