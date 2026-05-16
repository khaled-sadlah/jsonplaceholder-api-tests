import pytest
import requests
from config.urls import (
    PHOTOS_URL,
    PHOTO_BY_ID_URL,
    PHOTOS_BY_ALBUM_ID_URL,
)


class TestGetPhotos:

    def test_get_all_photos_status_200(self):
        response = requests.get(PHOTOS_URL)
        assert response.status_code == 200

    def test_get_all_photos_returns_list(self):
        response = requests.get(PHOTOS_URL)
        assert isinstance(response.json(), list)

    def test_get_all_photos_returns_5000(self):
        response = requests.get(PHOTOS_URL)
        assert len(response.json()) == 5000

    def test_get_all_photos_fields_exist(self):
        photo = requests.get(PHOTOS_URL).json()[0]
        assert "albumId" in photo
        assert "id" in photo
        assert "title" in photo
        assert "url" in photo
        assert "thumbnailUrl" in photo

    def test_get_photo_by_id_status_200(self):
        url = PHOTO_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_photo_by_id_correct_id(self):
        url = PHOTO_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert response.json()["id"] == 1

    def test_get_photo_by_id_url_is_string(self):
        url = PHOTO_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert isinstance(response.json()["url"], str)

    def test_get_photo_by_id_thumbnail_is_string(self):
        url = PHOTO_BY_ID_URL.format(id=1)
        response = requests.get(url)
        assert isinstance(response.json()["thumbnailUrl"], str)

    def test_get_photo_not_found_status_404(self):
        url = PHOTO_BY_ID_URL.format(id=9999999)
        response = requests.get(url)
        assert response.status_code == 404

    def test_get_photo_not_found_empty_body(self):
        url = PHOTO_BY_ID_URL.format(id=9999999)
        response = requests.get(url)
        assert response.json() == {}

    def test_get_photos_by_album_id_status_200(self):
        url = PHOTOS_BY_ALBUM_ID_URL.format(albumId=1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_get_photos_by_album_id_all_belong_to_album(self):
        url = PHOTOS_BY_ALBUM_ID_URL.format(albumId=1)
        response = requests.get(url)
        for photo in response.json():
            assert photo["albumId"] == 1

    def test_get_photos_by_album_id_returns_50(self):
        url = PHOTOS_BY_ALBUM_ID_URL.format(albumId=1)
        response = requests.get(url)
        assert len(response.json()) == 50

    def test_get_photos_invalid_album_id_returns_empty(self):
        url = PHOTOS_BY_ALBUM_ID_URL.format(albumId=9999)
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json() == []


class TestCreatePhoto:

    def test_create_photo_status_201(self):
        payload = {
            "albumId": 1,
            "title": "new photo title",
            "url": "https://via.placeholder.com/600/test",
            "thumbnailUrl": "https://via.placeholder.com/150/test",
        }
        response = requests.post(PHOTOS_URL, json=payload)
        assert response.status_code == 201

    def test_create_photo_returns_id(self):
        payload = {
            "albumId": 1,
            "title": "new photo title",
            "url": "https://via.placeholder.com/600/test",
            "thumbnailUrl": "https://via.placeholder.com/150/test",
        }
        response = requests.post(PHOTOS_URL, json=payload)
        assert "id" in response.json()

    def test_create_photo_title_matches(self):
        payload = {
            "albumId": 1,
            "title": "new photo title",
            "url": "https://via.placeholder.com/600/test",
            "thumbnailUrl": "https://via.placeholder.com/150/test",
        }
        response = requests.post(PHOTOS_URL, json=payload)
        assert response.json()["title"] == "new photo title"


class TestUpdatePhoto:

    def test_update_photo_status_200(self):
        url = PHOTO_BY_ID_URL.format(id=1)
        payload = {
            "albumId": 1,
            "id": 1,
            "title": "updated photo title",
            "url": "https://via.placeholder.com/600/updated",
            "thumbnailUrl": "https://via.placeholder.com/150/updated",
        }
        response = requests.put(url, json=payload)
        assert response.status_code == 200

    def test_update_photo_title_changed(self):
        url = PHOTO_BY_ID_URL.format(id=1)
        payload = {
            "albumId": 1,
            "id": 1,
            "title": "updated photo title",
            "url": "https://via.placeholder.com/600/updated",
            "thumbnailUrl": "https://via.placeholder.com/150/updated",
        }
        response = requests.put(url, json=payload)
        assert response.json()["title"] == "updated photo title"

    def test_update_photo_not_found_status_500(self):
        url = PHOTO_BY_ID_URL.format(id=9999999)
        response = requests.put(url, json={"title": "ghost photo"})
        assert response.status_code == 500


class TestPatchPhoto:

    def test_patch_photo_title_status_200(self):
        url = PHOTO_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"title": "patched photo title"})
        assert response.status_code == 200

    def test_patch_photo_title_updated(self):
        url = PHOTO_BY_ID_URL.format(id=1)
        response = requests.patch(url, json={"title": "patched photo title"})
        assert response.json()["title"] == "patched photo title"

    def test_patch_photo_not_found_status_500(self):
        url = PHOTO_BY_ID_URL.format(id=9999999)
        response = requests.patch(url, json={"title": "ghost patch"})
        assert response.status_code == 500


class TestDeletePhoto:

    def test_delete_photo_status_200(self):
        url = PHOTO_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.status_code == 200

    def test_delete_photo_returns_empty_object(self):
        url = PHOTO_BY_ID_URL.format(id=1)
        response = requests.delete(url)
        assert response.json() == {}

    def test_delete_photo_not_found_status_404(self):
        url = PHOTO_BY_ID_URL.format(id=9999999)
        response = requests.delete(url)
        assert response.status_code == 404
