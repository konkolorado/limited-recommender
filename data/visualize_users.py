"""
Provides at a glance information of the user dataset
"""

import matplotlib.pyplot as plt
from collections import Counter

DEFAULT_DATA_DIR = "data/"
RAW_DATA = "BX-Users-Cleansed.csv"

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
    with open(RAW_DATA, "r") as userfile:
        _ = userfile.readline()
        for line in userfile:
            line.encode('utf8')

            line = line.strip().split(";")[1:]
            if len(line) < 2 or line[-1] == "NULL":
                continue

            age = int(line[-1].strip("\""))
            country = line[0].strip("\" ").split(",")[-1]
            locations[country] += 1
            ages[age] += 1

    plot_locations(locations)
    plot_ages(ages)

if __name__ == '__main__':
    main()
