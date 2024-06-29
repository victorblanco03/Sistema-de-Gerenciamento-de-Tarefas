import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_create_task(client):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "This is a test task"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_list_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task(client):
    response = client.post("/tasks/", json={"title": "Task to get", "description": "This is a test task"})
    task_id = response.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Task to get"

def test_update_task(client):
    response = client.post("/tasks/", json={"title": "Task to update", "description": "This is a test task"})
    task_id = response.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Task", "description": "Updated description", "status": "Concluída"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["status"] == "Concluída"

def test_delete_task(client):
    response = client.post("/tasks/", json={"title": "Task to delete", "description": "This is a test task"})
    task_id = response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Task to delete"
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404