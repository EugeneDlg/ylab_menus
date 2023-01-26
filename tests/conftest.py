import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import get_session, app
from app.db_utils import TEST_DB_CONN_STRING
from app.db_models import Base
engine = create_engine(TEST_DB_CONN_STRING, echo=True)
Sessions = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session_():
    try:
        session = Sessions()
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    print("test_db_create")
    yield
    Base.metadata.drop_all(bind=engine)
    print("test_db_delete")


@pytest.fixture(scope='module')
def client():
    print("client")
    app.dependency_overrides[get_session] = get_session_
    client = TestClient(app=app)
    yield client
