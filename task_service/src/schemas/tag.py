from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class TagCreate(BaseModel):
    name: str = Field(..., max_length=100)


class TagResponse(BaseModel):
    id: int
    name: str
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
