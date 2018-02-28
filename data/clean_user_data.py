"""
Cleans data in the BX-Users, BX-Books, and BX-Book-Ratings datasets.

Removes lines in the dataset that: contain null values, has incomplete
data, has extraneous ages. Rewrites valid lines as utf8 encoded.

Presents the user lines in the dataset that have questionable location
data for validation, rejection, or modification.

Rewrites the data to filenames with  '-Cleansed' appended to the filenames

- TODO leverage csv library
"""

import os
from tempfile import TemporaryFile
from bisect import bisect_left
from difflib import get_close_matches
from collections import Counter

MAX_AGE = 100
MIN_AGE = 10
COUNT_THRESH = 10 # Locations appearing less often than this will be flagged

def clean_users(src_file, tmp_file):
    header = src_file.readline()
    tmp_file.write(header)

    for line in src_file:
        if missing_data(line):
            continue
        if contains_nulls(line):
            continue
        if missing_location_data(line):
            continue
        if get_line_age(line) > MAX_AGE or get_line_age(line) < MIN_AGE:
            continue

        line = process_data(line)
        line.encode("utf8")
        tmp_file.write(line)

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
    of extra quotation chars, and stripped of internal whitespace.
    Returns the new line
    """
    line = lowercase(line)
    line = strip_quotes(line)
    line = strip_whitespace(line)
    return line

def lowercase(line):
    new_line = line.split(';')
    new_line[1] = new_line[1].lower()
    return ';'.join(new_line)

def strip_quotes(line):
    new_line = line.split(';')
    new_line = [info.strip('\"') for info in new_line]
    new_line[-1] = new_line[-1].replace("\"", "")
    return ';'.join(new_line)

def strip_whitespace(line):
    new_line = line.split(';')
    location = new_line[1].split(",")
    location = [data.strip() for data in location]
    new_line[1] = ','.join(location)
    return ';'.join(new_line)

def clean_locations_interactive(tmp_file, dest_file):
    """
    Cleaning the city, state, country data is hard to do without
    human input. Here we collect the number of times the city, state,
    country come up in the dataset and values that come up too scarcely
    are presented to the user for validation or rejection. We assume
    that only country validity matters
    """
    country_counts = collect_country_frequency(tmp_file)
    corpus = countries_above_thresh(country_counts)
    changes, rejections = {}, set()

    dest_file.write(tmp_file.readline()) # Header
    for line in tmp_file:
        line = apply_changes_to_line(changes, line)
        *_, country = extract_city_state_country(line)

        if country_counts[country] >= COUNT_THRESH:
            dest_file.write(line)
        elif country in rejections:
            continue
        else:
            choice = user_menu(country_counts, corpus, country)
            if choice == "A":
                # Do this to remember this entry is ok
                country_counts[country] = COUNT_THRESH
                dest_file.write(line)
            if choice == "M":
                recs = get_recommendations(corpus, country)
                new_country = user_menu_update_country(recs)
                record_changes(changes, country, new_country)
                country_counts[new_country] = COUNT_THRESH
                corpus = countries_above_thresh(country_counts)
                dest_file.write(update_line(line, new_country))
            else:
                rejections.add(country)

def apply_changes_to_line(changes, line):
    *_, country = extract_city_state_country(line)
    if country in changes:
        new_country = changes[country]
        return update_line(line, new_country)
    else:
        return line

def record_changes(all_changes, old, new):
    all_changes[old] = new

def collect_country_frequency(fname):
    """
    Counts the number of times each country appears in the dataset.
    Returns dicts for each.
    """
    country_counts = Counter()
    _ = fname.readline()
    for line in fname:
        *_, country = extract_city_state_country(line)
        country_counts[country] += 1
    fname.seek(0)
    return country_counts

def extract_city_state_country(line):
    return line.split(";")[1].split(",")

def user_menu(country_counts, corpus, country):
    recs = get_recommendations(corpus, country)
    print(f"Country Counts '{country}': {country_counts[country]}")
    while True:
        result = input("Accept? Reject? Modify? See suggestions? [A/R/M/S]: ")
        if result == "S":
            print(f"Recommendations: {build_recs_message(recs)}")
        if result == "A" or result == "R" or result == "M":
            return result

def update_line(line, new_country):
    new_line = line.split(";")
    location_data = new_line[1].split(",")
    location_data[2] = new_country
    new_line[1] = ','.join(location_data)
    new_line = ';'.join(new_line)
    return new_line

def user_menu_update_country(recs):
    """
    Gets user input to update country name while presenting options
    previously encountered in the data..
    Requirements: Name must be greater than 1 char
    Returns the users input. Recs is a list of strings
    """
    message = build_recs_message(recs)
    print(f"Suggestions: {message}")

    while True:
        country = input("New country: ").lower().strip("\" ")
        try:
            choice = int(country) - 1
            if choice > -1 and choice < len(recs):
                country = recs[choice]
            else:
                country = ""
        except ValueError:
            pass
        if len(country) > 1:
            break
    return country

def countries_above_thresh(counts):
    """
    Creates a corpus of countries that have come up more than
    COUNT_THRESH times
    """
    return [k for k,v in counts.items() if v >= COUNT_THRESH]

def get_recommendations(corpus, word, n=3):
    """
    Returns the top n most similar words in a corpus to word.
    Performance shouldnt take a large hit since the program
    spends most of its time waiting for input.
    """
    return get_close_matches(word, corpus, n=n)

def build_recs_message(recs):
    if len(recs) == 0:
        s = "None"
    else:
        s = ''.join(f"{num}. {rec} " for num, rec in enumerate(recs, 1))
    return s

def main():
    sourcefile = "BX-Users.csv"
    destfile = "BX-Users-Cleansed.csv"
    with open(sourcefile, 'r', encoding="iso-8859-1") as srcf, \
      TemporaryFile('w+', encoding="utf8") as tmpf, \
      open(destfile, 'w', encoding="utf8") as destf:
        clean_users(srcf, tmpf)
        tmpf.seek(0)
        clean_locations_interactive(tmpf, destf)

if __name__ == '__main__':
    main()
