from datetime import UTC, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    priority: int = Field(3, ge=1, le=5)
    deadline: Optional[datetime] = Field(None)
    is_completed: bool = Field(False)
    tags_ids: List[int] = Field(default_factory=list)

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value is not None and value <= datetime.now(UTC):
            raise ValueError("Deadline must be in the future.")
        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    created_at: datetime
    deadline: Optional[datetime]
    is_completed: bool
    author_id: int
    tag_ids: List[int]

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[int] = Field(None, ge=1, le=5)
    deadline: Optional[datetime] = None
    is_completed: Optional[bool] = None
    tag_ids: Optional[List[int]] = None
