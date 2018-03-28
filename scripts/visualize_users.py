"""
Provides at a glance information of the user dataset
"""

import os
from collections import Counter

import plot_graph
import file_checks

data_directory = os.path.abspath("../data") + os.sep
source_data = data_directory + "BX-Users-Cleansed.csv"
TOKEN = "unk"

def main():
    file_checks.assert_location_exists(data_directory)
    file_checks.assert_file_exists(source_data)

    locations, ages = Counter(), Counter()
    with open(source_data, "r") as userfile:
        _ = userfile.readline()
        for line in userfile:
            line = line.strip().split(";")[1:]
            try:
                age = int(line[-1].strip("\""))
            except ValueError:
                continue
            country = line[0].strip("\" ").split(",")[-1]
            locations[country] += 1
            ages[age] += 1

    plot_graph.plot_top_n(locations, "Nations with most users", "Counts")
    plot_graph.plot_top_n(ages, "User age distribution", "Age [Years]", len(ages))

if __name__ == '__main__':
    main()
