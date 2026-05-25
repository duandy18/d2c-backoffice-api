"""Client presentation repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

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



def get_surface_by_code(session: Session, surface_code: str) -> ClientPresentationSurface | None:
    return session.scalar(
        select(ClientPresentationSurface).where(
            ClientPresentationSurface.surface_code == surface_code
        )
    )


def list_surfaces(session: Session) -> list[ClientPresentationSurface]:
    return list(
        session.scalars(
            select(ClientPresentationSurface).order_by(
                ClientPresentationSurface.surface_code,
                ClientPresentationSurface.id,
            )
        ).all()
    )


def create_surface(
    session: Session,
    surface: ClientPresentationSurface,
) -> ClientPresentationSurface:
    session.add(surface)
    session.flush()
    return surface


def get_data_binding_by_code(
    session: Session, binding_code: str
) -> ClientPresentationDataBinding | None:
    return session.scalar(
        select(ClientPresentationDataBinding).where(
            ClientPresentationDataBinding.binding_code == binding_code
        )
    )


def list_data_bindings(session: Session) -> list[ClientPresentationDataBinding]:
    return list(
        session.scalars(
            select(ClientPresentationDataBinding).order_by(
                ClientPresentationDataBinding.target_type,
                ClientPresentationDataBinding.target_code,
                ClientPresentationDataBinding.binding_code,
            )
        ).all()
    )


def create_data_binding(
    session: Session,
    binding: ClientPresentationDataBinding,
) -> ClientPresentationDataBinding:
    session.add(binding)
    session.flush()
    return binding


def get_visibility_rule_by_code(
    session: Session, rule_code: str
) -> ClientPresentationVisibilityRule | None:
    return session.scalar(
        select(ClientPresentationVisibilityRule).where(
            ClientPresentationVisibilityRule.rule_code == rule_code
        )
    )


def list_visibility_rules(session: Session) -> list[ClientPresentationVisibilityRule]:
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


def create_visibility_rule(
    session: Session,
    rule: ClientPresentationVisibilityRule,
) -> ClientPresentationVisibilityRule:
    session.add(rule)
    session.flush()
    return rule


def get_action_policy_by_code(
    session: Session, policy_code: str
) -> ClientPresentationActionPolicy | None:
    return session.scalar(
        select(ClientPresentationActionPolicy).where(
            ClientPresentationActionPolicy.policy_code == policy_code
        )
    )


def list_action_policies(session: Session) -> list[ClientPresentationActionPolicy]:
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


def create_action_policy(
    session: Session,
    policy: ClientPresentationActionPolicy,
) -> ClientPresentationActionPolicy:
    session.add(policy)
    session.flush()
    return policy


def get_tracking_policy_by_code(
    session: Session, policy_code: str
) -> ClientPresentationTrackingPolicy | None:
    return session.scalar(
        select(ClientPresentationTrackingPolicy).where(
            ClientPresentationTrackingPolicy.policy_code == policy_code
        )
    )


def list_tracking_policies(session: Session) -> list[ClientPresentationTrackingPolicy]:
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


def create_tracking_policy(
    session: Session,
    policy: ClientPresentationTrackingPolicy,
) -> ClientPresentationTrackingPolicy:
    session.add(policy)
    session.flush()
    return policy
