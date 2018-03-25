"""
Provides at a glance information of the user dataset
"""

import os
import matplotlib.pyplot as plt
from collections import Counter

data_directory = os.path.abspath("../data") + os.sep
source_data = data_directory + "BX-Users-Cleansed.csv"

def plot_locations(counter):
    counts, locs = zip(*sorted(zip(counter.values(), counter.keys())))
    plt.title("Counts for the 35 most recurring nations")
    plt.xlabel("Counts")
    plt.scatter(counts[-35:], locs[-35:])
    plt.show()

def plot_ages(counter):
    ages, counts = zip(*sorted(zip(counter.keys(), counter.values())))
    plt.title("User age frequencies")
    plt.xlabel("Age")
    plt.scatter(ages, counts)
    plt.show()

def main():
    locations, ages = Counter(), Counter()
    with open(source_data, "r") as userfile:
        _ = userfile.readline()
        for line in userfile:
            line = line.strip().split(";")[1:]
            age = int(line[-1].strip("\""))
            country = line[0].strip("\" ").split(",")[-1]
            locations[country] += 1
            ages[age] += 1

    plot_locations(locations)
    plot_ages(ages)

if __name__ == '__main__':
    main()
