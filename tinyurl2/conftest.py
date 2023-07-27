import os

import alembic.config
import pytest
from starlette.testclient import TestClient

from tinyurl2.app import app
from tinyurl2.database.base import BaseModel, db_engine
from tinyurl2.database.session import Session


@pytest.fixture(scope="session", autouse=True)
def init_db():
    alembic.config.main(argv=["upgrade", "head"])
    try:
        yield
    finally:
        alembic.config.main(argv=["downgrade", "base"])

        # if test DB is file-based SQLite, also remove the file for complete cleanup
        if (
            str(db_engine.engine.url).startswith("sqlite")
            and db_engine.engine.url.database != ":memory:"
        ):
            os.remove(db_engine.engine.url.database)


@pytest.fixture()
def db_session(request):
    session = Session()
    try:
        if getattr(request, "cls", None):
            request.cls.db_session = session

        yield session
    finally:
        # commit the transaction in case test function didn't do it to
        # do the cleanup below in a separate transaction
        session.commit()

        # truncate all tables to cleanup any data created by test
        # and prevent it affecting other tests
        with session.begin():
            for table in BaseModel.metadata.sorted_tables:
                session.execute(table.delete())

        session.close()


@pytest.fixture()
def app_client(request):
    client = TestClient(app)
    if getattr(request, "cls", None):
        request.cls.app_client = client

    return client
