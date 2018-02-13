"""
Performs a k-means clustering to cluster users. Omits users with null
values
"""

import matplotlib.pyplot as plt
import csv
from collections import Counter

locations = Counter()
ages = Counter()

def plot(counter):
    ages, counts = zip(*sorted(zip(counter.keys(), counter.values())))
    plt.scatter(ages, counts)
    plt.show()

with open("BX-Users.csv", "r", encoding="iso-8859-1") as userfile:
    _ = userfile.readline()
    for line in userfile:
        line.encode('utf8')

        line = line.strip().split(";")[1:]
        if len(line) < 2 or line[-1] == "NULL":
            continue

        age = int(line[-1].strip("\""))
        if age > 70:
            print(line)
        country = line[0].strip("\" ").split(",")[-1]
        locations[country] += 1
        ages[age] += 1

#print(locations)
#print(ages)
#plot(locations)
plot(ages)
