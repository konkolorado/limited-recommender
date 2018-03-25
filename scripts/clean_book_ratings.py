"""
Cleans data in the BX-Books-Ratings dataset

This should run after the BX-Users dataset has been cleaned

This script removes ratings from users that no longer exist in the
BX-Users dataset.  Those users may have been removed because their
data was clearly bogus and or incomplete.

This script removes lines that contain null values.  The script also
rewrites lines as UTF-8 encoding.
"""

import os
import sys
import csv

import file_checks
import user_interaction

data_directory = os.path.abspath("../data") + os.sep
users_dataset = data_directory + "BX-Users-Cleansed.csv"
ratings_data = data_directory + "BX-Book-Ratings.csv"
processed_data = data_directory + "BX-Book-Ratings-Cleansed.csv"


def do_file_checks(datadir, usersdata, ratingsdata, procdata):
    file_checks.assert_location_exists(datadir)
    file_checks.assert_file_exists(usersdata)
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
    do_file_checks(data_directory, users_dataset, ratings_data, processed_data)

if __name__ == '__main__':
    main()
