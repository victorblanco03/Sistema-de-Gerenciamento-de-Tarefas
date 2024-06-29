from sqlalchemy.orm import Session
from app.repositories.task_repository import TaskRepository
from app.models.task_model import TaskStatus

class TaskService:

    def __init__(self, db: Session):
        self.task_repository = TaskRepository(db)

    def create_task(self, title: str, description: str):
        if not title:
            raise ValueError("Title is required")
        return self.task_repository.create_task(title, description)

    def get_task_by_id(self, task_id: int):
        return self.task_repository.get_task_by_id(task_id)

    def update_task(self, task_id: int, title: str = None, description: str = None, status: TaskStatus = None):
        return self.task_repository.update_task(task_id, title, description, status)

    def delete_task(self, task_id: int):
        return self.task_repository.delete_task(task_id)

    def list_tasks(self):
        return self.task_repository.list_tasks()