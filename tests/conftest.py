import os
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from main import app
from db import get_session, engine  # Import your existing engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
# Use the same database URL or a test-specific async database URL
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite+aiosqlite:///./test.db")
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)


@pytest_asyncio.fixture(scope="function")
async def async_session():
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create session
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    session = async_session()
    try:
        yield session
    finally:
        await session.close()
        # Drop tables after test
        async with test_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_client(async_session):
    # Override the get_session dependency for testing
    app.dependency_overrides[get_session] = lambda: async_session

    async_client = AsyncClient(app=app, base_url="http://test")
    yield async_client

    # Clear overrides
    app.dependency_overrides.clear()


