"""
Provides at a glance information about the books dataset

In particular, shows which books received the most ratings and
which users rated the most
"""

import os
import csv
from collections import Counter

import plot_graph
import file_checks

data_directory = os.path.abspath("../data") + os.sep
source_data = data_directory + "BX-Book-Ratings-Cleansed.csv"
TOKEN = "unk"


def main():
    file_checks.assert_location_exists(data_directory)
    file_checks.assert_file_exists(source_data)

    count_book_ratings, count_user_ratings = Counter(), Counter()
    with open(source_data, 'r') as src:
        reader = csv.DictReader(src, delimiter=';')

        for row in reader:
            count_book_ratings[row["ISBN"]] += 1
            count_user_ratings[row["User-ID"]] += 1

    plot_graph.plot_top_n(count_book_ratings, "Top books with most ratings",
                          "ISBNS")
    plot_graph.plot_top_n(count_user_ratings, "Top users who rated",
                          "User ID")


if __name__ == "__main__":
    main()
