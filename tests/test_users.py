import pytest
import requests
from config.urls import (
    USERS_URL,
    USER_BY_ID_URL,
    USER_BY_USERNAME_URL,
)


class TestGetUsers:

    def test_get_all_users_status_200(self):
        response = requests.get(USERS_URL)
        assert response.status_code == 200

    def test_get_all_users_returns_list(self):
        response = requests.get(USERS_URL)
        assert isinstance(response.json(), list)

    def test_get_all_users_returns_10(self):
        response = requests.get(USERS_URL)
        assert len(response.json()) == 10

    def test_get_all_users_fields_exist(self):
        user = requests.get(USERS_URL).json()[0]
        for field in ["id", "name", "username", "email", "address", "phone", "website", "company"]:
            assert field in user

    def test_get_user_by_id_status_200(self):
        url = USER_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_user_by_id_correct_id(self):
        url = USER_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.json()["id"] == 1

    def test_get_user_by_id_email_has_at(self):
        url = USER_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert "@" in response.json()["email"]

    def test_get_user_by_id_address_has_city(self):
        url = USER_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert isinstance(response.json()["address"]["city"], str)

    def test_get_user_not_found_status_404(self):
        url = USER_BY_ID_URL.format(id=9999)
        response = requests.get(url)
        assert response.status_code == 404

    def test_get_user_not_found_empty_body(self):
        url = USER_BY_ID_URL.format(id=9999)
        response = requests.get(url)
        assert response.json() == {}

    def test_get_user_by_username_status_200(self):
        url = USER_BY_USERNAME_URL.format(username="Bret")
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_user_by_username_correct_user(self):
        url = USER_BY_USERNAME_URL.format(username="Bret")
        response = requests.get(url)
        assert response.json()[0]["username"] == "Bret"

    def test_get_user_by_username_returns_one(self):
        url = USER_BY_USERNAME_URL.format(username="Bret")
        response = requests.get(url)
        assert len(response.json()) == 1

    def test_get_user_invalid_username_returns_empty(self):
        url = USER_BY_USERNAME_URL.format(username="notexists123")
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json() == []


class TestCreateUser:

    def test_create_user_status_201(self):
        payload = {
            "name": "John Doe",
            "username": "johndoe",
            "email": "john@example.com",
            "phone": "1-234-567-8901",
            "website": "johndoe.com",
        }
        response = requests.post(USERS_URL, json=payload)
        assert response.status_code == 201

    def test_create_user_returns_id(self):
        payload = {
            "name": "John Doe",
            "username": "johndoe",
            "email": "john@example.com",
        }
        response = requests.post(USERS_URL, json=payload)
        assert "id" in response.json()

    def test_create_user_name_matches(self):
        payload = {"name": "John Doe", "username": "johndoe", "email": "john@example.com"}
        response = requests.post(USERS_URL, json=payload)
        assert response.json()["name"] == "John Doe"

    def test_create_user_empty_body(self):
        response = requests.post(USERS_URL, json={})
        assert response.status_code == 201
        assert "id" in response.json()


class TestUpdateUser:

    def test_update_user_status_200(self):
        url = USER_BY_ID_URL.format(id=1)
        payload = {
            "id": 1,
            "name": "updated name",
            "username": "updated_username",
            "email": "updated@example.com",
        }
        response = requests.put(url, json=payload)
        assert response.status_code == 200

    def test_update_user_name_changed(self):
        url = USER_BY_ID_URL.format(id=1)
        payload = {
            "id": 1,
            "name": "updated name",
            "username": "updated_username",
            "email": "updated@example.com",
        }
        response = requests.put(url, json=payload)
        assert response.json()["name"] == "updated name"

    def test_update_user_not_found_status_500(self):
        url = USER_BY_ID_URL.format(id=9999)
        response = requests.put(url, json={"name": "ghost user"})
        assert response.status_code == 500


class TestPatchUser:

    def test_patch_user_email_status_200(self):
        url = USER_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"email": "newemail@example.com"})
        assert response.status_code == 200

    def test_patch_user_email_updated(self):
        url = USER_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"email": "newemail@example.com"})
        assert response.json()["email"] == "newemail@example.com"

    def test_patch_user_other_fields_still_exist(self):
        url = USER_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"email": "newemail@example.com"})
        assert "name" in response.json()

    def test_patch_user_not_found_status_500(self):
        url = USER_BY_ID_URL.format(id=9999)
        response = requests.patch(url, json={"email": "ghost@example.com"})
        assert response.status_code == 500


class TestDeleteUser:

    def test_delete_user_status_200(self):
        url = USER_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.status_code == 200

    def test_delete_user_returns_empty_object(self):
        url = USER_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.json() == {}

    def test_delete_user_not_found_status_404(self):
        url = USER_BY_ID_URL.format(id=9999)
        response = requests.delete(url)
        assert response.status_code == 404
