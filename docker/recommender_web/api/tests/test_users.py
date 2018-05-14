from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from bookcrossing.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.new_user = {
            "user_id": "0",
            "location": "usa",
            "age": "25"
        }

    def test_can_create_new_user(self):
        old_count = User.objects.count()
        User(**self.new_user).save()
        new_count = User.objects.count()
        self.assertEqual(old_count + 1, new_count)


class UserViewTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.new_user = {
            "user_id": "0",
            "location": "usa",
            "age": "25"
        }

    def test_api_can_create_user(self):
        self.response = self.client.post(
            reverse('create_user'), self.new_user, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_cannot_create_duplicate_user(self):
        self.client.post(reverse('create_user'), self.new_user, format="json")
        self.response = self.client.post(reverse('create_user'),
                                         self.new_user, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_api_cannot_create_user_with_invalid_field_len(self):
        self.new_user["user_id"] = "0" * 21
        self.response = self.client.post(reverse('create_user'),
                                         self.new_user, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)
