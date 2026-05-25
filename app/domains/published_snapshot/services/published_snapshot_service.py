"""Published snapshot generation and read services."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.domains.publish.models.publish_version import PublishVersion
from app.domains.published_export.contracts.published_export_contract import (
    PublishedCouponSnapshotExport,
    PublishedCouponsSnapshotExportResponse,
    PublishedGroupExport,
    PublishedGroupsExportResponse,
    PublishedOfferComponentsExportResponse,
    PublishedOfferComponentSnapshotExport,
    PublishedOfferPositionsExportResponse,
    PublishedOfferPositionSnapshotExport,
    PublishedOfferPricesExportResponse,
    PublishedOfferPriceSnapshotExport,
    PublishedOffersExportResponse,
    PublishedOfferSnapshotExport,
    PublishedPromotionRulesExportResponse,
    PublishedPromotionRuleSnapshotExport,
    PublishedPromotionTargetsExportResponse,
    PublishedPromotionTargetSnapshotExport,
    PublishedStorefrontSectionLayoutsExportResponse,
    PublishedStorefrontSectionLayoutSnapshotExport,
    PublishedStorefrontSectionsExportResponse,
    PublishedStorefrontSectionSnapshotExport,
)
from app.domains.published_snapshot.models.published_snapshot import (
    PublishedCoupon,
    PublishedGroup,
    PublishedOffer,
    PublishedOfferComponent,
    PublishedOfferPosition,
    PublishedOfferPrice,
    PublishedPromotionRule,
    PublishedPromotionTarget,
    PublishedStorefrontSection,
    PublishedStorefrontSectionLayout,
)
from app.domains.published_snapshot.repos.published_snapshot_repo import (
    add_publish_version,
    add_published_rows,
    delete_snapshot_by_version,
    latest_publish_version,
    list_owner_components,
    list_owner_coupons,
    list_owner_groups,
    list_owner_offers,
    list_owner_positions,
    list_owner_prices,
    list_owner_promotion_rules,
    list_owner_promotion_targets,
    list_owner_storefront_section_layout_rows,
    list_owner_storefront_section_rows,
    list_published_components,
    list_published_coupons,
    list_published_groups,
    list_published_offers,
    list_published_positions,
    list_published_prices,
    list_published_rules,
    list_published_storefront_section_layouts,
    list_published_storefront_sections,
    list_published_targets,
)


def generate_publish_version() -> str:
    return f"pub_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"


def create_storefront_snapshot(
    session: Session,
    *,
    publish_version: str | None = None,
    published_by: str | None = None,
    note: str | None = None,
) -> PublishVersion:
    now = datetime.now(UTC)
    resolved_version = publish_version or generate_publish_version()

    delete_snapshot_by_version(session, resolved_version)

    version = PublishVersion(
        publish_version=resolved_version,
        publish_scope="storefront",
        status="published",
        source="manual",
        started_at=now,
        published_at=now,
        published_by=published_by,
        note=note,
    )
    add_publish_version(session, version)

    rows: list[object] = []

    for group in list_owner_groups(session):
        rows.append(
            PublishedGroup(
                publish_version=resolved_version,
                group_code=group.group_code,
                group_name=group.group_name,
                group_kind=group.group_kind,
                description=group.description,
                image_url=group.image_url,
                sort_order=group.sort_order,
                display_status=group.display_status,
                is_active=group.is_active,
                source_group_id=group.id,
                raw_payload={"source": "d2c_groups", "source_group_id": group.id},
                published_at=now,
            )
        )

    for section, group in list_owner_storefront_section_rows(session):
        rows.append(
            PublishedStorefrontSection(
                publish_version=resolved_version,
                section_code=section.section_code,
                section_type=section.section_type,
                group_code=group.group_code if group is not None else None,
                title=section.title,
                subtitle=section.subtitle,
                description=section.description,
                sort_order=section.sort_order,
                display_status=section.display_status,
                is_active=section.is_active,
                source_section_id=section.id,
                raw_payload={"source": "d2c_storefront_sections", "source_section_id": section.id},
                published_at=now,
            )
        )

    for layout, section in list_owner_storefront_section_layout_rows(session):
        rows.append(
            PublishedStorefrontSectionLayout(
                publish_version=resolved_version,
                section_code=section.section_code,
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
                source_layout_id=layout.id,
                raw_payload={
                    "source": "d2c_storefront_section_layouts",
                    "source_layout_id": layout.id,
                },
                published_at=now,
            )
        )

    for offer in list_owner_offers(session):
        rows.append(
            PublishedOffer(
                publish_version=resolved_version,
                offer_code=offer.offer_code,
                offer_type=offer.offer_type,
                title=offer.title,
                subtitle=offer.subtitle,
                description=offer.description,
                image_url=offer.image_url,
                display_status=offer.display_status,
                sell_status=offer.sell_status,
                source_offer_id=offer.id,
                raw_payload={"source": "d2c_offers", "source_offer_id": offer.id},
                published_at=now,
            )
        )

    for component, offer in list_owner_components(session):
        rows.append(
            PublishedOfferComponent(
                publish_version=resolved_version,
                offer_code=offer.offer_code,
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
                source_component_id=component.id,
                raw_payload=component.raw_payload,
                published_at=now,
            )
        )

    for price, offer in list_owner_prices(session):
        rows.append(
            PublishedOfferPrice(
                publish_version=resolved_version,
                offer_code=offer.offer_code,
                price_code=price.price_code,
                channel=price.channel,
                currency=price.currency,
                price_cents=price.price_cents,
                compare_at_price_cents=price.compare_at_price_cents,
                effective_from=price.effective_from,
                effective_until=price.effective_until,
                is_active=price.is_active,
                priority=price.priority,
                source_price_id=price.id,
                raw_payload={"source": "d2c_offer_prices", "source_price_id": price.id},
                published_at=now,
            )
        )

    for position, group, offer in list_owner_positions(session):
        rows.append(
            PublishedOfferPosition(
                publish_version=resolved_version,
                position_code=position.position_code,
                group_code=group.group_code,
                offer_code=offer.offer_code,
                sort_order=position.sort_order,
                position_source=position.position_source,
                is_featured=position.is_featured,
                visible_from=position.visible_from,
                visible_until=position.visible_until,
                is_active=position.is_active,
                source_position_id=position.id,
                raw_payload={"source": "d2c_offer_positions", "source_position_id": position.id},
                published_at=now,
            )
        )

    for rule in list_owner_promotion_rules(session):
        rows.append(
            PublishedPromotionRule(
                publish_version=resolved_version,
                promotion_code=rule.promotion_code,
                promotion_name=rule.promotion_name,
                description=rule.description,
                promotion_type=rule.promotion_type,
                discount_type=rule.discount_type,
                discount_value=rule.discount_value,
                threshold_amount_cents=rule.threshold_amount_cents,
                max_discount_cents=rule.max_discount_cents,
                currency=rule.currency,
                starts_at=rule.starts_at,
                ends_at=rule.ends_at,
                priority=rule.priority,
                stackable=rule.stackable,
                is_active=rule.is_active,
                display_badge=rule.display_badge,
                source_promotion_rule_id=rule.id,
                raw_payload={"source": "d2c_promotion_rules", "source_promotion_rule_id": rule.id},
                published_at=now,
            )
        )

    for target, rule in list_owner_promotion_targets(session):
        rows.append(
            PublishedPromotionTarget(
                publish_version=resolved_version,
                promotion_code=rule.promotion_code,
                target_type=target.target_type,
                target_id=target.target_id,
                target_code=target.target_code,
                source_target_id=target.id,
                raw_payload={"source": "d2c_promotion_targets", "source_target_id": target.id},
                published_at=now,
            )
        )

    for coupon, rule in list_owner_coupons(session):
        rows.append(
            PublishedCoupon(
                publish_version=resolved_version,
                coupon_code=coupon.coupon_code,
                coupon_name=coupon.coupon_name,
                promotion_code=rule.promotion_code,
                coupon_type=coupon.coupon_type,
                total_limit=coupon.total_limit,
                per_customer_limit=coupon.per_customer_limit,
                starts_at=coupon.starts_at,
                ends_at=coupon.ends_at,
                is_active=coupon.is_active,
                source_coupon_id=coupon.id,
                raw_payload={"source": "d2c_coupons", "source_coupon_id": coupon.id},
                published_at=now,
            )
        )

    add_published_rows(session, rows)
    session.commit()
    return version


def _version_or_none(session: Session, publish_version: str | None) -> PublishVersion | None:
    return latest_publish_version(session, publish_version)


def get_published_groups_snapshot(
    session: Session,
    publish_version: str | None,
) -> PublishedGroupsExportResponse:
    version = _version_or_none(session, publish_version)
    if version is None:
        return PublishedGroupsExportResponse(publish_version=None, count=0, groups=[])

    groups = [
        PublishedGroupExport(**row.__dict__)
        for row in list_published_groups(session, version.publish_version)
    ]
    return PublishedGroupsExportResponse(
        publish_version=version.publish_version,
        count=len(groups),
        groups=groups,
    )


def get_published_offers_snapshot(
    session: Session,
    publish_version: str | None,
) -> PublishedOffersExportResponse:
    version = _version_or_none(session, publish_version)
    if version is None:
        return PublishedOffersExportResponse(publish_version=None, count=0, offers=[])

    offers = [
        PublishedOfferSnapshotExport(**row.__dict__)
        for row in list_published_offers(session, version.publish_version)
    ]
    return PublishedOffersExportResponse(
        publish_version=version.publish_version,
        count=len(offers),
        offers=offers,
    )


def get_published_offer_components_snapshot(
    session: Session,
    publish_version: str | None,
) -> PublishedOfferComponentsExportResponse:
    version = _version_or_none(session, publish_version)
    if version is None:
        return PublishedOfferComponentsExportResponse(publish_version=None, count=0, components=[])

    components = [
        PublishedOfferComponentSnapshotExport(
            publish_version=row.publish_version,
            offer_code=row.offer_code,
            component_no=row.component_no,
            pms_item_id=row.pms_item_id,
            pms_sku=row.pms_sku,
            pms_sku_code_id=row.pms_sku_code_id,
            sku_code=row.sku_code,
            pms_item_uom_id=row.pms_item_uom_id,
            uom_code=row.uom_code,
            uom_name=row.uom_name,
            pms_barcode_id=row.pms_barcode_id,
            barcode=row.barcode,
            quantity=str(row.quantity),
            component_role=row.component_role,
            sort_order=row.sort_order,
            required=row.required,
            published_at=row.published_at,
            source_component_id=row.source_component_id,
            raw_payload=row.raw_payload,
        )
        for row in list_published_components(session, version.publish_version)
    ]
    return PublishedOfferComponentsExportResponse(
        publish_version=version.publish_version,
        count=len(components),
        components=components,
    )


def get_published_offer_prices_snapshot(
    session: Session,
    publish_version: str | None,
) -> PublishedOfferPricesExportResponse:
    version = _version_or_none(session, publish_version)
    if version is None:
        return PublishedOfferPricesExportResponse(publish_version=None, count=0, prices=[])

    prices = [
        PublishedOfferPriceSnapshotExport(**row.__dict__)
        for row in list_published_prices(session, version.publish_version)
    ]
    return PublishedOfferPricesExportResponse(
        publish_version=version.publish_version,
        count=len(prices),
        prices=prices,
    )


def get_published_offer_positions_snapshot(
    session: Session,
    publish_version: str | None,
) -> PublishedOfferPositionsExportResponse:
    version = _version_or_none(session, publish_version)
    if version is None:
        return PublishedOfferPositionsExportResponse(publish_version=None, count=0, positions=[])

    positions = [
        PublishedOfferPositionSnapshotExport(**row.__dict__)
        for row in list_published_positions(session, version.publish_version)
    ]
    return PublishedOfferPositionsExportResponse(
        publish_version=version.publish_version,
        count=len(positions),
        positions=positions,
    )


def get_published_promotion_rules_snapshot(
    session: Session,
    publish_version: str | None,
) -> PublishedPromotionRulesExportResponse:
    version = _version_or_none(session, publish_version)
    if version is None:
        return PublishedPromotionRulesExportResponse(
            publish_version=None,
            count=0,
            promotion_rules=[],
        )

    rules = [
        PublishedPromotionRuleSnapshotExport(**row.__dict__)
        for row in list_published_rules(session, version.publish_version)
    ]
    return PublishedPromotionRulesExportResponse(
        publish_version=version.publish_version,
        count=len(rules),
        promotion_rules=rules,
    )


def get_published_promotion_targets_snapshot(
    session: Session,
    publish_version: str | None,
) -> PublishedPromotionTargetsExportResponse:
    version = _version_or_none(session, publish_version)
    if version is None:
        return PublishedPromotionTargetsExportResponse(
            publish_version=None,
            count=0,
            promotion_targets=[],
        )

    targets = [
        PublishedPromotionTargetSnapshotExport(**row.__dict__)
        for row in list_published_targets(session, version.publish_version)
    ]
    return PublishedPromotionTargetsExportResponse(
        publish_version=version.publish_version,
        count=len(targets),
        promotion_targets=targets,
    )


def get_published_coupons_snapshot(
    session: Session,
    publish_version: str | None,
) -> PublishedCouponsSnapshotExportResponse:
    version = _version_or_none(session, publish_version)
    if version is None:
        return PublishedCouponsSnapshotExportResponse(publish_version=None, count=0, coupons=[])

    coupons = [
        PublishedCouponSnapshotExport(**row.__dict__)
        for row in list_published_coupons(session, version.publish_version)
    ]
    return PublishedCouponsSnapshotExportResponse(
        publish_version=version.publish_version,
        count=len(coupons),
        coupons=coupons,
    )


def get_published_storefront_sections_snapshot(
    session: Session,
    publish_version: str | None = None,
) -> PublishedStorefrontSectionsExportResponse:
    version = latest_publish_version(session, publish_version)
    if version is None:
        return PublishedStorefrontSectionsExportResponse(publish_version=None, count=0, sections=[])

    sections = [
        PublishedStorefrontSectionSnapshotExport(
            publish_version=row.publish_version,
            section_code=row.section_code,
            section_type=row.section_type,
            group_code=row.group_code,
            title=row.title,
            subtitle=row.subtitle,
            description=row.description,
            sort_order=row.sort_order,
            display_status=row.display_status,
            is_active=row.is_active,
            published_at=row.published_at,
            source_section_id=row.source_section_id,
            raw_payload=row.raw_payload,
        )
        for row in list_published_storefront_sections(session, version.publish_version)
    ]
    return PublishedStorefrontSectionsExportResponse(
        publish_version=version.publish_version,
        count=len(sections),
        sections=sections,
    )


def get_published_storefront_section_layouts_snapshot(
    session: Session,
    publish_version: str | None = None,
) -> PublishedStorefrontSectionLayoutsExportResponse:
    version = latest_publish_version(session, publish_version)
    if version is None:
        return PublishedStorefrontSectionLayoutsExportResponse(
            publish_version=None, count=0, layouts=[]
        )

    layouts = [
        PublishedStorefrontSectionLayoutSnapshotExport(
            publish_version=row.publish_version,
            section_code=row.section_code,
            display_type=row.display_type,
            columns_desktop=row.columns_desktop,
            columns_tablet=row.columns_tablet,
            columns_mobile=row.columns_mobile,
            card_size=row.card_size,
            image_ratio=row.image_ratio,
            show_promotion_badge=row.show_promotion_badge,
            show_sales_summary=row.show_sales_summary,
            show_review_summary=row.show_review_summary,
            show_compare_price=row.show_compare_price,
            show_quantity_stepper=row.show_quantity_stepper,
            max_items=row.max_items,
            published_at=row.published_at,
            source_layout_id=row.source_layout_id,
            raw_payload=row.raw_payload,
        )
        for row in list_published_storefront_section_layouts(session, version.publish_version)
    ]
    return PublishedStorefrontSectionLayoutsExportResponse(
        publish_version=version.publish_version,
        count=len(layouts),
        layouts=layouts,
    )
