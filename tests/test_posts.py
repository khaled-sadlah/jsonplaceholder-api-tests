import pytest
import requests
from config.urls import (
    POSTS_URL,
    POST_BY_ID_URL,
    POSTS_BY_USER_ID_URL,
)


class TestGetPosts:

    def test_get_all_posts_status_200(self):
        response = requests.get(POSTS_URL)
        assert response.status_code == 200

    def test_get_all_posts_returns_list(self):
        response = requests.get(POSTS_URL)
        assert isinstance(response.json(), list)

    def test_get_all_posts_returns_100_posts(self):
        response = requests.get(POSTS_URL)
        assert len(response.json()) == 100

    def test_get_all_posts_fields_exist(self):
        response = requests.get(POSTS_URL)
        post = response.json()[0]
        assert "userId" in post
        assert "id" in post
        assert "title" in post
        assert "body" in post

    def test_get_post_by_id_status_200(self):
        url = POST_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_post_by_id_correct_id(self):
        url = POST_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.json()["id"] == 1

    def test_get_post_by_id_title_is_string(self):
        url = POST_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert isinstance(response.json()["title"], str)

    def test_get_post_not_found_status_404(self):
        url = POST_BY_ID_URL.format(id=9999)
        response = requests.get(url)
        assert response.status_code == 404

    def test_get_post_not_found_empty_body(self):
        url = POST_BY_ID_URL.format(id=9999)
        response = requests.get(url)
        assert response.json() == {}

    def test_get_posts_by_user_id_status_200(self):
        url = POSTS_BY_USER_ID_URL.format(userId=1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_posts_by_user_id_all_belong_to_user(self):
        url = POSTS_BY_USER_ID_URL.format(userId=1)
        response = requests.get(url)
        for post in response.json():
            assert post["userId"] == 1

    def test_get_posts_by_user_id_returns_10(self):
        url = POSTS_BY_USER_ID_URL.format(userId=1)
        response = requests.get(url)
        assert len(response.json()) == 10

    def test_get_posts_invalid_user_id_returns_empty(self):
        url = POSTS_BY_USER_ID_URL.format(userId=9999)
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json() == []


class TestCreatePost:

    def test_create_post_status_201(self):
        payload = {"userId": 1, "title": "my new post", "body": "post body content"}
        response = requests.post(POSTS_URL, json=payload)
        assert response.status_code == 201

    def test_create_post_returns_id(self):
        payload = {"userId": 1, "title": "my new post", "body": "post body content"}
        response = requests.post(POSTS_URL, json=payload)
        assert "id" in response.json()

    def test_create_post_title_matches(self):
        payload = {"userId": 1, "title": "my new post", "body": "post body content"}
        response = requests.post(POSTS_URL, json=payload)
        assert response.json()["title"] == "my new post"

    def test_create_post_userId_matches(self):
        payload = {"userId": 1, "title": "my new post", "body": "post body content"}
        response = requests.post(POSTS_URL, json=payload)
        assert response.json()["userId"] == 1

    def test_create_post_without_id_server_assigns(self):
        payload = {"userId": 2, "title": "post without id", "body": "body content"}
        response = requests.post(POSTS_URL, json=payload)
        assert response.status_code == 201
        assert isinstance(response.json()["id"], int)

    def test_create_post_with_duplicate_id(self):
        payload = {"id": 1, "userId": 1, "title": "duplicate id post", "body": "body"}
        response = requests.post(POSTS_URL, json=payload)
        assert response.status_code == 201
        assert response.json()["id"] == 1

    def test_create_post_with_empty_body(self):
        response = requests.post(POSTS_URL, json={})
        assert response.status_code == 201
        assert "id" in response.json()

    def test_create_post_missing_title(self):
        payload = {"userId": 1, "body": "post without a title"}
        response = requests.post(POSTS_URL, json=payload)
        assert response.status_code == 201
        assert "title" not in response.json()


class TestUpdatePost:

    def test_update_post_status_200(self):
        url = POST_BY_ID_URL.format(id=1)
        payload = {"id": 1, "userId": 1, "title": "updated title", "body": "updated body"}
        response = requests.put(url, json=payload)
        assert response.status_code == 200

    def test_update_post_title_changed(self):
        url = POST_BY_ID_URL.format(id=1)
        payload = {"id": 1, "userId": 1, "title": "updated title", "body": "updated body"}
        response = requests.put(url, json=payload)
        assert response.json()["title"] == "updated title"

    def test_update_post_id_unchanged(self):
        url = POST_BY_ID_URL.format(id=1)
        payload = {"id": 1, "userId": 1, "title": "updated title", "body": "updated body"}
        response = requests.put(url, json=payload)
        assert response.json()["id"] == 1

    def test_update_post_not_found_status_500(self):
        url = POST_BY_ID_URL.format(id=9999)
        payload = {"id": 9999, "userId": 1, "title": "ghost", "body": "ghost body"}
        response = requests.put(url, json=payload)
        assert response.status_code == 500

    def test_update_post_empty_body_status_200(self):
        url = POST_BY_ID_URL.format(id=1)
        response = requests.put(url, json={})
        assert response.status_code == 200

    def test_update_post_title_only(self):
        url = POST_BY_ID_URL.format(id=1)
        payload = {"title": "only title updated"}
        response = requests.put(url, json=payload)
        assert response.status_code == 200
        assert response.json()["title"] == "only title updated"

    def test_update_post_invalid_data_types(self):
        url = POST_BY_ID_URL.format(id=1)
        payload = {"userId": "abc", "id": "xyz", "title": 99999, "body": None}
        response = requests.put(url, json=payload)
        assert response.status_code == 200


class TestPatchPost:

    def test_patch_post_title_status_200(self):
        url = POST_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"title": "patched title"})
        assert response.status_code == 200

    def test_patch_post_title_updated(self):
        url = POST_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"title": "patched title"})
        assert response.json()["title"] == "patched title"

    def test_patch_post_other_fields_still_exist(self):
        url = POST_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"title": "patched title"})
        assert "body" in response.json()
        assert "userId" in response.json()

    def test_patch_post_not_found_status_500(self):
        url = POST_BY_ID_URL.format(id=9999)
        response = requests.patch(url, json={"title": "patching ghost post"})
        assert response.status_code == 500


class TestDeletePost:

    def test_delete_post_status_200(self):
        url = POST_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.status_code == 200

    def test_delete_post_returns_empty_object(self):
        url = POST_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.json() == {}

    def test_delete_post_not_found_status_404(self):
        url = POST_BY_ID_URL.format(id=9999)
        response = requests.delete(url)
        assert response.status_code == 404
