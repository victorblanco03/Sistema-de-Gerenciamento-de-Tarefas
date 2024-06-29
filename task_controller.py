
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.task_model import TaskStatus
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter()

@router.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    return task_service.create_task(task.title, task.description)

@router.get("/tasks/", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    task_service = TaskService(db)
    return task_service.list_tasks()

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task = task_service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    updated_task = task_service.update_task(task_id, task.title, task.description, task.status)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task = task_service.delete_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task