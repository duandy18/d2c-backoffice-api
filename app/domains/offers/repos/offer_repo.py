"""Backoffice Offer repositories."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domains.offers.models.offer import Offer, OfferComponent, OfferPosition, OfferPrice


def get_offer_by_code(session: Session, offer_code: str) -> Offer | None:
    return session.scalar(select(Offer).where(Offer.offer_code == offer_code))


def list_offers(session: Session) -> list[Offer]:
    statement = select(Offer).order_by(Offer.sort_order, Offer.id)
    return list(session.scalars(statement).all())


def create_offer(session: Session, offer: Offer) -> Offer:
    session.add(offer)
    session.flush()
    return offer


def next_component_no(session: Session, offer_id: int) -> int:
    value = session.scalar(
        select(func.coalesce(func.max(OfferComponent.component_no), 0)).where(
            OfferComponent.offer_id == offer_id
        )
    )
    return int(value or 0) + 1


def create_offer_component(session: Session, component: OfferComponent) -> OfferComponent:
    session.add(component)
    session.flush()
    return component


def create_offer_price(session: Session, price: OfferPrice) -> OfferPrice:
    session.add(price)
    session.flush()
    return price


def create_offer_position(session: Session, position: OfferPosition) -> OfferPosition:
    session.add(position)
    session.flush()
    return position


def list_offer_components(session: Session, offer_id: int) -> list[OfferComponent]:
    statement = (
        select(OfferComponent)
        .where(OfferComponent.offer_id == offer_id)
        .order_by(OfferComponent.sort_order, OfferComponent.id)
    )
    return list(session.scalars(statement).all())


def list_offer_prices(session: Session, offer_id: int) -> list[OfferPrice]:
    statement = (
        select(OfferPrice)
        .where(OfferPrice.offer_id == offer_id)
        .order_by(OfferPrice.is_active.desc(), OfferPrice.priority, OfferPrice.id)
    )
    return list(session.scalars(statement).all())


def list_offer_positions(session: Session, offer_id: int) -> list[OfferPosition]:
    statement = (
        select(OfferPosition)
        .where(OfferPosition.offer_id == offer_id)
        .order_by(OfferPosition.sort_order, OfferPosition.id)
    )
    return list(session.scalars(statement).all())
