from sqlalchemy import Table, Column, Integer, ForeignKey
from src.db.base import Base

task_tag_table = Table(
    "task_tag",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)
