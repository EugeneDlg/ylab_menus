import asyncio
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db import get_session
from app.envconfig import TEST_DB_CONN_STRING
from app.main import app

engine = create_async_engine(TEST_DB_CONN_STRING, echo=True)
Sessions = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def get_session_():
    try:
        session = Sessions()
        yield session
    finally:
        await session.close()


# @pytest.fixture(scope='module')
# def client():
#     app.dependency_overrides[get_session] = get_session_
#     client = TestClient(app=app)
#     yield client


# @pytest.fixture
# async def create_menu_in_database(asyncpg_pool):
#     async def create_menu_in_database(id_: str, title: str, description: str):
#         async with asyncpg_pool.acquire() as connection:
#             return await connection.execute(
#                 """INSERT INTO menu VALUES ($1, $2, $3)""",
#                 id_,
#                 title,
#                 description,
#             )
#
#     return create_menu_in_database


# @pytest_asyncio.fixture(scope="function", autouse=True)
# async def clean_tables():
#     async with engine.connect() as conn:
#         await conn.execute(text("TRUNCATE TABLE menu CASCADE;"))
#         await conn.commit()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, Any]:
    app.dependency_overrides[get_session] = get_session_
    async with AsyncClient(app=app, base_url="http://test") as client_:
        yield client_
