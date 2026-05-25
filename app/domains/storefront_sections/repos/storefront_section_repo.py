"""Backoffice storefront section repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.groups.models.group import Group
from app.domains.storefront_sections.models.storefront_section import (
    StorefrontSection,
    StorefrontSectionLayout,
)


def get_section_by_code(session: Session, section_code: str) -> StorefrontSection | None:
    return session.scalar(
        select(StorefrontSection).where(StorefrontSection.section_code == section_code)
    )


def list_section_rows(session: Session) -> list[tuple[StorefrontSection, Group | None]]:
    statement = (
        select(StorefrontSection, Group)
        .outerjoin(Group, Group.id == StorefrontSection.group_id)
        .order_by(StorefrontSection.sort_order, StorefrontSection.id)
    )
    return list(session.execute(statement).all())


def create_section(session: Session, section: StorefrontSection) -> StorefrontSection:
    session.add(section)
    session.flush()
    return section


def get_layout_by_section_id(
    session: Session,
    section_id: int,
) -> StorefrontSectionLayout | None:
    return session.scalar(
        select(StorefrontSectionLayout).where(StorefrontSectionLayout.section_id == section_id)
    )


def create_layout(
    session: Session,
    layout: StorefrontSectionLayout,
) -> StorefrontSectionLayout:
    session.add(layout)
    session.flush()
    return layout
