"""Client presentation repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.client_presentation.models.client_presentation import (
    ClientPresentationBlockType,
    ClientPresentationPage,
    ClientPresentationRegion,
)


def get_page_by_code(session: Session, page_code: str) -> ClientPresentationPage | None:
    return session.scalar(
        select(ClientPresentationPage).where(ClientPresentationPage.page_code == page_code)
    )


def list_pages(session: Session) -> list[ClientPresentationPage]:
    return list(
        session.scalars(
            select(ClientPresentationPage).order_by(
                ClientPresentationPage.sort_order,
                ClientPresentationPage.id,
            )
        ).all()
    )


def create_page(
    session: Session,
    page: ClientPresentationPage,
) -> ClientPresentationPage:
    session.add(page)
    session.flush()
    return page


def get_region_by_code(session: Session, region_code: str) -> ClientPresentationRegion | None:
    return session.scalar(
        select(ClientPresentationRegion).where(
            ClientPresentationRegion.region_code == region_code
        )
    )


def list_region_rows_by_page_id(
    session: Session,
    page_id: int,
) -> list[tuple[ClientPresentationRegion, ClientPresentationPage]]:
    statement = (
        select(ClientPresentationRegion, ClientPresentationPage)
        .join(ClientPresentationPage, ClientPresentationPage.id == ClientPresentationRegion.page_id)
        .where(ClientPresentationRegion.page_id == page_id)
        .order_by(ClientPresentationRegion.sort_order, ClientPresentationRegion.id)
    )
    return list(session.execute(statement).all())


def list_all_region_rows(
    session: Session,
) -> list[tuple[ClientPresentationRegion, ClientPresentationPage]]:
    statement = (
        select(ClientPresentationRegion, ClientPresentationPage)
        .join(ClientPresentationPage, ClientPresentationPage.id == ClientPresentationRegion.page_id)
        .order_by(
            ClientPresentationPage.sort_order,
            ClientPresentationRegion.sort_order,
            ClientPresentationRegion.id,
        )
    )
    return list(session.execute(statement).all())


def create_region(
    session: Session,
    region: ClientPresentationRegion,
) -> ClientPresentationRegion:
    session.add(region)
    session.flush()
    return region


def get_block_type_by_code(
    session: Session,
    block_type: str,
) -> ClientPresentationBlockType | None:
    return session.scalar(
        select(ClientPresentationBlockType).where(
            ClientPresentationBlockType.block_type == block_type
        )
    )


def list_block_types(session: Session) -> list[ClientPresentationBlockType]:
    return list(
        session.scalars(
            select(ClientPresentationBlockType).order_by(
                ClientPresentationBlockType.block_type,
                ClientPresentationBlockType.id,
            )
        ).all()
    )


def create_block_type(
    session: Session,
    block_type: ClientPresentationBlockType,
) -> ClientPresentationBlockType:
    session.add(block_type)
    session.flush()
    return block_type
