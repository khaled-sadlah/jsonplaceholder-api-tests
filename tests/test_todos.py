import pytest
import requests
from config.urls import (
    TODOS_URL,
    TODO_BY_ID_URL,
    TODOS_BY_USER_ID_URL,
    TODOS_COMPLETED_URL,
)


class TestGetTodos:

    def test_get_all_todos_status_200(self):
        response = requests.get(TODOS_URL)
        assert response.status_code == 200

    def test_get_all_todos_returns_list(self):
        response = requests.get(TODOS_URL)
        assert isinstance(response.json(), list)

    def test_get_all_todos_returns_200(self):
        response = requests.get(TODOS_URL)
        assert len(response.json()) == 200

    def test_get_all_todos_fields_exist(self):
        todo = requests.get(TODOS_URL).json()[0]
        assert "userId" in todo
        assert "id" in todo
        assert "title" in todo
        assert "completed" in todo

    def test_get_todo_by_id_status_200(self):
        url = TODO_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_todo_by_id_correct_id(self):
        url = TODO_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.json()["id"] == 1

    def test_get_todo_by_id_completed_is_bool(self):
        url = TODO_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert isinstance(response.json()["completed"], bool)

    def test_get_todo_not_found_status_404(self):
        url = TODO_BY_ID_URL.format(id=9999)
        response = requests.get(url)
        assert response.status_code == 404

    def test_get_todo_not_found_empty_body(self):
        url = TODO_BY_ID_URL.format(id=9999)
        response = requests.get(url)
        assert response.json() == {}

    def test_get_todos_by_user_id_status_200(self):
        url = TODOS_BY_USER_ID_URL.format(userId=1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_todos_by_user_id_all_belong_to_user(self):
        url = TODOS_BY_USER_ID_URL.format(userId=1)
        response = requests.get(url)
        for todo in response.json():
            assert todo["userId"] == 1

    def test_get_completed_todos_all_true(self):
        url = TODOS_COMPLETED_URL.format(completed="true")
        response = requests.get(url)
        assert response.status_code == 200
        for todo in response.json():
            assert todo["completed"] is True

    def test_get_incomplete_todos_all_false(self):
        url = TODOS_COMPLETED_URL.format(completed="false")
        response = requests.get(url)
        assert response.status_code == 200
        for todo in response.json():
            assert todo["completed"] is False


class TestCreateTodo:

    def test_create_todo_status_201(self):
        payload = {"userId": 1, "title": "buy groceries", "completed": False}
        response = requests.post(TODOS_URL, json=payload)
        assert response.status_code == 201

    def test_create_todo_returns_id(self):
        payload = {"userId": 1, "title": "buy groceries", "completed": False}
        response = requests.post(TODOS_URL, json=payload)
        assert "id" in response.json()

    def test_create_todo_completed_is_false(self):
        payload = {"userId": 1, "title": "buy groceries", "completed": False}
        response = requests.post(TODOS_URL, json=payload)
        assert response.json()["completed"] is False

    def test_create_todo_empty_body(self):
        response = requests.post(TODOS_URL, json={})
        assert response.status_code == 201
        assert "id" in response.json()


class TestUpdateTodo:

    def test_update_todo_status_200(self):
        url = TODO_BY_ID_URL.format(id=1)
        payload = {"userId": 1, "id": 1, "title": "updated todo", "completed": True}
        response = requests.put(url, json=payload)
        assert response.status_code == 200

    def test_update_todo_title_changed(self):
        url = TODO_BY_ID_URL.format(id=1)
        payload = {"userId": 1, "id": 1, "title": "updated todo", "completed": True}
        response = requests.put(url, json=payload)
        assert response.json()["title"] == "updated todo"

    def test_update_todo_completed_is_true(self):
        url = TODO_BY_ID_URL.format(id=1)
        payload = {"userId": 1, "id": 1, "title": "updated todo", "completed": True}
        response = requests.put(url, json=payload)
        assert response.json()["completed"] is True

    def test_update_todo_not_found_status_500(self):
        url = TODO_BY_ID_URL.format(id=9999)
        response = requests.put(url, json={"title": "ghost todo"})
        assert response.status_code == 500


class TestPatchTodo:

    def test_patch_todo_completed_status_200(self):
        url = TODO_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"completed": True})
        assert response.status_code == 200

    def test_patch_todo_completed_updated(self):
        url = TODO_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"completed": True})
        assert response.json()["completed"] is True

    def test_patch_todo_not_found_status_500(self):
        url = TODO_BY_ID_URL.format(id=9999)
        response = requests.patch(url, json={"completed": True})
        assert response.status_code == 500


class TestDeleteTodo:

    def test_delete_todo_status_200(self):
        url = TODO_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.status_code == 200

    def test_delete_todo_returns_empty_object(self):
        url = TODO_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.json() == {}

    def test_delete_todo_not_found_status_404(self):
        url = TODO_BY_ID_URL.format(id=9999)
        response = requests.delete(url)
        assert response.status_code == 404
