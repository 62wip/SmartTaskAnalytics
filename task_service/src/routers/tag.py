from fastapi import APIRouter, Depends, status
from src.dependencies.auth import get_current_user

from src.db.session import get_session
from src.schemas.tag import TagCreate, TagResponse
from src.crud.tag import *

router = APIRouter()


@router.post(
    "/create",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ручка для регистрации",
)
async def create_task(
    task_data: TagCreate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    tag = await create_tag(session, task_data.name, current_user["id"])
    return tag
