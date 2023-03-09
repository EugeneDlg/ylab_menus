import asyncio
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db import TABLES, get_db_session
from app.db_models import Base
from app.envconfig import TEST_DB_CONN_STRING
from app.main import app

engine = create_async_engine(TEST_DB_CONN_STRING, echo=True)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def get_session_():
    try:
        Session = sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        yield Session
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, Any]:
    app.dependency_overrides[get_db_session] = get_session_
    async with AsyncClient(app=app, base_url="http://test") as client_:
        yield client_


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# TABLES = ["menu", "submenu", "dish"]


async def clean_tables():
    async with engine.connect() as conn:
        await conn.execute(text("TRUNCATE TABLE menu CASCADE;"))
        for table in TABLES:
            await conn.execute(text(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1"))
        await conn.commit()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def create_and_drop_tables():
    await clean_tables()
    # await create_tables()
    yield
    await drop_tables()
