from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status


from src.db.session import get_session
from src.dependencies.auth import get_current_user
from src.schemas.task import DeadlineShiftRequest, TaskCreate, TaskResponse, TaskUpdate
from src.schemas.tag import TagResponse
from src.crud.task import *

router = APIRouter()


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать задачу",
)
async def create_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    task = await create_task_db(session, task_data, current_user["id"])
    return task


@router.get(
    "/",
    response_model=Sequence[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить все задачи текущего пользователя с сортировкой",
)
async def get_all_tasks(
    skip: int = 0,
    limit: int = 100,
    is_completed: Optional[bool] = Query(
        None, description="Фильтр по статусу выполнения"
    ),
    sort_by: str = Query(
        "created_at",
        description="Поле для сортировки (title, priority, deadline, created_at)",
        regex="^(title|priority|deadline|created_at)$",
    ),
    order: str = Query(
        "desc", description="Порядок сортировки (asc или desc)", regex="^(asc|desc)$"
    ),
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tasks = await get_all_tasks_by_author_id(
        session, current_user["id"], skip, limit, is_completed, sort_by, order
    )
    return tasks


@router.get(
    "/{task_id:int}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить задачу по ID",
)
async def get_tag(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tag = await get_task_by_id(session, task_id, current_user["id"])
    if not tag:
        raise HTTPException(status_code=404, detail="Task not found")
    return tag


@router.patch(
    "/{task_id:int}",
    response_model=TaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Обновить задачу",
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    task = await update_task_by_id(session, task_id, current_user["id"], task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete(
    "/{task_id:int}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить задачу"
)
async def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    success = await delete_task_by_id(session, task_id, current_user["id"])
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")


@router.patch(
    "/{task_id:int}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Пометить задачу выполенной",
)
async def mark_task_complete(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    task = await mark_task_complete_by_id(session, task_id, current_user["id"])
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get(
    "/{task_id:int}/tags",
    response_model=Sequence[TagResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить теги задачи",
)
async def get_task_tags(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tags = await get_task_tags_by_id(session, task_id, current_user["id"])
    return tags


@router.get(
    "/search/", response_model=Sequence[TaskResponse], summary="Поиск задач по названию"
)
async def search_tasks(
    title: str,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tasks = await search_tasks_by_title(session, title, current_user["id"])
    return tasks


@router.patch(
    "/{task_id:int}/add_tags",
    response_model=TaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Добавить тэги к задаче",
)
async def update_tags_task(
    task_id: int,
    tags_ids: List[int],
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    task = await update_tags_task_by_id(session, task_id, current_user["id"], tags_ids)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get(
    "/by-deadline",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить задачи с дедлайном в указанный промежуток",
)
async def get_tasks_by_deadline_interval(
    day_start: date,
    day_end: date,
    is_completed: Optional[bool] = Query(
        None, description="Фильтр по статусу выполнения"
    ),
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tasks = await get_tasks_by_deadline_period(
        session, current_user["id"], day_start, day_end, is_completed
    )
    return tasks


@router.get(
    "/by-deadline/{day}",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить задачи с дедлайном в указанный день",
)
async def get_tasks_by_deadline(
    day: date,
    is_completed: Optional[bool] = Query(
        None, description="Фильтр по статусу выполнения"
    ),
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tasks = await get_tasks_by_deadline_period(
        session, current_user["id"], day, day, is_completed
    )
    return tasks


@router.patch(
    "/{task_id}/shift_deadline",
    response_model=TaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Перенести дедлайн задачи",
)
async def shift_task_deadline(
    task_id: int,
    shift_data: DeadlineShiftRequest,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    shift = timedelta(
        days=shift_data.days, hours=shift_data.hours, minutes=shift_data.minutes
    )

    task = await shift_task_deadline_by_id(session, task_id, current_user["id"], shift)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get(
    "/overdue",
    response_model=Sequence[TaskResponse],
    summary="Получить просроченные задачи",
)
async def get_overdue_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tasks = await get_overdue_tasks_db(session, current_user["id"], skip, limit)
    return tasks
