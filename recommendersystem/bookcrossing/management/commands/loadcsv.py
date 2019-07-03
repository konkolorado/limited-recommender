from django.core.management.base import BaseCommand, CommandError
from bookcrossing.models import User, Book, Rating

import os
import csv


class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '-users_csv',
            action='store',
            dest='users_csv',
            default=None,
            help="users datafile to preload",
        )
        parser.add_argument(
            '-books_csv',
            action='store',
            dest='books_csv',
            default=None,
            help="books datafile to preload",
        )
        parser.add_argument(
            '-ratings_csv',
            action='store',
            dest='ratings_csv',
            default=None,
            help="ratings datafile to preload",
        )

    def handle(self, *args, **options):
        self.load_csv(options['users_csv'], User)
        self.load_csv(options['books_csv'], Book)
        self.load_csv(options['ratings_csv'], Rating)

    def load_csv(self, csvfile, model):
        if not os.path.isfile(csvfile):
            raise CommandError(f"{csvfile} does not exist")
        with open(csvfile, 'r') as f:
            counter = 0
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                counter += self.commit_to_model(model, row)
        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded {counter} lines of data from {csvfile}'))

    def commit_to_model(self, model, row):
        if model == User:
            _, new = User.objects.get_or_create(user_id=row["User-ID"],
                                                location=row["Location"],
                                                age=row["Age"])
        if model == Book:
            _, new = Book.objects.get_or_create(isbn=row["ISBN"],
                                                title=row["Book-Title"],
                                                author=row["Book-Author"],
                                                publication_yr=row["Year-Of-Publication"],
                                                publisher=row["Publisher"],
                                                image_url_s=row["Image-URL-S"],
                                                image_url_m=row["Image-URL-M"],
                                                image_url_l=row["Image-URL-L"])
        if model == Rating:
            _, new = Rating.objects.get_or_create(
                user_id=User.objects.get(user_id=row["User-ID"]),
                isbn=Book.objects.get(isbn=row["ISBN"]),
                rating=row["Book-Rating"])
        return new
