from fastapi import APIRouter, Depends
from src.dependencies.auth import get_current_user

router = APIRouter()

# @router.post("/create")
# async def create_task(task_data: TaskCreate, current_user: dict = Depends(get_current_user),  # Требуем авторизацию
# ):
#     # current_user — это данные, которые вернул auth_service (например, {"id": 1, "email": "user@example.com"})
#     task = Task(
#         title=task_data.title,
#         author_id=current_user["id"],  # Берём ID пользователя из токена
#         ...
#     )
#     ...