from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.task import TaskResponse
from src.dependencies.auth import get_current_user
from src.db.session import get_session
from src.schemas.tag import TagCreate, TagResponse, TagUpdate
from src.crud.tag import *

router = APIRouter()


@router.post(
    "/",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать тэг",
)
async def create_task(
    task_data: TagCreate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tag = await create_tag(session, task_data.name, current_user["id"])
    return tag


@router.get(
    "/",
    response_model=Sequence[TagResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Получить все теги текущего пользователя",
)
async def get_all_tasks(
    skip: int = 0,
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tags = await get_all_tags_by_author_id(session, current_user["id"], skip, limit)
    return tags


@router.get("/{tag_id}", response_model=TagResponse, summary="Получить тег по ID")
async def get_tag(
    tag_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tag = await get_tag_by_id(session, tag_id, current_user["id"])
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.patch("/{tag_id}", response_model=TagResponse, summary="Обновить тег")
async def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if tag_data.name is None:
        raise HTTPException(status_code=400, detail="Name is required")
    tag = await update_tag_by_id(session, tag_id, current_user["id"], tag_data.name)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.delete(
    "/{tag_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить тег"
)
async def delete_tag(
    tag_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    success = await delete_tag_by_id(session, tag_id, current_user["id"])
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")


@router.get(
    "/search", response_model=Sequence[TagResponse], summary="Поиск тегов по имени"
)
async def search_tags(
    name: str,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tags = await search_tags_by_name(session, name, current_user["id"])
    return tags


@router.get(
    "/{tag_id}/tasks",
    response_model=Sequence[TaskResponse],
    summary="Получить все задачи по тегу",
)
async def get_tasks_by_tag(
    tag_id: int,
    is_complited: bool | None = None,
    skip: int = 0,
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tasks = await get_tasks_for_tag(session, tag_id, current_user["id"], is_complited, skip, limit)
    return tasks
