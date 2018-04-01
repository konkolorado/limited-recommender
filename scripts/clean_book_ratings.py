"""
Cleans data in the BX-Books-Ratings dataset

This should run after the BX-Users and the BX-Books datasets have
been cleaned.

This script removes ratings from users that no longer exist in the
BX-Users dataset and removes ratings for books that no longer exist
in the BX-Books dataset.  Those users/books may have been removed
because their data was clearly bogus and or incomplete.

This script also removes lines that contain null values and rewrites
lines in UTF-8 encoding.
"""

import os
import sys
import csv
from bisect import bisect_left

import file_checks
import user_interaction

data_directory = os.path.abspath("../data") + os.sep
users_dataset = data_directory + "BX-Users-Cleansed.csv"
books_dataset = data_directory + "BX-Books-Cleansed.csv"
ratings_dataset = data_directory + "BX-Book-Ratings.csv"
processed_data = data_directory + "BX-Book-Ratings-Cleansed.csv"

def collect_user_ids(src_file):
    """
    Stores User ids in a list. Takes advantage of the fact that Users
    are listed in increasing ID order
    """
    ids = []
    with open(src_file, 'r', encoding="iso-8859-1") as src:
        reader = csv.DictReader(src, delimiter=';')
        for row in reader:
            ids.append(int(row["User-ID"]))

    assert sorted(ids) == ids, "User ids are out of order"
    return ids

def collect_book_isbns(src_file):
    """
    Stores and returns ISBNs in a set
    """
    isbns = set()
    with open(src_file, 'r', encoding="iso-8859-1") as src:
        reader = csv.DictReader(src, delimiter=";")
        for row in reader:
            isbns.add(row["ISBN"])
    return isbns

def keep_valid_ratings(ratings_file, proc_file, ids, isbns):
    with open(ratings_file, 'r', encoding="iso-8859-1") as ratings, \
         open(proc_file, 'w', encoding="utf8") as dest:
        reader = csv.DictReader(ratings, delimiter=';')
        writer = csv.DictWriter(dest, reader.fieldnames, delimiter=";",
            quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for row in reader:
            if "NULL" in row:
                continue
            elif valid_id(ids, int(row["User-ID"])) and \
               valid_isbn(isbns, row["ISBN"]):
                    writer.writerow(row)

def valid_id(ids, curr_id):
    i  = bisect_left(ids, curr_id)
    if ids[i] == curr_id:
        return True
    else:
        return False

def valid_isbn(isbns, curr_isbn):
    return curr_isbn in isbns

def do_file_checks(datadir, usersdata, booksdata, ratingsdata, procdata):
    file_checks.assert_location_exists(datadir)
    file_checks.assert_file_exists(usersdata)
    file_checks.assert_file_exists(booksdata)
    file_checks.assert_file_exists(ratingsdata)
    try:
        file_checks.assert_file_not_exists(procdata)
    except AssertionError:
        message = f"File {processed_data} already exists. If you proceed it " \
        "will be overwritten. Continue anyways?"
        response = user_interaction.force_user_input(["Y", "n"], message)
        if response == "n":
            sys.exit()

def main():
    do_file_checks(data_directory, users_dataset, books_dataset,
                   ratings_dataset, processed_data)

    user_ids = collect_user_ids(users_dataset)
    book_isbns = collect_book_isbns(books_dataset)
    keep_valid_ratings(ratings_dataset, processed_data, user_ids, book_isbns)

if __name__ == '__main__':
    main()
