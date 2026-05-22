from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import D2CBackofficeSettings, load_settings


class Base(DeclarativeBase):
    pass


def create_db_engine(settings: D2CBackofficeSettings | None = None) -> Engine:
    resolved_settings = settings or load_settings()
    return create_engine(resolved_settings.database_url, pool_pre_ping=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_engine(database_url: str) -> Engine:
    return create_engine(database_url, pool_pre_ping=True)


def get_session_factory(database_url: str) -> sessionmaker[Session]:
    return create_session_factory(get_engine(database_url))


def get_session() -> Generator[Session, None, None]:
    settings = load_settings()
    session_factory = get_session_factory(settings.database_url)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
