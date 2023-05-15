from datetime import date

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import clear_mappers, sessionmaker

import config
from adapters.orm import mapper_registry, start_mappers
from adapters.repository import SqlAlchemyRepository
from domain.model import Batch


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture
def sqlite_db():
    engine = create_engine(config.get_sqlite_uri())
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session(sqlite_db):
    start_mappers()
    yield sessionmaker(bind=sqlite_db)()
    clear_mappers()


@pytest.fixture
def add_stock(sqlite_session):
    repo = SqlAlchemyRepository(sqlite_session)

    def _add_stock(batches):
        for batch in batches:
            if len(batch) == 4:
                repo.add(
                    Batch(batch[0], batch[1], batch[2], date.fromisoformat(batch[3]))
                )
            else:
                repo.add(Batch(batch[0], batch[1], batch[2]))
        sqlite_session.commit()

    yield _add_stock

    sqlite_session.execute(text("DELETE From allocations;"))
    sqlite_session.execute(text("DELETE From batches;"))
    sqlite_session.execute(text("DELETE From order_lines;"))
    sqlite_session.commit()
