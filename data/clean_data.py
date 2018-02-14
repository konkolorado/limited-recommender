"""
Cleans data in the BX-Users, BX-Books, and BX-Book-Ratings datasets.

Removes lines in the dataset that: contain null values, has incomplete
data, has extraneous ages. Rewrites valid lines as utf8 encoded.

Rewrites the data to filenames with  '-Cleansed' appended to the filenames

TODO
- make sure i'm lowercasing all Locations
- remove extraneous quote marks from the data
- remove white space from between the location info
"""
import os

from collections import Counter

MAX_AGE = 100
MIN_AGE = 10
COUNT_THRESH = 10 # Locations appearing less often than this will be flagged

def clean_users():
    datafile = "BX-Users.csv"
    destfile = "BX-Users-TempFile.csv"
    with open(datafile, 'r', encoding="iso-8859-1") as srcf, \
            open(destfile, 'w', encoding="utf8") as destf:
        header = srcf.readline()
        destf.write(header)

        for line in srcf:
            if missing_data(line):
                continue
            if contains_nulls(line):
                continue
            if missing_location_data(line):
                continue
            if get_line_age(line) > MAX_AGE or get_line_age(line) < MIN_AGE:
                continue

            #line = process_data(line)
            line.encode("utf8")
            destf.write(line)

def missing_data(line):
    return len(line.split(";")) != 3

def contains_nulls(line):
    return "NULL" in line

def missing_location_data(line):
    location = line.split(";")[1]
    location = location.split(",")
    if len(location) != 3:
        return True
    return any(loc == "" or loc == " " for loc in location)

def get_line_age(line):
    return int(line.strip().split(";")[-1].strip("\""))

def process_data(line):
    """
    Modifies the data in the line to be: all lowercase, stripped
    of extra quotation chars, and stripped of leading and internal
    whitespace. Returns the new line
    """
    line = lowercase(line)
    line = strip_quotes(line)
    line = strip_whitespace(line)
    return line

def lowercase(line):

    #new_line = line.split(";")
    #print(new_line)
    #result = line.split(";")[1].split(",")


def clean_locations_interactive():
    """
    Cleaning the city, state, country data is hard to do without
    human input. Here we collect the number of times the city, state,
    country come up in the dataset and values that come up too scarcely
    are presented to the user for validation or rejection. We assume
    that only country validity matters
    """
    tempfile = "BX-Users-TempFile.csv"
    destfile = "BX-Users-Cleansed.csv"
    country_counts = collect_country_frequency(tempfile)

    with open(tempfile, 'r') as srcf, open(destfile, 'w') as destf:
        header = srcf.readline()
        destf.write(header)

        for line in srcf:
            *_, country = extract_city_state_country(line)
            if country_counts[country] < COUNT_THRESH:
                print(f"Country Counts '{country}': {country_counts[country]}")

                choice = user_menu()
                if choice == "Y":
                    destf.write(line)
                if choice == "M":
                    print(line)
                    line = update_line(line)
                    print(line)
                    destf.write(line)
                else:
                    continue # Reject line
            else:
                destf.write(line)
        remove_tempfile()

def collect_country_frequency(filename):
    """
    Counts the number of times each country appears in the dataset.
    Returns dicts for each.
    """
    country_counts = Counter()
    with open(filename, "r") as f:
        _ = f.readline()
        for line in f:
            *_, country = extract_city_state_country(line)
            country_counts[country] += 1
    return country_counts

def extract_city_state_country(line):
    result = line.split(";")[1].split(",")
    return [loc.lower().strip(" \"") for loc in result]

def user_menu():
    while True:
        result = input("Accept? Reject? Modify? [Y/R/M]: ")
        if result == "Y" or result == "R" or result == "M":
            return result

def update_line(line):
    country = input("New country: ")
    line = update_country_in_line(country, line)
    return line

def update_country_in_line(new_country, line):
    new_line = line.split(";")
    location_data = new_line[1].split(",")
    location_data[2] = new_country
    new_line[1] = ','.join(location_data)
    new_line = ';'.join(new_line)
    return new_line

def remove_tempfile():
    os.remove("BX-Users-TempFile.csv")

def main():
    clean_users()
    clean_locations_interactive()

if __name__ == '__main__':
    main()
