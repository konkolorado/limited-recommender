"""
Cleans data in the BX-Book dataset

This script removes lines that contain null values and rewrites
lines in UTF-8 encoding.
"""

import os
import sys
import csv

import file_checks
import user_interaction

data_directory = os.path.abspath("../data") + os.sep
book_dataset = data_directory + "BX-Books.csv"
processed_data = data_directory + "BX-Books-Cleansed.csv"

NO_NULLS = True  # Each field must contain something

def clean_books(src_file, dest_file):
    with open(src_file, 'r', encoding='iso-8859-1') as src, \
         open(dest_file, 'w', encoding='utf8') as dest:
        reader = csv.DictReader(src, delimiter=';')
        writer = csv.DictWriter(dest, reader.fieldnames, delimiter=';')

        writer.writeheader()
        for row in reader:
            if NO_NULLS and all(row):
                writer.writerow(row)
            elif not NO_NULLS:
                writer.writerow(row)

def do_file_checks(datadir, bookdata, procdata):
    file_checks.assert_location_exists(datadir)
    file_checks.assert_file_exists(bookdata)
    try:
        file_checks.assert_file_not_exists(procdata)
    except AssertionError:
        message = f"File {processed_data} already exists. If you proceed it " \
        "will be overwritten. Continue anyways?"
        response = user_interaction.force_user_input(["Y", "n"], message)
        if response == "n":
            sys.exit()

def main():
    do_file_checks(data_directory, book_dataset, processed_data)

    clean_books(book_dataset, processed_data)

if __name__ == '__main__':
    main()
