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
MAX_COUNT_THRESH = 930 # Locations appearing more than this are auto accepted
MIN_COUNT_THRESH = 1  # Locations appearing less than this are auto rejected
FILL_UNK = True       # Rejected locations are replaced with an UNK token
TOKEN = "unk"

def clean_users(src_stream, tmp_stream):
    tmp_stream.write(src_stream.readline()) # Header

    for line in src_stream:
        if missing_data(line):
            continue
        if missing_age(line):
            if FILL_UNK:
                line = update_line_age(line, TOKEN)
            else:
                continue
        if missing_country_data(line):
            if FILL_UNK:
                line = update_line_country(line, TOKEN)
            else:
                continue
        if get_line_age(line) > MAX_AGE or get_line_age(line) < MIN_AGE:
            continue

        line = process_data(line)
        line.encode("utf8")
        tmp_stream.write(line)

def missing_data(line):
    return len(line.split(";")) != 3

def missing_age(line):
    line = line.split(';')
    try:
        age = line[-1].strip()
    except IndexError:
        return True
    if age == "NULL":
        return True
    return False

def update_line_age(line, symbol):
    new_line = line.split(";")
    new_line[-1] = symbol
    new_line = ';'.join(new_line) + '\n'
    return new_line

def missing_country_data(line):
    *_, country = extract_city_state_country(line)
    country = country.replace('"', '')
    if country.strip() in ["", " ", "n/a", "NULL"]:
        return True

def get_line_age(line):
    line = line.strip().split(";")
    if line[-1] == TOKEN:
        return MAX_AGE - 1
    return int(line[-1].strip("\""))

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

def clean_locations(tmp_stream, dest_stream):
    """
    Cleaning the city, state, country data is hard to do without
    human input. Here we collect the number of times the city, state,
    country come up in the dataset and values that come up too scarcely
    are presented to the user for validation or rejection. We assume
    that only country validity matters
    """
    country_counts = get_country_counts(tmp_stream)
    accepted_countries = get_countries_above_max_threshold(country_counts)
    rejected_countries = get_countries_below_min_threshold(country_counts)
    changes = {}

    dest_stream.write(tmp_stream.readline()) # Header
    for line in tmp_stream:
        line = apply_user_changes_to_line(changes, line)
        *_, country = extract_city_state_country(line)

        if country in accepted_countries:
            dest_stream.write(line)
        elif country in rejected_countries:
            if FILL_UNK:
                update_changes(changes, country, TOKEN)
                line = update_line_country(line, TOKEN)
                dest_stream.write(line)
        else:
            recs = get_recommendations(accepted_countries, country)
            response = ask_user(country_counts, country, recs)
            if response == "R":
                rejected_countries.add(country)
                line = update_line_country(line, TOKEN)
            if response == "A":
                accepted_countries.add(country)
            if response == "M":
                new_country = get_new_country_from_user(recs)
                update_changes(changes, country, new_country)
                accepted_countries.add(new_country)
                line = update_line_country(line, new_country)
            if response in ["A", "M"] or FILL_UNK:
                dest_stream.write(line)

def get_country_counts(fname):
    """
    Records the number of times each country appears in the dataset
    """
    _ = fname.readline()

    country_counts = Counter()
    for line in fname:
        *_, country = extract_city_state_country(line)
        country_counts[country] += 1
    fname.seek(0)
    return country_counts

def get_countries_above_max_threshold(counts):
    """
    Creates a set of countries that have come up more than
    MAX_COUNT_THRESH times
    """
    return set(k for k,v in counts.items() if v >= MAX_COUNT_THRESH)

def get_countries_below_min_threshold(counts):
    """
    Creates a set of countries that have come up less than
    MIN_COUNT_THRESH times. This signals they are automatically rejected
    """
    return set(k for k,v in counts.items() if v <= MIN_COUNT_THRESH)

def apply_user_changes_to_line(changes, line):
    *_, country = extract_city_state_country(line)
    if country in changes:
        new_country = changes[country]
        return update_line_country(line, new_country)
    else:
        return line

def extract_city_state_country(line):
    return line.split(";")[1].split(",")

def update_line_country(line, new_country):
    new_line = line.split(";")
    location_data = new_line[1].split(",")
    location_data[-1] = new_country
    new_line[1] = ','.join(location_data)
    new_line = ';'.join(new_line)
    return new_line

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
        tmp.seek(0)
        clean_locations(tmp, dest)

if __name__ == '__main__':
    main()
