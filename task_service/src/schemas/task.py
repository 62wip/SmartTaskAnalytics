from datetime import UTC, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.schemas.tag import TagResponse


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    priority: int = Field(3, ge=1, le=5)
    deadline: Optional[datetime] = Field(None)
    tags: List[TagResponse] = Field(default_factory=list)

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value is not None:
            now = datetime.now(UTC)
            if value.tzinfo is None:
                value = value.replace(tzinfo=UTC)
            else:
                value = value.astimezone(UTC)

            if value <= now:
                raise ValueError("Deadline must be in the future")
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
    tags: List[TagResponse]

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[int] = Field(None, ge=1, le=5)
    deadline: Optional[datetime] = None
    is_completed: Optional[bool] = None
    tag_ids: Optional[List[int]] = None

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value is not None:
            now = datetime.now(UTC)
            if value.tzinfo is None:
                value = value.replace(tzinfo=UTC)
            else:
                value = value.astimezone(UTC)

            if value <= now:
                raise ValueError("Deadline must be in the future")
        return value

class DeadlineShiftRequest(BaseModel):
    days: int = Field(0, description="Дней для переноса")
    hours: int = Field(0, description="Часов для переноса")
    minutes: int = Field(0, description="Минут для переноса")