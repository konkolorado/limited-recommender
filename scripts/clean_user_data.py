"""
Cleans data in the BX-Users dataset.

Removes lines in the dataset that: contain null values, has incomplete
data, has extraneous ages. Rewrites valid lines as utf8 encoded.

Presents the user lines in the dataset that have questionable location
data for validation, rejection, or modification.

Rewrites the data to a new file

- TODO leverage csv library
"""

import os
import csv

from tempfile import TemporaryFile
from bisect import bisect_left
from difflib import get_close_matches
from collections import Counter

import user_interaction
import file_checks

data_directory = os.path.abspath("../data") + os.sep
source_data = data_directory + "BX-Users.csv"
processed_data = data_directory + "BX-Users-Cleansed.csv"

MAX_AGE = 100
MIN_AGE = 10
MAX_COUNT_THRESH = 10000  # Locations appearing more than this are auto accepted
MIN_COUNT_THRESH = 1  # Locations appearing less than this are auto rejected
DROP_UNK = False      # Drop empty/null data or replace with a token
TOKEN = "unk"


def clean_users(src_stream, tmp_stream):
    reader = csv.DictReader(src_stream, delimiter=';')
    writer = csv.DictWriter(tmp_stream, reader.fieldnames, delimiter=";",
                            quoting=csv.QUOTE_ALL)
    writer.writeheader()

    for row in reader:
        if missing_data(row):
            continue
        if missing_age(row):
            if DROP_UNK:
                continue
            update_row_age(row, TOKEN)
        if missing_country_data(row):
            if DROP_UNK:
                continue
            update_row_country(row, TOKEN)
        if get_row_age(row) > MAX_AGE or get_row_age(row) < MIN_AGE:
            continue

        process_data(row)
        writer.writerow(row)


def missing_data(row):
    return len(row) != 3


def missing_age(row):
    return row["Age"] in ["NULL", ""]


def update_row_age(row, symbol):
    row["Age"] = symbol


def missing_country_data(row):
    location = row["Location"]
    country = extract_country_from_location(location)
    if country.strip() in ["", " ", "n/a", "NULL"]:
        return True


def extract_country_from_location(location):
    country = location.split(',')[-1]
    country = country.replace('"', '')
    return country


def get_row_age(row):
    age = row["Age"]
    if age == TOKEN:
        return MAX_AGE - 1
    return int(age)


def process_data(row):
    """
    Modifies the data in the line to be: all lowercase
    and stripped of internal whitespace.
    """
    lowercase(row)
    strip_whitespace(row)


def lowercase(row):
    row["Location"] = row["Location"].lower()


def strip_whitespace(row):
    location = row["Location"].split(",")
    stripped = [l.strip() for l in location]
    row["Location"] = ','.join(stripped)


def clean_locations(tmp_stream, dest_stream):
    """
    Cleaning the city, state, country data is hard to do without
    human input. Here we collect the number of times the city, state,
    country come up in the dataset and values that come up too scarcely
    are presented to the user for validation or rejection. We assume
    that only country validity matters
    """
    reader = csv.DictReader(tmp_stream, delimiter=';')
    writer = csv.DictWriter(dest_stream, reader.fieldnames, delimiter=";",
                            quoting=csv.QUOTE_ALL)
    writer.writeheader()

    country_counts = get_country_counts(tmp_stream, reader)
    accepted_countries = get_countries_above_max_threshold(country_counts)
    rejected_countries = get_countries_below_min_threshold(country_counts)
    changes = {}

    tmp_stream.readline()  # Gets DictReader to skip headerline
    for row in reader:
        apply_user_changes_to_line(changes, row)
        country = extract_country_from_location(row["Location"])

        if country in accepted_countries:
            writer.writerow(row)
        elif country in rejected_countries:
            if not DROP_UNK:
                update_changes(changes, country, TOKEN)
                update_row_country(row, TOKEN)
                writer.writerow(row)
        else:
            recs = get_recommendations(accepted_countries, country)
            response = ask_user(country_counts, country, recs)
            if response == "R":
                rejected_countries.add(country)
                update_row_country(row, TOKEN)
            if response == "A":
                accepted_countries.add(country)
            if response == "M":
                new_country = get_new_country_from_user(recs)
                update_changes(changes, country, new_country)
                accepted_countries.add(new_country)
                update_row_country(row, new_country)
            if response in ["A", "M"] or not DROP_UNK:
                writer.writerow(row)


def get_country_counts(stream, csv_reader):
    """
    Records the number of times each country appears in the dataset
    """
    country_counts = Counter()
    for row in csv_reader:
        country = extract_country_from_location(row["Location"])
        country_counts[country] += 1

    reset_stream(stream)
    return country_counts


def reset_stream(stream):
    stream.seek(0)


def get_countries_above_max_threshold(counts):
    """
    Creates a set of countries that have come up more than
    MAX_COUNT_THRESH times
    """
    return set(k for k, v in counts.items() if v >= MAX_COUNT_THRESH)


def get_countries_below_min_threshold(counts):
    """
    Creates a set of countries that have come up less than
    MIN_COUNT_THRESH times. This signals they are automatically rejected
    """
    return set(k for k, v in counts.items() if v <= MIN_COUNT_THRESH)


def apply_user_changes_to_line(changes, row):
    country = extract_country_from_location(row["Location"])
    if country in changes:
        new_country = changes[country]
        update_row_country(row, new_country)


def update_row_country(row, new_country):
    location = row["Location"].split(",")
    location[-1] = new_country
    row["Location"] = ','.join(location)


def get_recommendations(corpus, word, n=3):
    """
    Returns the top n most similar words in a corpus to word.
    """
    return get_close_matches(word, corpus, n=n)


def ask_user(country_counts, country, suggestions):
    message = "Accept? Reject? Modify? See suggestions?"
    recs_message = build_recs_message(suggestions)

    print(f"Country Counts '{country}': {country_counts[country]}")
    response = user_interaction.force_user_input(["A", "R", "M", "S"],
                                                 message)
    while response == "S":
        response = user_interaction.force_user_input(["A", "R", "M", "S"],
                                                     recs_message)
    return response


def build_recs_message(recs):
    if len(recs) == 0:
        s = "Suggestions: None"
    else:
        s = ''.join(f"{num}. {rec} " for num, rec in enumerate(recs, 1))
        s = "Suggestions: " + s
    return s


def get_new_country_from_user(suggestions):
    """
    Gets user input to update country while presenting valid options seen
    in the data.
    Requirements: Updated country name must be greater than 1 char
    Params:
        suggestions: a list of possible country
    Returns a new country name
    """
    recs_message = build_recs_message(suggestions)
    print(f"{recs_message}")

    while True:
        country = input("New country: ").lower().strip("\" ")
        try:
            choice = int(country) - 1
            if choice > -1 and choice < len(suggestions):
                country = suggestions[choice]
                break
        except ValueError:
            if len(country) > 1:
                break
    return country


def update_changes(all_changes, old, new):
    all_changes[old] = new


def do_file_checks(datadir, srcdata, procdata):
    """
    Performs validation to ensure datadir is a valid location,
    srcdata exists, and procdata does not exist.  Aborts if
    datadir or srcdata do not exist. Asks to proceed if procdata
    already exists
    """
    file_checks.assert_location_exists(datadir)
    file_checks.assert_file_exists(srcdata)
    try:
        file_checks.assert_file_not_exists(procdata)
    except AssertionError:
        message = f"File {procdata} already exists. If you proceed it " \
            "will be overwritten. Continue anyways?"
        response = user_interaction.force_user_input(["Y", "n"], message)
        if response == "n":
            raise SystemExit()


def main():
    do_file_checks(data_directory, source_data, processed_data)

    with open(source_data, 'r', encoding="iso-8859-1") as src, \
            TemporaryFile('w+', encoding="utf8", dir=data_directory) as tmp,          \
            open(processed_data, 'w', encoding="utf8") as dest:
        clean_users(src, tmp)
        reset_stream(tmp)
        clean_locations(tmp, dest)


if __name__ == '__main__':
    main()
