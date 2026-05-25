"""Backoffice storefront section repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.groups.models.group import Group
from app.domains.offers.models.offer import Offer
from app.domains.storefront_sections.models.storefront_section import (
    StorefrontSection,
    StorefrontSectionLayout,
    StorefrontSectionPosition,
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

def get_position_by_code(
    session: Session,
    position_code: str,
) -> StorefrontSectionPosition | None:
    return session.scalar(
        select(StorefrontSectionPosition).where(
            StorefrontSectionPosition.position_code == position_code
        )
    )


def list_section_position_rows(
    session: Session,
    section_id: int,
) -> list[tuple[StorefrontSectionPosition, Offer]]:
    statement = (
        select(StorefrontSectionPosition, Offer)
        .join(Offer, Offer.id == StorefrontSectionPosition.offer_id)
        .where(StorefrontSectionPosition.section_id == section_id)
        .order_by(StorefrontSectionPosition.sort_order, StorefrontSectionPosition.id)
    )
    return list(session.execute(statement).all())


def list_section_positions_by_offer_id(
    session: Session,
    offer_id: int,
) -> list[StorefrontSectionPosition]:
    statement = (
        select(StorefrontSectionPosition)
        .where(StorefrontSectionPosition.offer_id == offer_id)
        .order_by(StorefrontSectionPosition.sort_order, StorefrontSectionPosition.id)
    )
    return list(session.scalars(statement).all())


def create_position(
    session: Session,
    position: StorefrontSectionPosition,
) -> StorefrontSectionPosition:
    session.add(position)
    session.flush()
    return position
