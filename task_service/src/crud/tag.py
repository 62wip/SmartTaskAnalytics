from typing import Optional, Sequence
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.task import Task
from src.models.tag import Tag
from src.models.task_tag import task_tag_table


async def create_tag_db(session: AsyncSession, name: str, author_id: int) -> Tag:
    tag = Tag(name=name, author_id=author_id)
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag


async def get_all_tags_by_author_id(
    session: AsyncSession,
    author_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Tag]:
    result = await session.execute(
        select(Tag).filter(Tag.author_id == author_id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_tag_by_id(
    session: AsyncSession, tag_id: int, author_id: int
) -> Optional[Tag]:
    result = await session.execute(
        select(Tag).filter(Tag.id == tag_id, Tag.author_id == author_id)
    )
    return result.scalars().first()


async def update_tag_by_id(
    session: AsyncSession, tag_id: int, author_id: int, new_name: str
) -> Optional[Tag]:
    tag = await get_tag_by_id(session, tag_id, author_id)
    if tag:
        tag.name = new_name  # type: ignore
        await session.commit()
        await session.refresh(tag)
    return tag


async def delete_tag_by_id(session: AsyncSession, tag_id: int, author_id: int) -> bool:
    tag = await get_tag_by_id(session, tag_id, author_id)
    if tag:
        await session.delete(tag)
        await session.commit()
        return True
    return False


async def search_tags_by_name(
    session: AsyncSession, name: str, author_id: int
) -> Sequence[Tag]:
    result = await session.execute(
        select(Tag)
        .where(and_(Tag.author_id == author_id, Tag.name.ilike(f"%{name}%")))
        .limit(10)
    )
    return result.scalars().all()


async def get_tasks_for_tag(
    session: AsyncSession,
    tag_id: int,
    author_id: int,
    is_completed: bool | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Task]:
    tag = await get_tag_by_id(session, tag_id, author_id)
    if not tag:
        return []
    query = (
        select(Task)
        .join(task_tag_table, Task.id == task_tag_table.c.task_id)
        .where(task_tag_table.c.tag_id == tag_id)
    )
    if is_completed is not None:
        query = query.where(Task.is_completed == is_completed)

    tasks = await session.execute(query.offset(skip).limit(limit))
    return tasks.scalars().all()
