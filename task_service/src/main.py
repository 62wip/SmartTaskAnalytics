from fastapi import FastAPI
from src.routers.task import router as task_router
from src.routers.tag import router as tag_router

app = FastAPI(title="Task Service")

app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(tag_router, prefix="/tags", tags=["tags"])
