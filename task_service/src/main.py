from fastapi import FastAPI
from src.routers.task import router as task_router

app = FastAPI(title="Task Service")

app.include_router(task_router, prefix="/task", tags=["task"])
