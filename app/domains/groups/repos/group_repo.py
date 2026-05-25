"""Backoffice group repositories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.groups.models.group import Group


def get_group_by_code(session: Session, group_code: str) -> Group | None:
    return session.scalar(select(Group).where(Group.group_code == group_code))


def list_groups(session: Session) -> list[Group]:
    statement = select(Group).order_by(Group.sort_order, Group.id)
    return list(session.scalars(statement).all())


def create_group(session: Session, group: Group) -> Group:
    session.add(group)
    session.flush()
    return group
