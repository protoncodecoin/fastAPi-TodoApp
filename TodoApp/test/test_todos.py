from fastapi import status
from ..main import app
from ..routers.todos import get_db, get_current_user
from ..models import Todos

from .utils import (
    override_get_current_user,
    override_get_db,
    test_todo,
    client,
    TestingSessionLocal,
)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "complete": False,
            "description": "Need to learn everyday!",
            "id": 1,
            "owner_id": 1,
            "priority": 5,
            "title": "Learn to code!",
        }
    ]


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "complete": False,
        "description": "Need to learn everyday!",
        "id": 1,
        "owner_id": 1,
        "priority": 5,
        "title": "Learn to code!",
    }


def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Resource not found"}


def test_create_todo(test_todo):
    request_data = {
        "complete": False,
        "description": "New todo",
        "owner_id": 1,
        "priority": 3,
        "title": "New Todo",
    }
    response = client.post("/todos/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model: Todos = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.complete == request_data.get("complete")
    assert model.priority == request_data.get("priority")


def test_update_todos(test_todo):
    request_data = {
        "complete": True,
        "description": "Decided to learn c++",
        "owner_id": 1,
        "priority": 4,
        "title": "Continue Learning C++",
    }

    response = client.put("todos/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model.title == request_data.get("title")


def test_update_not_todos(test_todo):
    request_data = {
        "complete": True,
        "description": "Decided to learn c++",
        "owner_id": 1,
        "priority": 4,
        "title": "Continue Learning C++",
    }

    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(test_todo):
    response = client.delete("/todos/delete/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None


def test_todo_not_found():
    response = client.delete("/todos/delete/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
