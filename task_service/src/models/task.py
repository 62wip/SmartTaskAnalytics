from datetime import UTC, datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.db.base import Base
from src.models.task_tag import task_tag_table
from models.tag import Tag


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True, default="")
    priority = Column(Integer, nullable=False, default=3)
    created_at = Column(DateTime, default=datetime.now(UTC))
    deadline = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    author_id = Column(Integer, nullable=False)
    tags = relationship("Tag", secondary=task_tag_table, backref="tasks")
