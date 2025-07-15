from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TagCreate(BaseModel):
    name: str = Field(..., max_length=100)


class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)


class TagResponse(BaseModel):
    id: int
    name: str
    author_id: int
