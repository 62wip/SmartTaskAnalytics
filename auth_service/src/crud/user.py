from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.user import User
from src.core.security import hash_password


async def create_user(
    session: AsyncSession, username: str, email: str, password: str
) -> User:
    hashed_pw = hash_password(password)
    user = User(username=username, email=email, hashed_password=hashed_pw)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    result = await session.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    result = await session.execute(select(User).filter(User.username == username))
    return result.scalars().first()
