import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.task_model import Base, Task, TaskStatus
from app.repositories.task_repository import TaskRepository

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_task(db_session):
    task_repository = TaskRepository(db_session)
    task = task_repository.create_task("Test Task", "This is a test task")
    assert task.title == "Test Task"

def test_get_task_by_id(db_session):
    task_repository = TaskRepository(db_session)
    task = task_repository.create_task("Test Task", "This is a test task")
    fetched_task = task_repository.get_task_by_id(task.id)
    assert fetched_task.id == task.id

def test_update_task(db_session):
    task_repository = TaskRepository(db_session)
    task = task_repository.create_task("Task to update", "This is a test task")
    updated_task = task_repository.update_task(task.id, title="Updated Task", description="Updated description", status=TaskStatus.COMPLETED)
    assert updated_task.title == "Updated Task"
    assert updated_task.status == TaskStatus.COMPLETED

def test_delete_task(db_session):
    task_repository = TaskRepository(db_session)
    task = task_repository.create_task("Task to delete", "This is a test task")
    task_repository.delete_task(task.id)
    deleted_task = task_repository.get_task_by_id(task.id)
    assert deleted_task is None