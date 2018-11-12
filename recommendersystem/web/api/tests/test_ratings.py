from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from bookcrossing.models import Rating, User, Book


class RatingTestCase(TestCase):
    def setUp(self):
        self.create_demo_user_and_book()
        self.new_rating = {
            "user_id": User.objects.get(user_id="0"),
            "isbn": Book.objects.get(isbn="0"),
            "rating": "5"
        }

    def create_demo_user_and_book(self):
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
        self.new_user = {
            "user_id": "0",
            "location": "usa",
            "age": "25"
        }
        Book(**self.new_book).save()
        User(**self.new_user).save()

    def test_can_create_new_rating(self):
        old_count = Rating.objects.count()
        Rating(**self.new_rating).save()
        new_count = Rating.objects.count()
        self.assertEqual(old_count + 1, new_count)


class RatingViewPostTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.create_demo_user_and_book()
        self.new_rating = {
            "user_id": "0",
            "isbn": "0",
            "rating": "5"
        }

    def create_demo_user_and_book(self):
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
        self.new_user = {
            "user_id": "0",
            "location": "usa",
            "age": "25"
        }
        Book(**self.new_book).save()
        User(**self.new_user).save()

    def test_api_can_create_rating(self):
        self.response = self.client.post(
            reverse('api-rating-create'), self.new_rating, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_cannot_create_duplicate_rating(self):
        self.client.post(reverse('api-rating-create'), self.new_rating,
                         format="json")
        self.response = self.client.post(reverse('api-rating-create'),
                                         self.new_rating, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_api_cannot_create_rating_with_invalid_user_id(self):
        self.new_rating["user_id"] = "1"
        self.response = self.client.post(reverse('api-rating-create'),
                                         self.new_rating, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_api_cannot_create_rating_with_invalid_isbn(self):
        self.new_rating["isbn"] = "1"
        self.response = self.client.post(reverse('api-rating-create'),
                                         self.new_rating, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_api_cannot_create_rating_with_negative_rating(self):
        self.new_rating["rating"] = "-1"
        self.response = self.client.post(reverse('api-rating-create'),
                                         self.new_rating, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_api_cannot_create_rating_with_rating_over_ten(self):
        self.new_rating["rating"] = "11"
        self.response = self.client.post(reverse('api-rating-create'),
                                         self.new_rating, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)


class RatingViewGetTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.create_demo_user_book_rating()

    def create_demo_user_book_rating(self):
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
        self.new_user = {
            "user_id": "0",
            "location": "usa",
            "age": "25"
        }
        Book(**self.new_book).save()
        User(**self.new_user).save()
        self.new_rating = {
            "user_id": User.objects.get(user_id="0"),
            "isbn": Book.objects.get(isbn="0"),
            "rating": "5"
        }
        Rating(**self.new_rating).save()

    def test_api_can_get_rating_by_user_id(self):
        self.response = self.client.get(reverse('api-rating-create'),
                                        {'user_id': '0'})
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data["results"]), 1)

    def test_api_can_get_rating_by_isbn(self):
        self.response = self.client.get(reverse('api-rating-create'),
                                        {'isbn': '0'})
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data["results"]), 1)

    def test_api_can_get_rating_by_rating(self):
        self.response = self.client.get(reverse('api-rating-create'),
                                        {'rating': '5'})
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data["results"]), 1)

    def test_api_can_get_rating_by_isbn_and_user_id_and_rating(self):
        self.response = self.client.get(reverse('api-rating-create'),
                                        {'isbn': '0', 'user_id': '0',
                                         'rating': '5'})
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data["results"]), 1)

    def test_api_cannot_get_fake_rating_by_user_id(self):
        self.response = self.client.get(reverse('api-rating-create'),
                                        {'user_id': '-1'})
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(len(self.response.data["results"]), 0)

    def test_api_cannot_get_fake_rating_by_isbn(self):
        self.response = self.client.get(reverse('api-rating-create'),
                                        {'isbn': '-1'})
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(len(self.response.data["results"]), 0)

    def test_api_cannot_get_fake_rating_by_rating(self):
        self.response = self.client.get(reverse('api-rating-create'),
                                        {'rating': '1'})
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(len(self.response.data["results"]), 0)


class RatingViewPutTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.create_demo_user_book_rating()

    def create_demo_user_book_rating(self):
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
        self.new_user = {
            "user_id": "0",
            "location": "usa",
            "age": "25"
        }
        Book(**self.new_book).save()
        User(**self.new_user).save()
        self.new_rating = {
            "id": 1,
            "user_id": User.objects.get(user_id="0"),
            "isbn": Book.objects.get(isbn="0"),
            "rating": "5"
        }
        Rating(**self.new_rating).save()

    def test_api_can_update_rating(self):
        response = self.client.put(
            reverse('api-rating-detail', kwargs={'pk':
                                             self.new_rating["id"]
                                             }),
            {
                "rating": "9",
                "user_id": self.new_user["user_id"],
                "isbn": self.new_book["isbn"]
            }, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_cannot_update_fake_rating(self):
        response = self.client.put(
            reverse('api-rating-detail', kwargs={'pk':
                                             self.new_rating["id"] * 50
                                             }),
            {
                "rating": "9",
                "user_id": self.new_user["user_id"],
                "isbn": self.new_book["isbn"]
            }, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_cannot_update_rating_with_bad_data(self):
        response = self.client.put(
            reverse('api-rating-detail', kwargs={'pk':
                                             self.new_rating["id"]}),
            {"rating": 11}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RatingViewDeleteTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.create_demo_user_book_rating()

    def create_demo_user_book_rating(self):
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
        self.new_user = {
            "user_id": "0",
            "location": "usa",
            "age": "25"
        }
        Book(**self.new_book).save()
        User(**self.new_user).save()
        self.new_rating = {
            "id": 1,
            "user_id": User.objects.get(user_id="0"),
            "isbn": Book.objects.get(isbn="0"),
            "rating": "5"
        }
        Rating(**self.new_rating).save()

    def test_api_can_delete_rating(self):
        response = self.client.delete(
            reverse('api-rating-detail', kwargs={'pk': self.new_rating["id"]}),
            format='json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_cannot_delete_fake_rating(self):
        response = self.client.delete(
            reverse('api-rating-detail', kwargs={'pk': self.new_rating["id"]*50}),
            format='json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
