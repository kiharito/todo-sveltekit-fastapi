from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_task_crud():
    response = client.post(
        "/tasks/",
        json={"title": "New Task"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Task"
    task_id = data["id"]

    response = client.get("/tasks/{}".format(task_id))
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Task"
    assert data["id"] == task_id

    response = client.put(
        "/tasks/{}".format(task_id),
        json={"title": "Updated Task"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["id"] == task_id

    response = client.get("/tasks/{}".format(task_id))
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["id"] == task_id

    response = client.delete("/tasks/{}".format(task_id))
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task deleted"

    response = client.get("/tasks/{}".format(task_id))
    assert response.status_code == 404
