import pytest
import requests
from config.urls import (
    ALBUMS_URL,
    ALBUM_BY_ID_URL,
    ALBUMS_BY_USER_ID_URL,
)


class TestGetAlbums:

    def test_get_all_albums_status_200(self):
        response = requests.get(ALBUMS_URL)
        assert response.status_code == 200

    def test_get_all_albums_returns_list(self):
        response = requests.get(ALBUMS_URL)
        assert isinstance(response.json(), list)

    def test_get_all_albums_returns_100(self):
        response = requests.get(ALBUMS_URL)
        assert len(response.json()) == 100

    def test_get_all_albums_fields_exist(self):
        album = requests.get(ALBUMS_URL).json()[0]
        assert "userId" in album
        assert "id" in album
        assert "title" in album

    def test_get_album_by_id_status_200(self):
        url = ALBUM_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_album_by_id_correct_id(self):
        url = ALBUM_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.json()["id"] == 1

    def test_get_album_by_id_title_is_string(self):
        url = ALBUM_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert isinstance(response.json()["title"], str)

    def test_get_album_not_found_status_404(self):
        url = ALBUM_BY_ID_URL.format(id=9999)
        response = requests.get(url)
        assert response.status_code == 404

    def test_get_album_not_found_empty_body(self):
        url = ALBUM_BY_ID_URL.format(id=9999)
        response = requests.get(url)
        assert response.json() == {}

    def test_get_albums_by_user_id_status_200(self):
        url = ALBUMS_BY_USER_ID_URL.format(userId=1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_albums_by_user_id_all_belong_to_user(self):
        url = ALBUMS_BY_USER_ID_URL.format(userId=1)
        response = requests.get(url)
        for album in response.json():
            assert album["userId"] == 1

    def test_get_albums_invalid_user_id_returns_empty(self):
        url = ALBUMS_BY_USER_ID_URL.format(userId=9999)
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json() == []


class TestCreateAlbum:

    def test_create_album_status_201(self):
        payload = {"userId": 1, "title": "my new album"}
        response = requests.post(ALBUMS_URL, json=payload)
        assert response.status_code == 201

    def test_create_album_returns_id(self):
        payload = {"userId": 1, "title": "my new album"}
        response = requests.post(ALBUMS_URL, json=payload)
        assert "id" in response.json()

    def test_create_album_title_matches(self):
        payload = {"userId": 1, "title": "my new album"}
        response = requests.post(ALBUMS_URL, json=payload)
        assert response.json()["title"] == "my new album"

    def test_create_album_empty_body(self):
        response = requests.post(ALBUMS_URL, json={})
        assert response.status_code == 201
        assert "id" in response.json()


class TestUpdateAlbum:

    def test_update_album_status_200(self):
        url = ALBUM_BY_ID_URL.format(id=1)
        payload = {"userId": 1, "id": 1, "title": "updated album title"}
        response = requests.put(url, json=payload)
        assert response.status_code == 200

    def test_update_album_title_changed(self):
        url = ALBUM_BY_ID_URL.format(id=1)
        payload = {"userId": 1, "id": 1, "title": "updated album title"}
        response = requests.put(url, json=payload)
        assert response.json()["title"] == "updated album title"

    def test_update_album_not_found_status_500(self):
        url = ALBUM_BY_ID_URL.format(id=9999)
        response = requests.put(url, json={"title": "ghost album"})
        assert response.status_code == 500


class TestPatchAlbum:

    def test_patch_album_title_status_200(self):
        url = ALBUM_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"title": "patched album title"})
        assert response.status_code == 200

    def test_patch_album_title_updated(self):
        url = ALBUM_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"title": "patched album title"})
        assert response.json()["title"] == "patched album title"

    def test_patch_album_not_found_status_500(self):
        url = ALBUM_BY_ID_URL.format(id=9999)
        response = requests.patch(url, json={"title": "ghost patch"})
        assert response.status_code == 500


class TestDeleteAlbum:

    def test_delete_album_status_200(self):
        url = ALBUM_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.status_code == 200

    def test_delete_album_returns_empty_object(self):
        url = ALBUM_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.json() == {}

    def test_delete_album_not_found_status_404(self):
        url = ALBUM_BY_ID_URL.format(id=9999)
        response = requests.delete(url)
        assert response.status_code == 404
