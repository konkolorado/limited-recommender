from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

import json

from bookcrossing.models import Book


class BookTestCase(TestCase):
    def setUp(self):
        self.book = {
            "isbn": "0",
            "title": "0",
            "author": "0",
            "publication_yr": "0",
            "publisher": "0",
            "image_url_s": "http://www.google.com",
            "image_url_m": "http://www.google.com",
            "image_url_l": "http://www.google.com",
        }

    def test_can_create_new_book(self):
        old_count = Book.objects.count()
        Book(**self.book).save()
        new_count = Book.objects.count()
        self.assertEqual(old_count + 1, new_count)


class BookViewPostTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.book = {
            "isbn": "0",
            "title": "0",
            "author": "0",
            "publication_yr": "0",
            "publisher": "0",
            "image_url_s": "http://www.google.com",
            "image_url_m": "http://www.google.com",
            "image_url_l": "http://www.google.com",
        }

    def test_api_can_create_book(self):
        response = self.client.post(
            reverse('book-create'), self.book, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_cannot_create_duplicate_book(self):
        self.client.post(reverse('book-create'), self.book, format="json")
        response = self.client.post(reverse('book-create'),
                                    self.book, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_api_cannot_create_book_with_invalid_url(self):
        self.book["image_url_s"] = "nonsense_url"
        response = self.client.post(reverse('book-create'),
                                    self.book, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_api_cannot_create_book_with_invalid_field_len(self):
        self.book["isbn"] = "0" * 21
        response = self.client.post(reverse('book-create'),
                                    self.book, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)


class BookViewGetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = {
            "id": 1,
            "isbn": "0",
            "title": "0",
            "author": "0",
            "publication_yr": "0",
            "publisher": "0",
            "image_url_s": "http://www.google.com",
            "image_url_m": "http://www.google.com",
            "image_url_l": "http://www.google.com",
        }
        Book(**self.book).save()

    def test_api_can_get_book(self):
        book = Book.objects.get()
        response = self.client.get(
            reverse('book-detail',
                    kwargs={'pk': book.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.book)

    def test_api_cannot_get_fake_book(self):
        response = self.client.get(
            reverse('book-detail',
                    kwargs={'pk': -1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookViewPutTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = {
            "id": "1",
            "isbn": "0",
            "title": "0",
            "author": "0",
            "publication_yr": "0",
            "publisher": "0",
            "image_url_s": "http://www.google.com",
            "image_url_m": "http://www.google.com",
            "image_url_l": "http://www.google.com",
        }
        Book(**self.book).save()

    def test_api_can_update_book(self):
        self.book["title"] = -1
        response = self.client.put(
            reverse('book-detail', kwargs={'pk': self.book["id"]}),
            self.book, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_cannot_update_fake_book(self):
        self.book["title"] = -1
        response = self.client.put(
            reverse('book-detail', kwargs={'pk': self.book["id"] * 50}),
            self.book, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_cannot_update_book_with_bad_data(self):
        self.book["image_url_s"] = "0"
        response = self.client.put(
            reverse('book-detail', kwargs={'pk': self.book["id"]}),
            self.book, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookViewDeleteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = {
            "id": "1",
            "isbn": "0",
            "title": "0",
            "author": "0",
            "publication_yr": "0",
            "publisher": "0",
            "image_url_s": "http://www.google.com",
            "image_url_m": "http://www.google.com",
            "image_url_l": "http://www.google.com",
        }
        Book(**self.book).save()

    def test_api_can_delete_book(self):
        response = self.client.delete(
            reverse('book-detail', kwargs={'pk': self.book["id"]}),
            format='json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_cannot_delete_fake_book(self):
        response = self.client.delete(
            reverse('book-detail', kwargs={'pk': self.book["id"] * 50}),
            format='json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
