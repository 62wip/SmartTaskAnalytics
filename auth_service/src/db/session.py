from typing import AsyncGenerator, cast

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends

from src.core.config import DATABASE_URL

assert DATABASE_URL is not None, "DATABASE_URL is not set"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
)
AsyncSessionLocal.configure(bind=engine)

Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with cast(AsyncSession, AsyncSessionLocal()) as session:
        yield session
