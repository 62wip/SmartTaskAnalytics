from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.tag import Tag

async def create_tag(session: AsyncSession, name: str, author_id: int) -> Tag:
    tag = Tag(name=name, author_id=author_id)
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag

async def get_all_tags_by_author_id(session: AsyncSession, author_id: int) -> Sequence[Tag]:
    result = await session.execute(select(Tag).filter(Tag.author_id == author_id))
    return result.scalars().all()