import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import TEST_DB_CONN_STRING
from app.db import get_session
from app.db_models import Base
from app.main import app

engine = create_engine(TEST_DB_CONN_STRING, echo=True)
Sessions = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session_():
    try:
        session = Sessions()
        yield session
    finally:
        session.close()


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='module')
def client():
    app.dependency_overrides[get_session] = get_session_
    client = TestClient(app=app)
    yield client
