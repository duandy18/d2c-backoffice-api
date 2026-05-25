"""Backoffice group services."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domains.groups.contracts.group_contract import (
    BackofficeGroupContract,
    BackofficeGroupCreateRequest,
    BackofficeGroupsResponse,
)
from app.domains.groups.models.group import Group
from app.domains.groups.repos.group_repo import create_group, get_group_by_code, list_groups


class BackofficeGroupDuplicateCodeError(Exception):
    pass


def build_group_contract(group: Group) -> BackofficeGroupContract:
    return BackofficeGroupContract(
        id=group.id,
        group_code=group.group_code,
        group_name=group.group_name,
        group_kind=group.group_kind,
        description=group.description,
        image_url=group.image_url,
        sort_order=int(group.sort_order),
        display_status=group.display_status,
        is_active=group.is_active,
        source_type=group.source_type,
        source_ref=group.source_ref,
        created_at=group.created_at,
        updated_at=group.updated_at,
    )


def get_backoffice_groups(session: Session) -> BackofficeGroupsResponse:
    groups = [build_group_contract(group) for group in list_groups(session)]
    return BackofficeGroupsResponse(count=len(groups), groups=groups)


def create_backoffice_group(
    session: Session,
    payload: BackofficeGroupCreateRequest,
) -> BackofficeGroupContract:
    if get_group_by_code(session, payload.group_code) is not None:
        raise BackofficeGroupDuplicateCodeError("group_code_already_exists")

    group = Group(
        group_code=payload.group_code,
        group_name=payload.group_name,
        group_kind=payload.group_kind,
        description=payload.description,
        image_url=payload.image_url,
        sort_order=payload.sort_order,
        display_status=payload.display_status,
        is_active=payload.is_active,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )

    try:
        create_group(session, group)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise BackofficeGroupDuplicateCodeError("group_code_already_exists") from exc

    return build_group_contract(group)
