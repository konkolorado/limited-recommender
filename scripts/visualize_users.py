"""
Provides at a glance information of the user dataset
"""

import os
import csv
from collections import Counter

import plot_graph
import file_checks

data_directory = os.path.abspath("../data") + os.sep
source_data = data_directory + "BX-Users-Cleansed.csv"
TOKEN = "unk"


def pull_country_from_location(location):
    return location.split(",")[-1]


def main():
    file_checks.assert_location_exists(data_directory)
    file_checks.assert_file_exists(source_data)

    locations, ages = Counter(), Counter()
    with open(source_data, "r") as src:
        reader = csv.DictReader(src, delimiter=';')

        for row in reader:
            country = pull_country_from_location(row["Location"])

            locations[country] += 1
            if row["Age"] != TOKEN:
                ages[int(row["Age"])] += 1

    plot_graph.plot_top_n(locations, "Nations with most users", "Counts")
    plot_graph.plot_top_n(ages, "User age distribution", "Age [Years]", len(ages))


if __name__ == '__main__':
    main()
