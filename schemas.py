from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.task_model import TaskStatus

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime

    class Config:
        orm_mode = True