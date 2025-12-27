from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Priority = Literal["low", "medium", "high"]
Category = Literal["work", "study", "home", "other"]


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=2000)
    priority: Priority = "medium"
    category: Category = "other"
    important: bool = False
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    created_at: datetime


class ErrorResponse(BaseModel):
    detail: str
