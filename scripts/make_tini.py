"""
Takes a dataset and makes tini versions of it.

First we choose n samples randomly from the ratings dataset.  From this sample,
we extract user / book identifiers and use them to filter the user / book
datasets to only included these values
"""

import os
import csv
import random

import file_checks

data_directory = os.path.abspath("../data") + os.sep
book_dataset = data_directory + "BX-Books-Cleansed.csv"
book_dataset_out = data_directory + "BX-Books-Cleansed-Tini.csv"

users_dataset = data_directory + "BX-Users-Cleansed.csv"
users_dataset_out = data_directory + "BX-Users-Cleansed-Tini.csv"

ratings_dataset = data_directory + "BX-Book-Ratings-Cleansed.csv"
ratings_dataset_out = data_directory + "BX-Book-Ratings-Cleansed-Tini.csv"


class BXDatasetTini(object):
    def __init__(self, books, users, ratings):
        self.books = books
        self.users = users
        self.ratings = ratings

        self.user_ids, self.book_isbns = set(), set()

        file_checks.assert_file_exists(self.books)
        file_checks.assert_file_exists(self.users)
        file_checks.assert_file_exists(self.ratings)

    def make_tini_books(self, out_fname, n):
        with open(self.books) as src, open(out_fname, 'w') as dst:
            reader = csv.DictReader(src, delimiter=';')
            writer = csv.DictWriter(dst, reader.fieldnames, delimiter=';',
                quoting=csv.QUOTE_ALL)

            writer.writeheader()
            for i, line in enumerate(reader):
                if line["ISBN"] in self.book_isbns:
                    writer.writerow(line)

    def _add_isbn_to_book_isbns(self, line):
        self.book_isbns.add(line["ISBN"])

    def make_tini_users(self, out_fname, n):
        with open(self.users) as src, open(out_fname, 'w') as dst:
            reader = csv.DictReader(src, delimiter=';')
            writer = csv.DictWriter(dst, reader.fieldnames, delimiter=';',
                quoting=csv.QUOTE_ALL)

            writer.writeheader()
            for i, line in enumerate(reader):
                if line["User-ID"] in self.user_ids:
                    writer.writerow(line)

    def _add_id_to_user_ids(self, line):
        self.user_ids.add(line["User-ID"])

    def make_tini_ratings(self, out_fname, n):
        """
        Randomly chooses n ratings from the ratings data provided in
        self.ratings. Saves the datalines in out_fname
        """
        f_len = self._get_file_length(self.ratings)
        lines = self._sample(0, f_len, n)

        with open(self.ratings) as src, open(out_fname, 'w') as dst:
            reader = csv.DictReader(src, delimiter=';')
            writer = csv.DictWriter(dst, reader.fieldnames, delimiter=';',
                quoting=csv.QUOTE_ALL)

            writer.writeheader()
            for i, line in enumerate(reader):
                if len(lines) > 0 and i == lines[0]:
                    self._add_id_to_user_ids(line)
                    self._add_isbn_to_book_isbns(line)
                    writer.writerow(line)
                    lines.pop(0)

    def _get_file_length(self, fname):
        with open(fname, 'r') as f:
            n_lines = sum(1 for line in f)
        return n_lines - 1 # Remove header line

    def _sample(self, low, high, n):
        """
        Given a low int and a high int, randomly selects n integers
        """
        return sorted(random.sample(range(low, high), n))

def main():
    tini = BXDatasetTini(book_dataset, users_dataset, ratings_dataset)

    tini.make_tini_ratings(ratings_dataset_out, 10)
    tini.make_tini_books(book_dataset_out, 10)
    tini.make_tini_users(users_dataset_out, 10)

if __name__ == '__main__':
    main()
