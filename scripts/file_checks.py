import os


def assert_file_exists(filename):
    assert(os.path.isfile(filename)), f"{filename} does not exist"


def assert_file_not_exists(filename):
    assert(not os.path.isfile(filename)), f"{filename} exists"


def assert_location_exists(location):
    assert(os.path.isdir(location)), f"{location} does not exist"
