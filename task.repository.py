from sqlalchemy.orm import Session
from app.models.task_model import Task, TaskStatus

class TaskRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, description: str):
        new_task = Task(title=title, description=description)
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def get_task_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def update(self, task_id: int, title: str = None, description: str = None, status: TaskStatus = None):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if status:
                task.status = status
            self.db.commit()
            self.db.refresh(task)
        return task

    def delete(self, task_id: int):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task:
            self.db.delete(task)
            self.db.commit()
        return task

    def list(self):
        return self.db.query(Task).all()