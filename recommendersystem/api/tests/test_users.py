from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

import json

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


class UserViewPostTestCase(TestCase):
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
            reverse('api-user-list'), self.new_user, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_cannot_create_duplicate_user(self):
        self.client.post(reverse('api-user-list'), self.new_user, format="json")
        self.response = self.client.post(reverse('api-user-list'),
                                         self.new_user, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_api_cannot_create_user_with_invalid_field_len(self):
        self.new_user["user_id"] = "0" * 21
        self.response = self.client.post(reverse('api-user-list'),
                                         self.new_user, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)


class UserViewGetTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.new_user = {
            "id": 1,
            "user_id": "0",
            "location": "usa",
            "age": "25"
        }
        User(**self.new_user).save()

    def test_api_can_get_user(self):
        user = User.objects.get()
        response = self.client.get(
            reverse('api-user-detail',
                    kwargs={'pk': user.pk}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.new_user)

    def test_api_cannot_get_fake_user(self):
        response = self.client.get(
            reverse('api-user-detail',
                    kwargs={'pk': -1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserViewPutTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.new_user = {
            "id": "1",
            "user_id": "0",
            "location": "usa",
            "age": "25"
        }
        User(**self.new_user).save()

    def test_api_can_update_user(self):
        self.new_user["location"] = "blah"
        response = self.client.put(
            reverse('api-user-detail', kwargs={'pk':
                                           self.new_user["id"]}),
            self.new_user, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_cannot_update_fake_user(self):
        self.new_user["age"] = 0
        response = self.client.put(
            reverse('api-user-detail', kwargs={'pk':
                                           self.new_user["id"] * 50}),
            self.new_user, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_cannot_update_user_with_bad_data(self):
        self.new_user["age"] = 1000
        response = self.client.put(
            reverse('api-user-detail', kwargs={'pk':
                                           self.new_user["id"]}),
            self.new_user, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserViewDeleteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.new_user = {
            "id": "1",
            "user_id": "0",
            "location": "usa",
            "age": "25"
        }
        User(**self.new_user).save()

    def test_api_can_delete_user(self):
        response = self.client.delete(
            reverse("api-user-detail", kwargs={'pk':
                                           self.new_user["id"]}),
            format='json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_cannot_delete_fake_user(self):
        response = self.client.delete(
            reverse('api-user-detail', kwargs={'pk':
                                           self.new_user["id"] * 50}),
            format='json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
