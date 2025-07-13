from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import delete, text

from src.main import app
from src.db.session import get_session, AsyncSessionLocal
from src.models.user import User


@pytest_asyncio.fixture(scope="function")
async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:  # type: ignore
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest_asyncio.fixture(autouse=True)
async def clean_db(override_get_session: AsyncSession):
    async with override_get_session.begin():
        await override_get_session.execute(
            text("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
        )
        await override_get_session.commit()


@pytest_asyncio.fixture(scope="function")
async def client(override_get_session) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_session] = lambda: override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        try:
            yield client
        finally:
            app.dependency_overrides.clear()
