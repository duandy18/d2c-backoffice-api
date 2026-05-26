"""Backoffice Offer services."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domains.groups.models.group import Group
from app.domains.groups.repos.group_repo import get_group_by_code
from app.domains.offers.contracts.offer_contract import (
    BackofficeOfferComponentContract,
    BackofficeOfferComponentCreateRequest,
    BackofficeOfferComponentsResponse,
    BackofficeOfferContract,
    BackofficeOfferCreateRequest,
    BackofficeOfferPositionContract,
    BackofficeOfferPositionCreateRequest,
    BackofficeOfferPositionsResponse,
    BackofficeOfferPriceContract,
    BackofficeOfferPriceCreateRequest,
    BackofficeOfferPricesResponse,
    BackofficeOfferPublishCheckResponse,
    BackofficeOffersResponse,
)
from app.domains.offers.models.offer import Offer, OfferComponent, OfferPosition, OfferPrice
from app.domains.offers.repos.offer_repo import (
    create_offer,
    create_offer_component,
    create_offer_position,
    create_offer_price,
    get_offer_by_code,
    list_offer_components,
    list_offer_positions,
    list_offer_prices,
    list_offers,
    next_component_no,
)
from app.domains.pms_projection.models import (
    PmsBarcodeProjection,
    PmsProductProjection,
    PmsSkuCodeProjection,
    PmsUnitProjection,
)
from app.domains.storefront_sections.repos.storefront_section_repo import (
    list_section_positions_by_offer_id,
)


class BackofficeOfferDuplicateCodeError(Exception):
    pass


class BackofficeOfferNotFoundError(Exception):
    pass


class BackofficeOfferInvalidRangeError(Exception):
    pass


class BackofficeOfferProjectionNotFoundError(Exception):
    pass


class BackofficeOfferGroupNotFoundError(Exception):
    pass


class BackofficeOfferPositionDuplicateError(Exception):
    pass


class BackofficeOfferPriceDuplicateError(Exception):
    pass


def _validate_range(start: object, end: object, error_code: str) -> None:
    if start is not None and end is not None and end <= start:  # type: ignore[operator]
        raise BackofficeOfferInvalidRangeError(error_code)


def build_offer_contract(offer: Offer) -> BackofficeOfferContract:
    return BackofficeOfferContract(
        id=offer.id,
        offer_code=offer.offer_code,
        offer_type=offer.offer_type,
        title=offer.title,
        subtitle=offer.subtitle,
        description=offer.description,
        image_url=offer.image_url,
        display_status=offer.display_status,
        sell_status=offer.sell_status,
        publish_status=offer.publish_status,
        source_type=offer.source_type,
        sort_order=offer.sort_order,
        visible_from=offer.visible_from,
        visible_until=offer.visible_until,
        created_at=offer.created_at,
        updated_at=offer.updated_at,
    )


def get_backoffice_offers(session: Session) -> BackofficeOffersResponse:
    offers = [build_offer_contract(offer) for offer in list_offers(session)]
    return BackofficeOffersResponse(count=len(offers), offers=offers)


def get_backoffice_offer(session: Session, offer_code: str) -> BackofficeOfferContract:
    offer = get_offer_by_code(session, offer_code)
    if offer is None:
        raise BackofficeOfferNotFoundError("offer_not_found")
    return build_offer_contract(offer)


def create_backoffice_offer(
    session: Session,
    payload: BackofficeOfferCreateRequest,
) -> BackofficeOfferContract:
    _validate_range(payload.visible_from, payload.visible_until, "offer_visible_range_invalid")

    if get_offer_by_code(session, payload.offer_code) is not None:
        raise BackofficeOfferDuplicateCodeError("offer_code_already_exists")

    offer = Offer(
        offer_code=payload.offer_code,
        offer_type=payload.offer_type,
        title=payload.title,
        subtitle=payload.subtitle,
        description=payload.description,
        image_url=payload.image_url,
        display_status=payload.display_status,
        sell_status=payload.sell_status,
        publish_status=payload.publish_status,
        source_type=payload.source_type,
        sort_order=payload.sort_order,
        visible_from=payload.visible_from,
        visible_until=payload.visible_until,
    )

    try:
        create_offer(session, offer)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise BackofficeOfferDuplicateCodeError("offer_code_already_exists") from exc

    return build_offer_contract(offer)


def _get_offer_or_raise(session: Session, offer_code: str) -> Offer:
    offer = get_offer_by_code(session, offer_code)
    if offer is None:
        raise BackofficeOfferNotFoundError("offer_not_found")
    return offer


def _get_product(session: Session, pms_item_id: int) -> PmsProductProjection:
    row = session.scalar(
        select(PmsProductProjection).where(PmsProductProjection.pms_item_id == pms_item_id)
    )
    if row is None:
        raise BackofficeOfferProjectionNotFoundError("pms_product_projection_not_found")
    return row


def _get_sku_code(session: Session, pms_sku_code_id: int) -> PmsSkuCodeProjection:
    row = session.scalar(
        select(PmsSkuCodeProjection).where(PmsSkuCodeProjection.pms_sku_code_id == pms_sku_code_id)
    )
    if row is None:
        raise BackofficeOfferProjectionNotFoundError("pms_sku_code_projection_not_found")
    return row


def _get_unit(session: Session, pms_item_uom_id: int) -> PmsUnitProjection:
    row = session.scalar(
        select(PmsUnitProjection).where(PmsUnitProjection.pms_item_uom_id == pms_item_uom_id)
    )
    if row is None:
        raise BackofficeOfferProjectionNotFoundError("pms_unit_projection_not_found")
    return row


def _get_barcode(session: Session, pms_barcode_id: int | None) -> PmsBarcodeProjection | None:
    if pms_barcode_id is None:
        return None

    row = session.scalar(
        select(PmsBarcodeProjection).where(PmsBarcodeProjection.pms_barcode_id == pms_barcode_id)
    )
    if row is None:
        raise BackofficeOfferProjectionNotFoundError("pms_barcode_projection_not_found")
    return row


def build_component_contract(component: OfferComponent) -> BackofficeOfferComponentContract:
    return BackofficeOfferComponentContract(
        id=component.id,
        offer_id=component.offer_id,
        component_no=component.component_no,
        pms_item_id=component.pms_item_id,
        pms_sku=component.pms_sku,
        pms_sku_code_id=component.pms_sku_code_id,
        sku_code=component.sku_code,
        pms_item_uom_id=component.pms_item_uom_id,
        uom_code=component.uom_code,
        uom_name=component.uom_name,
        pms_barcode_id=component.pms_barcode_id,
        barcode=component.barcode,
        quantity=component.quantity,
        component_role=component.component_role,
        sort_order=component.sort_order,
        required=component.required,
        created_at=component.created_at,
        updated_at=component.updated_at,
    )


def get_backoffice_offer_components(
    session: Session,
    offer_code: str,
) -> BackofficeOfferComponentsResponse:
    offer = _get_offer_or_raise(session, offer_code)
    components = [
        build_component_contract(component)
        for component in list_offer_components(session, offer.id)
    ]
    return BackofficeOfferComponentsResponse(count=len(components), components=components)


def create_backoffice_offer_component(
    session: Session,
    offer_code: str,
    payload: BackofficeOfferComponentCreateRequest,
) -> BackofficeOfferComponentContract:
    offer = _get_offer_or_raise(session, offer_code)
    product = _get_product(session, payload.pms_item_id)
    sku_code = _get_sku_code(session, payload.pms_sku_code_id)
    unit = _get_unit(session, payload.pms_item_uom_id)
    barcode = _get_barcode(session, payload.pms_barcode_id)

    if sku_code.pms_item_id != product.pms_item_id:
        raise BackofficeOfferProjectionNotFoundError("pms_sku_code_item_mismatch")
    if unit.pms_item_id != product.pms_item_id:
        raise BackofficeOfferProjectionNotFoundError("pms_unit_item_mismatch")
    if barcode is not None and barcode.pms_item_id != product.pms_item_id:
        raise BackofficeOfferProjectionNotFoundError("pms_barcode_item_mismatch")

    component = OfferComponent(
        offer_id=offer.id,
        component_no=next_component_no(session, offer.id),
        pms_item_id=product.pms_item_id,
        pms_sku=product.pms_sku,
        pms_sku_code_id=sku_code.pms_sku_code_id,
        sku_code=sku_code.sku_code,
        pms_item_uom_id=unit.pms_item_uom_id,
        uom_code=unit.uom,
        uom_name=unit.display_name or unit.uom_name,
        pms_barcode_id=barcode.pms_barcode_id if barcode else None,
        barcode=barcode.barcode if barcode else None,
        quantity=payload.quantity,
        component_role=payload.component_role,
        sort_order=payload.sort_order,
        required=payload.required,
        raw_payload={
            "source": "d2c-backoffice-api",
            "pms_item_id": product.pms_item_id,
            "pms_sku_code_id": sku_code.pms_sku_code_id,
            "pms_item_uom_id": unit.pms_item_uom_id,
            "pms_barcode_id": barcode.pms_barcode_id if barcode else None,
        },
    )

    create_offer_component(session, component)
    session.commit()
    return build_component_contract(component)


def build_price_contract(price: OfferPrice) -> BackofficeOfferPriceContract:
    return BackofficeOfferPriceContract(
        id=price.id,
        offer_id=price.offer_id,
        price_code=price.price_code,
        channel=price.channel,
        currency=price.currency,
        price_cents=price.price_cents,
        compare_at_price_cents=price.compare_at_price_cents,
        effective_from=price.effective_from,
        effective_until=price.effective_until,
        is_active=price.is_active,
        priority=price.priority,
        created_at=price.created_at,
        updated_at=price.updated_at,
    )


def get_backoffice_offer_prices(
    session: Session,
    offer_code: str,
) -> BackofficeOfferPricesResponse:
    offer = _get_offer_or_raise(session, offer_code)
    prices = [build_price_contract(price) for price in list_offer_prices(session, offer.id)]
    return BackofficeOfferPricesResponse(count=len(prices), prices=prices)


def create_backoffice_offer_price(
    session: Session,
    offer_code: str,
    payload: BackofficeOfferPriceCreateRequest,
) -> BackofficeOfferPriceContract:
    offer = _get_offer_or_raise(session, offer_code)
    _validate_range(payload.effective_from, payload.effective_until, "offer_price_range_invalid")

    price = OfferPrice(
        offer_id=offer.id,
        price_code=payload.price_code,
        channel=payload.channel,
        currency=payload.currency.upper(),
        price_cents=payload.price_cents,
        compare_at_price_cents=payload.compare_at_price_cents,
        effective_from=payload.effective_from,
        effective_until=payload.effective_until,
        is_active=payload.is_active,
        priority=payload.priority,
    )

    try:
        create_offer_price(session, price)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise BackofficeOfferPriceDuplicateError("offer_price_code_already_exists") from exc

    return build_price_contract(price)


def build_position_contract(
    position: OfferPosition,
    group: Group,
    offer: Offer,
) -> BackofficeOfferPositionContract:
    return BackofficeOfferPositionContract(
        id=position.id,
        position_code=position.position_code,
        group_id=position.group_id,
        group_code=group.group_code,
        offer_id=position.offer_id,
        offer_code=offer.offer_code,
        sort_order=position.sort_order,
        position_source=position.position_source,
        is_featured=position.is_featured,
        visible_from=position.visible_from,
        visible_until=position.visible_until,
        is_active=position.is_active,
        created_at=position.created_at,
        updated_at=position.updated_at,
    )


def get_backoffice_offer_positions(
    session: Session,
    offer_code: str,
) -> BackofficeOfferPositionsResponse:
    offer = _get_offer_or_raise(session, offer_code)
    positions: list[BackofficeOfferPositionContract] = []

    for position in list_offer_positions(session, offer.id):
        group = session.get(Group, position.group_id)
        if group is None:
            raise BackofficeOfferGroupNotFoundError("group_not_found")
        positions.append(build_position_contract(position, group, offer))

    return BackofficeOfferPositionsResponse(count=len(positions), positions=positions)


def create_backoffice_offer_position(
    session: Session,
    offer_code: str,
    payload: BackofficeOfferPositionCreateRequest,
) -> BackofficeOfferPositionContract:
    offer = _get_offer_or_raise(session, offer_code)
    group = get_group_by_code(session, payload.group_code)
    if group is None:
        raise BackofficeOfferGroupNotFoundError("group_not_found")

    _validate_range(payload.visible_from, payload.visible_until, "offer_position_range_invalid")

    position = OfferPosition(
        position_code=payload.position_code,
        group_id=group.id,
        offer_id=offer.id,
        sort_order=payload.sort_order,
        position_source=payload.position_source,
        is_featured=payload.is_featured,
        visible_from=payload.visible_from,
        visible_until=payload.visible_until,
        is_active=payload.is_active,
    )

    try:
        create_offer_position(session, position)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise BackofficeOfferPositionDuplicateError("offer_position_already_exists") from exc

    return build_position_contract(position, group, offer)


def get_backoffice_offer_publish_check(
    session: Session,
    offer_code: str,
) -> BackofficeOfferPublishCheckResponse:
    offer = _get_offer_or_raise(session, offer_code)
    components = list_offer_components(session, offer.id)
    prices = list_offer_prices(session, offer.id)
    section_positions = list_section_positions_by_offer_id(session, offer.id)

    has_component = len(components) > 0
    has_active_price = any(price.is_active for price in prices)
    has_section_position = any(position.is_active for position in section_positions)
    has_title = bool(offer.title.strip())
    has_image = bool((offer.image_url or "").strip())
    is_visible = offer.display_status == "visible"
    is_sellable = offer.sell_status == "sellable"

    reasons: list[str] = []
    if not has_component:
        reasons.append("offer_component_required")
    if not has_active_price:
        reasons.append("offer_active_price_required")
    if not has_section_position:
        reasons.append("offer_section_position_required")
    if not has_title:
        reasons.append("offer_title_required")
    if not has_image:
        reasons.append("offer_image_required")
    if not is_visible:
        reasons.append("offer_display_status_must_be_visible")
    if not is_sellable:
        reasons.append("offer_sell_status_must_be_sellable")

    return BackofficeOfferPublishCheckResponse(
        offer_code=offer.offer_code,
        can_publish=len(reasons) == 0,
        blocking_reasons=reasons,
        has_component=has_component,
        has_active_price=has_active_price,
        has_section_position=has_section_position,
        has_title=has_title,
        has_image=has_image,
        is_visible=is_visible,
        is_sellable=is_sellable,
    )
