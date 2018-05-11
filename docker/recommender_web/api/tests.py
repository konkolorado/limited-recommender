from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from bookcrossing.models import Book


class BookTestCase(TestCase):
    def setUp(self):
        self.new_book = {
            "isbn": "0",
            "title": "0",
            "author": "0",
            "publication_yr": "0",
            "publisher": "0",
            "image_url_s": "0",
            "image_url_m": "0",
            "image_url_l": "0",
        }

    def test_can_create_new_book(self):
        old_count = Book.objects.count()
        Book(**self.new_book).save()
        new_count = Book.objects.count()
        self.assertEqual(old_count + 1, new_count)


class ViewTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.new_book = {
            "isbn": "0",
            "title": "0",
            "author": "0",
            "publication_yr": "0",
            "publisher": "0",
            "image_url_s": "http://www.google.com",
            "image_url_m": "http://www.google.com",
            "image_url_l": "http://www.google.com",
        }
        self.response = self.client.post(
            reverse('create'), self.new_book, format="json")

    def test_api_can_create_book(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
