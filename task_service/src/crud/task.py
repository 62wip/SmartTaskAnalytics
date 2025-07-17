from datetime import UTC, date, datetime, timedelta
from typing import List, Optional, Sequence
from fastapi import HTTPException
from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.tag import Tag
from src.schemas.task import TaskCreate, TaskUpdate
from src.models.task import Task
from src.models.task_tag import task_tag_table


async def create_task_db(
    session: AsyncSession, task_data: TaskCreate, author_id: int
) -> Task:
    task_dict = task_data.model_dump()

    if task_dict.get("deadline"):
        deadline = task_dict["deadline"]
        if deadline.tzinfo is not None:
            task_dict["deadline"] = deadline.astimezone(UTC)
        else:
            task_dict["deadline"] = deadline.replace(tzinfo=UTC)

    task = Task(**task_data.model_dump(), author_id=author_id)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_all_tasks_by_author_id(
    session: AsyncSession,
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    is_completed: bool | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
) -> Sequence[Task]:
    sort_column = {
        "title": Task.title,
        "priority": Task.priority,
        "deadline": Task.deadline,
        "created_at": Task.created_at,
    }.get(sort_by, Task.created_at)
    sort_order = desc if order == "desc" else asc

    query = select(Task).where(Task.author_id == author_id)
    if is_completed is not None:
        query = query.where(Task.is_completed == is_completed)
    query = query.order_by(sort_order(sort_column)).offset(skip).limit(limit)

    result = await session.execute(query)
    return result.scalars().all()


async def get_task_by_id(
    session: AsyncSession, task_id: int, author_id: int
) -> Optional[Task]:
    result = await session.execute(
        select(Task).filter(Task.id == task_id, Task.author_id == author_id)
    )
    return result.scalars().first()


async def update_task_by_id(
    session: AsyncSession, task_id: int, author_id: int, task_data: TaskUpdate
) -> Optional[Task]:
    task = await get_task_by_id(session, task_id, author_id)
    if task:
        if task_data.title is not None:
            task.title = task_data.title  # type: ignore
        if task_data.description is not None:
            task.description = task_data.description  # type: ignore
        if task_data.priority is not None:
            task.priority = task_data.priority  # type: ignore
        if task_data.is_completed is not None:
            task.is_completed = task_data.is_completed  # type: ignore
        if task_data.deadline is not None:
            deadline = task_data.deadline
            if deadline.tzinfo is not None:
                task.deadline = deadline.astimezone(UTC)  # type: ignore
            else:
                task.deadline = deadline.replace(tzinfo=UTC)  # type: ignore
        if task_data.tag_ids is not None:
            result = await session.execute(
                select(Tag).where(
                    and_(Tag.id.in_(task_data.tag_ids), Tag.author_id == author_id)
                )
            )
            valid_tags = result.scalars().all()
            task.tags.clear()
            task.tags.extend(valid_tags)

    await session.commit()
    await session.refresh(task)
    return task


async def delete_task_by_id(
    session: AsyncSession, task_id: int, author_id: int
) -> bool:
    task = await get_task_by_id(session, task_id, author_id)
    if task:
        await session.delete(task)
        await session.commit()
        return True
    return False


async def mark_task_complete_by_id(
    session: AsyncSession, task_id: int, author_id: int
) -> Optional[Task]:
    task = await get_task_by_id(session, task_id, author_id)
    if task:
        task.is_completed = True  # type: ignore
        await session.commit()
        await session.refresh(task)
    return task


async def get_task_tags_by_id(
    session: AsyncSession, task_id: int, author_id: int
) -> Sequence[Tag]:
    task = await get_task_by_id(session, task_id, author_id)
    if not task:
        return []
    return task.tags


async def search_tasks_by_title(
    session: AsyncSession, title: str, author_id: int
) -> Sequence[Task]:
    result = await session.execute(
        select(Task)
        .where(and_(Task.author_id == author_id), Task.title.ilike(f"%{title}%"))
        .limit(10)
    )
    return result.scalars().all()


async def update_tags_task_by_id(
    session: AsyncSession, task_id: int, author_id: int, tag_ids: List[int]
) -> Optional[Task]:
    task = await get_task_by_id(session, task_id, author_id)
    if task:
        result = await session.execute(
            select(Tag).where(and_(Tag.id.in_(tag_ids), Tag.author_id == author_id))
        )

        new_valid_tags = result.scalars().all()
        current_tag_ids = {tag.id for tag in task.tags}
        valid_tags = []
        for tag in new_valid_tags:
            if tag.id not in current_tag_ids:
                valid_tags.append(tag)
        task.tags.clear()
        task.tags.extend(valid_tags)

        await session.commit()
        await session.refresh(task)
    return task


async def get_tasks_by_deadline_period(
    session: AsyncSession,
    author_id: int,
    day_start: date,
    day_end: date,
    is_completed: bool | None = None,
) -> Sequence[Task]:
    start_datetime = datetime.combine(day_start, datetime.min.time()).replace(
        tzinfo=UTC
    )
    end_datetime = datetime.combine(day_end, datetime.max.time()).replace(tzinfo=UTC)
    query = select(Task).where(
        and_(
            Task.author_id == author_id,
            Task.deadline.between(start_datetime, end_datetime),
        )
    )

    if is_completed is not None:
        query = query.where(Task.is_completed == is_completed)

    result = await session.execute(query)
    return result.scalars().all()


async def shift_task_deadline_by_id(
    session: AsyncSession, task_id: int, author_id: int, shift: timedelta
) -> Optional[Task]:
    task = await get_task_by_id(session, task_id, author_id)
    if task and task.deadline:  # type: ignore
        task.deadline += shift  # type: ignore
        await session.commit()
        await session.refresh(task)
    return task


async def get_overdue_tasks_db(
    session: AsyncSession, author_id: int, skip: int = 0, limit: int = 100
) -> Sequence[Task]:
    now = datetime.now(UTC)

    query = (
        select(Task)
        .where(
            and_(
                Task.author_id == author_id,
                Task.deadline < now,
                Task.is_completed == False,
            )
        )
        .order_by(Task.deadline.asc())
        .offset(skip)
        .limit(limit)
    )

    result = await session.execute(query)
    return result.scalars().all()
