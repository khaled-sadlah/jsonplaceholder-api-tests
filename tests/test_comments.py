import pytest
import requests
from config.urls import (
    COMMENTS_URL,
    COMMENT_BY_ID_URL,
    COMMENTS_BY_POST_ID_URL,
)


class TestGetComments:

    def test_get_all_comments_status_200(self):
        response = requests.get(COMMENTS_URL)
        assert response.status_code == 200

    def test_get_all_comments_returns_list(self):
        response = requests.get(COMMENTS_URL)
        assert isinstance(response.json(), list)

    def test_get_all_comments_returns_500(self):
        response = requests.get(COMMENTS_URL)
        assert len(response.json()) == 500

    def test_get_all_comments_fields_exist(self):
        comment = requests.get(COMMENTS_URL).json()[0]
        assert "postId" in comment
        assert "id" in comment
        assert "name" in comment
        assert "email" in comment
        assert "body" in comment

    def test_get_comment_by_id_status_200(self):
        url = COMMENT_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_comment_by_id_correct_id(self):
        url = COMMENT_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.json()["id"] == 1

    def test_get_comment_by_id_email_format(self):
        url = COMMENT_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert "@" in response.json()["email"]

    def test_get_comment_not_found_status_404(self):
        url = COMMENT_BY_ID_URL.format(id=9999)
        response = requests.get(url)
        assert response.status_code == 404

    def test_get_comment_not_found_empty_body(self):
        url = COMMENT_BY_ID_URL.format(id=9999)
        response = requests.get(url)
        assert response.json() == {}

    def test_get_comments_by_post_id_status_200(self):
        url = COMMENTS_BY_POST_ID_URL.format(postId=1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_comments_by_post_id_all_belong_to_post(self):
        url = COMMENTS_BY_POST_ID_URL.format(postId=1)
        response = requests.get(url)
        for comment in response.json():
            assert comment["postId"] == 1

    def test_get_comments_by_post_id_returns_5(self):
        url = COMMENTS_BY_POST_ID_URL.format(postId=1)
        response = requests.get(url)
        assert len(response.json()) == 5

    def test_get_comments_invalid_post_id_returns_empty(self):
        url = COMMENTS_BY_POST_ID_URL.format(postId=9999)
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json() == []


class TestCreateComment:

    def test_create_comment_status_201(self):
        payload = {
            "postId": 1,
            "name": "test user",
            "email": "testuser@mail.com",
            "body": "this is a test comment",
        }
        response = requests.post(COMMENTS_URL, json=payload)
        assert response.status_code == 201

    def test_create_comment_returns_id(self):
        payload = {
            "postId": 1,
            "name": "test user",
            "email": "testuser@mail.com",
            "body": "this is a test comment",
        }
        response = requests.post(COMMENTS_URL, json=payload)
        assert "id" in response.json()

    def test_create_comment_email_matches(self):
        payload = {
            "postId": 1,
            "name": "test user",
            "email": "testuser@mail.com",
            "body": "this is a test comment",
        }
        response = requests.post(COMMENTS_URL, json=payload)
        assert response.json()["email"] == "testuser@mail.com"

    def test_create_comment_empty_body(self):
        response = requests.post(COMMENTS_URL, json={})
        assert response.status_code == 201
        assert "id" in response.json()


class TestUpdateComment:

    def test_update_comment_status_200(self):
        url = COMMENT_BY_ID_URL.format(id=1)
        payload = {
            "postId": 1,
            "id": 1,
            "name": "updated name",
            "email": "updated@mail.com",
            "body": "updated comment body",
        }
        response = requests.put(url, json=payload)
        assert response.status_code == 200

    def test_update_comment_name_changed(self):
        url = COMMENT_BY_ID_URL.format(id=1)
        payload = {
            "postId": 1,
            "id": 1,
            "name": "updated name",
            "email": "updated@mail.com",
            "body": "updated comment body",
        }
        response = requests.put(url, json=payload)
        assert response.json()["name"] == "updated name"

    def test_update_comment_not_found_status_500(self):
        url = COMMENT_BY_ID_URL.format(id=9999)
        response = requests.put(url, json={"name": "ghost"})
        assert response.status_code == 500


class TestPatchComment:

    def test_patch_comment_body_status_200(self):
        url = COMMENT_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"body": "patched comment body"})
        assert response.status_code == 200

    def test_patch_comment_body_updated(self):
        url = COMMENT_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"body": "patched comment body"})
        assert response.json()["body"] == "patched comment body"

    def test_patch_comment_not_found_status_500(self):
        url = COMMENT_BY_ID_URL.format(id=9999)
        response = requests.patch(url, json={"body": "patching ghost comment"})
        assert response.status_code == 500


class TestDeleteComment:

    def test_delete_comment_status_200(self):
        url = COMMENT_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.status_code == 200

    def test_delete_comment_returns_empty_object(self):
        url = COMMENT_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.json() == {}

    def test_delete_comment_not_found_status_404(self):
        url = COMMENT_BY_ID_URL.format(id=9999)
        response = requests.delete(url)
        assert response.status_code == 404
