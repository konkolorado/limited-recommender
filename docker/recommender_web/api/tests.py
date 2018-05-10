from django.test import TestCase


from bookcrossing.models import Book, User, Rating
# Create your tests here.

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
