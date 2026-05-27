"""Published snapshot repositories."""

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

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
from app.domains.groups.models.group import Group
from app.domains.offers.models.offer import Offer, OfferComponent, OfferPosition, OfferPrice
from app.domains.promotions.models.promotion_rule import Coupon, PromotionRule, PromotionTarget
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
    PublishedStorefrontSectionPosition,
)
from app.domains.storefront_sections.models.storefront_section import (
    StorefrontSection,
    StorefrontSectionLayout,
    StorefrontSectionPosition,
)


def add_publish_version(session: Session, publish_version: PublishVersion) -> PublishVersion:
    session.add(publish_version)
    session.flush()
    return publish_version


def delete_snapshot_by_version(session: Session, publish_version: str) -> None:
    for model in (
        PublishedClientActionPolicy,
        PublishedClientBlockType,
        PublishedClientDataBinding,
        PublishedClientSurface,
        PublishedClientTrackingPolicy,
        PublishedClientVisibilityRule,
        PublishedClientRegion,
        PublishedClientPage,
        PublishedCoupon,
        PublishedPromotionTarget,
        PublishedPromotionRule,
        PublishedStorefrontSectionPosition,
        PublishedStorefrontSectionLayout,
        PublishedStorefrontSection,
        PublishedOfferPosition,
        PublishedOfferPrice,
        PublishedOfferComponent,
        PublishedOffer,
        PublishedGroup,
    ):
        session.execute(delete(model).where(model.publish_version == publish_version))


def list_owner_client_pages(session: Session) -> list[ClientPresentationPage]:
    return list(
        session.scalars(
            select(ClientPresentationPage).order_by(
                ClientPresentationPage.sort_order,
                ClientPresentationPage.id,
            )
        ).all()
    )


def list_owner_client_regions(
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


def list_owner_client_region_blocks(
    session: Session,
) -> list[tuple[ClientPresentationRegionBlock, ClientPresentationRegion, ClientPresentationPage]]:
    statement = (
        select(ClientPresentationRegionBlock, ClientPresentationRegion, ClientPresentationPage)
        .join(
            ClientPresentationRegion,
            ClientPresentationRegion.id == ClientPresentationRegionBlock.region_id,
        )
        .join(ClientPresentationPage, ClientPresentationPage.id == ClientPresentationRegion.page_id)
        .order_by(
            ClientPresentationPage.sort_order,
            ClientPresentationRegion.sort_order,
            ClientPresentationRegionBlock.sort_order,
            ClientPresentationRegionBlock.id,
        )
    )
    return list(session.execute(statement).all())


def list_owner_client_block_types(session: Session) -> list[ClientPresentationBlockType]:
    return list(
        session.scalars(
            select(ClientPresentationBlockType).order_by(
                ClientPresentationBlockType.block_type,
                ClientPresentationBlockType.id,
            )
        ).all()
    )


def list_owner_client_surfaces(session: Session) -> list[ClientPresentationSurface]:
    return list(
        session.scalars(
            select(ClientPresentationSurface).order_by(
                ClientPresentationSurface.surface_code,
                ClientPresentationSurface.id,
            )
        ).all()
    )


def list_owner_client_data_bindings(session: Session) -> list[ClientPresentationDataBinding]:
    return list(
        session.scalars(
            select(ClientPresentationDataBinding).order_by(
                ClientPresentationDataBinding.target_type,
                ClientPresentationDataBinding.target_code,
                ClientPresentationDataBinding.binding_code,
            )
        ).all()
    )


def list_owner_client_visibility_rules(
    session: Session,
) -> list[ClientPresentationVisibilityRule]:
    return list(
        session.scalars(
            select(ClientPresentationVisibilityRule).order_by(
                ClientPresentationVisibilityRule.target_type,
                ClientPresentationVisibilityRule.target_code,
                ClientPresentationVisibilityRule.priority,
                ClientPresentationVisibilityRule.rule_code,
            )
        ).all()
    )


def list_owner_client_action_policies(
    session: Session,
) -> list[ClientPresentationActionPolicy]:
    return list(
        session.scalars(
            select(ClientPresentationActionPolicy).order_by(
                ClientPresentationActionPolicy.target_type,
                ClientPresentationActionPolicy.target_code,
                ClientPresentationActionPolicy.action_type,
                ClientPresentationActionPolicy.policy_code,
            )
        ).all()
    )


def list_owner_client_tracking_policies(
    session: Session,
) -> list[ClientPresentationTrackingPolicy]:
    return list(
        session.scalars(
            select(ClientPresentationTrackingPolicy).order_by(
                ClientPresentationTrackingPolicy.target_type,
                ClientPresentationTrackingPolicy.target_code,
                ClientPresentationTrackingPolicy.event_name,
                ClientPresentationTrackingPolicy.policy_code,
            )
        ).all()
    )


def list_owner_groups(session: Session) -> list[Group]:
    return list(session.scalars(select(Group).order_by(Group.sort_order, Group.id)).all())


def list_owner_offers(session: Session) -> list[Offer]:
    return list(session.scalars(select(Offer).order_by(Offer.sort_order, Offer.id)).all())


def list_owner_components(session: Session) -> list[tuple[OfferComponent, Offer]]:
    statement = (
        select(OfferComponent, Offer)
        .join(Offer, Offer.id == OfferComponent.offer_id)
        .order_by(Offer.offer_code, OfferComponent.sort_order, OfferComponent.id)
    )
    return list(session.execute(statement).all())


def list_owner_prices(session: Session) -> list[tuple[OfferPrice, Offer]]:
    statement = (
        select(OfferPrice, Offer)
        .join(Offer, Offer.id == OfferPrice.offer_id)
        .order_by(Offer.offer_code, OfferPrice.priority, OfferPrice.id)
    )
    return list(session.execute(statement).all())


def list_owner_positions(session: Session) -> list[tuple[OfferPosition, Group, Offer]]:
    statement = (
        select(OfferPosition, Group, Offer)
        .join(Group, Group.id == OfferPosition.group_id)
        .join(Offer, Offer.id == OfferPosition.offer_id)
        .order_by(Group.sort_order, OfferPosition.sort_order, OfferPosition.id)
    )
    return list(session.execute(statement).all())


def list_owner_promotion_rules(session: Session) -> list[PromotionRule]:
    return list(
        session.scalars(
            select(PromotionRule).order_by(PromotionRule.priority, PromotionRule.id)
        ).all()
    )


def list_owner_promotion_targets(session: Session) -> list[tuple[PromotionTarget, PromotionRule]]:
    statement = (
        select(PromotionTarget, PromotionRule)
        .join(PromotionRule, PromotionRule.id == PromotionTarget.promotion_rule_id)
        .order_by(PromotionRule.priority, PromotionTarget.id)
    )
    return list(session.execute(statement).all())


def list_owner_coupons(session: Session) -> list[tuple[Coupon, PromotionRule]]:
    statement = (
        select(Coupon, PromotionRule)
        .join(PromotionRule, PromotionRule.id == Coupon.promotion_rule_id)
        .order_by(Coupon.id)
    )
    return list(session.execute(statement).all())


def add_published_rows(session: Session, rows: list[object]) -> None:
    session.add_all(rows)
    session.flush()


def latest_publish_version(session: Session, publish_version: str | None) -> PublishVersion | None:
    if publish_version is not None:
        return session.scalar(
            select(PublishVersion).where(PublishVersion.publish_version == publish_version)
        )

    statement = (
        select(PublishVersion)
        .where(PublishVersion.status == "published")
        .where(PublishVersion.publish_scope.in_(("storefront", "all")))
        .order_by(PublishVersion.published_at.desc().nullslast(), PublishVersion.id.desc())
        .limit(1)
    )
    return session.scalar(statement)


def list_published_client_pages(
    session: Session, publish_version: str
) -> list[PublishedClientPage]:
    return list(
        session.scalars(
            select(PublishedClientPage)
            .where(PublishedClientPage.publish_version == publish_version)
            .order_by(PublishedClientPage.sort_order, PublishedClientPage.id)
        ).all()
    )


def list_published_client_regions(
    session: Session, publish_version: str
) -> list[PublishedClientRegion]:
    return list(
        session.scalars(
            select(PublishedClientRegion)
            .where(PublishedClientRegion.publish_version == publish_version)
            .order_by(PublishedClientRegion.page_code, PublishedClientRegion.sort_order)
        ).all()
    )


def list_published_client_region_blocks(
    session: Session, publish_version: str
) -> list[PublishedClientRegionBlock]:
    return list(
        session.scalars(
            select(PublishedClientRegionBlock)
            .where(PublishedClientRegionBlock.publish_version == publish_version)
            .order_by(
                PublishedClientRegionBlock.page_code,
                PublishedClientRegionBlock.region_code,
                PublishedClientRegionBlock.sort_order,
                PublishedClientRegionBlock.id,
            )
        ).all()
    )


def list_published_client_block_types(
    session: Session, publish_version: str
) -> list[PublishedClientBlockType]:
    return list(
        session.scalars(
            select(PublishedClientBlockType)
            .where(PublishedClientBlockType.publish_version == publish_version)
            .order_by(PublishedClientBlockType.block_type, PublishedClientBlockType.id)
        ).all()
    )


def list_published_client_surfaces(
    session: Session, publish_version: str
) -> list[PublishedClientSurface]:
    return list(
        session.scalars(
            select(PublishedClientSurface)
            .where(PublishedClientSurface.publish_version == publish_version)
            .order_by(PublishedClientSurface.surface_code, PublishedClientSurface.id)
        ).all()
    )


def list_published_client_data_bindings(
    session: Session, publish_version: str
) -> list[PublishedClientDataBinding]:
    return list(
        session.scalars(
            select(PublishedClientDataBinding)
            .where(PublishedClientDataBinding.publish_version == publish_version)
            .order_by(
                PublishedClientDataBinding.target_type,
                PublishedClientDataBinding.target_code,
                PublishedClientDataBinding.binding_code,
            )
        ).all()
    )


def list_published_client_visibility_rules(
    session: Session, publish_version: str
) -> list[PublishedClientVisibilityRule]:
    return list(
        session.scalars(
            select(PublishedClientVisibilityRule)
            .where(PublishedClientVisibilityRule.publish_version == publish_version)
            .order_by(
                PublishedClientVisibilityRule.target_type,
                PublishedClientVisibilityRule.target_code,
                PublishedClientVisibilityRule.priority,
            )
        ).all()
    )


def list_published_client_action_policies(
    session: Session, publish_version: str
) -> list[PublishedClientActionPolicy]:
    return list(
        session.scalars(
            select(PublishedClientActionPolicy)
            .where(PublishedClientActionPolicy.publish_version == publish_version)
            .order_by(
                PublishedClientActionPolicy.target_type,
                PublishedClientActionPolicy.target_code,
                PublishedClientActionPolicy.action_type,
            )
        ).all()
    )


def list_published_client_tracking_policies(
    session: Session, publish_version: str
) -> list[PublishedClientTrackingPolicy]:
    return list(
        session.scalars(
            select(PublishedClientTrackingPolicy)
            .where(PublishedClientTrackingPolicy.publish_version == publish_version)
            .order_by(
                PublishedClientTrackingPolicy.target_type,
                PublishedClientTrackingPolicy.target_code,
                PublishedClientTrackingPolicy.event_name,
            )
        ).all()
    )


def list_published_groups(session: Session, publish_version: str) -> list[PublishedGroup]:
    return list(
        session.scalars(
            select(PublishedGroup)
            .where(PublishedGroup.publish_version == publish_version)
            .order_by(PublishedGroup.sort_order, PublishedGroup.id)
        ).all()
    )


def list_published_offers(session: Session, publish_version: str) -> list[PublishedOffer]:
    return list(
        session.scalars(
            select(PublishedOffer)
            .where(PublishedOffer.publish_version == publish_version)
            .order_by(PublishedOffer.id)
        ).all()
    )


def list_published_components(
    session: Session, publish_version: str
) -> list[PublishedOfferComponent]:
    return list(
        session.scalars(
            select(PublishedOfferComponent)
            .where(PublishedOfferComponent.publish_version == publish_version)
            .order_by(PublishedOfferComponent.offer_code, PublishedOfferComponent.component_no)
        ).all()
    )


def list_published_prices(session: Session, publish_version: str) -> list[PublishedOfferPrice]:
    return list(
        session.scalars(
            select(PublishedOfferPrice)
            .where(PublishedOfferPrice.publish_version == publish_version)
            .order_by(
                PublishedOfferPrice.offer_code, PublishedOfferPrice.priority, PublishedOfferPrice.id
            )
        ).all()
    )


def list_published_positions(
    session: Session, publish_version: str
) -> list[PublishedOfferPosition]:
    return list(
        session.scalars(
            select(PublishedOfferPosition)
            .where(PublishedOfferPosition.publish_version == publish_version)
            .order_by(PublishedOfferPosition.group_code, PublishedOfferPosition.sort_order)
        ).all()
    )


def list_published_rules(session: Session, publish_version: str) -> list[PublishedPromotionRule]:
    return list(
        session.scalars(
            select(PublishedPromotionRule)
            .where(PublishedPromotionRule.publish_version == publish_version)
            .order_by(PublishedPromotionRule.priority, PublishedPromotionRule.id)
        ).all()
    )


def list_published_targets(
    session: Session, publish_version: str
) -> list[PublishedPromotionTarget]:
    return list(
        session.scalars(
            select(PublishedPromotionTarget)
            .where(PublishedPromotionTarget.publish_version == publish_version)
            .order_by(PublishedPromotionTarget.promotion_code, PublishedPromotionTarget.id)
        ).all()
    )


def list_published_coupons(session: Session, publish_version: str) -> list[PublishedCoupon]:
    return list(
        session.scalars(
            select(PublishedCoupon)
            .where(PublishedCoupon.publish_version == publish_version)
            .order_by(PublishedCoupon.id)
        ).all()
    )


def list_owner_storefront_section_rows(
    session: Session,
) -> list[tuple[StorefrontSection, Group | None]]:
    statement = (
        select(StorefrontSection, Group)
        .outerjoin(Group, Group.id == StorefrontSection.group_id)
        .order_by(StorefrontSection.sort_order, StorefrontSection.id)
    )
    return list(session.execute(statement).all())


def list_owner_storefront_section_layout_rows(
    session: Session,
) -> list[tuple[StorefrontSectionLayout, StorefrontSection]]:
    statement = (
        select(StorefrontSectionLayout, StorefrontSection)
        .join(StorefrontSection, StorefrontSection.id == StorefrontSectionLayout.section_id)
        .order_by(StorefrontSection.sort_order, StorefrontSection.id)
    )
    return list(session.execute(statement).all())


def list_owner_storefront_section_position_rows(
    session: Session,
) -> list[tuple[StorefrontSectionPosition, StorefrontSection, Offer]]:
    statement = (
        select(StorefrontSectionPosition, StorefrontSection, Offer)
        .join(StorefrontSection, StorefrontSection.id == StorefrontSectionPosition.section_id)
        .join(Offer, Offer.id == StorefrontSectionPosition.offer_id)
        .order_by(
            StorefrontSection.sort_order,
            StorefrontSectionPosition.sort_order,
            StorefrontSectionPosition.id,
        )
    )
    return list(session.execute(statement).all())


def list_published_storefront_sections(
    session: Session,
    publish_version: str,
) -> list[PublishedStorefrontSection]:
    statement = (
        select(PublishedStorefrontSection)
        .where(PublishedStorefrontSection.publish_version == publish_version)
        .order_by(PublishedStorefrontSection.sort_order, PublishedStorefrontSection.id)
    )
    return list(session.scalars(statement).all())


def list_published_storefront_section_layouts(
    session: Session,
    publish_version: str,
) -> list[PublishedStorefrontSectionLayout]:
    statement = (
        select(PublishedStorefrontSectionLayout)
        .where(PublishedStorefrontSectionLayout.publish_version == publish_version)
        .order_by(
            PublishedStorefrontSectionLayout.section_code, PublishedStorefrontSectionLayout.id
        )
    )
    return list(session.scalars(statement).all())


def list_published_storefront_section_positions(
    session: Session,
    publish_version: str,
) -> list[PublishedStorefrontSectionPosition]:
    statement = (
        select(PublishedStorefrontSectionPosition)
        .where(PublishedStorefrontSectionPosition.publish_version == publish_version)
        .order_by(
            PublishedStorefrontSectionPosition.section_code,
            PublishedStorefrontSectionPosition.sort_order,
            PublishedStorefrontSectionPosition.id,
        )
    )
    return list(session.scalars(statement).all())
