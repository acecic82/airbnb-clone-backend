from django.test import TestCase
from rest_framework.test import APITestCase

from users.models import User
from . import models

# Create your tests here.


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Description"
    URL = "/api/v1/rooms/amenities"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        print("-------------test_all_amenitiest---------------")

        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status Code isn't 200.")

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_create_amenity(self):
        newAmenityName = "New Amenity"
        newAmenityDesc = "New Amenity desc."

        response = self.client.post(
            self.URL,
            data={
                "name": newAmenityName,
                "description": newAmenityDesc,
            },
        )

        self.assertEqual(response.status_code, 200, "Not 200 status code")

        data = response.json()

        self.assertEqual(
            data["name"],
            newAmenityName,
        )

        self.assertEqual(
            data["description"],
            newAmenityDesc,
        )

        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)


class TestAmenity(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Description"
    URL = "/api/v1/rooms/amenities"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):

        response = self.client.get(
            f"{self.URL}/2",
        )

        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):

        response = self.client.get(
            f"{self.URL}/1",
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["name"],
            self.NAME,
        )

        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_amenity_delete(self):

        response = self.client.delete(
            f"{self.URL}/1",
        )

        self.assertEqual(response.status_code, 204)


class TestRoom(APITestCase):

    URL = "/api/v1/rooms"

    def setUp(self):
        user = User.objects.create(username="test")

        user.set_password("123")
        user.save()

        self.user = user

    def test_create_room(self):

        response = self.client.post(f"{self.URL}/")

        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.user)

        response = self.client.post(f"{self.URL}/")

        self.assertEqual(response.status_code, 400)
