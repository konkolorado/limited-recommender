"""
Contains various methods for interacting with users.
"""


def force_user_input(options, message=""):
    """
    Args
        options: a list of choices the user can choose from
        message: an optional prompt to display to the user
    Returns:
        the choice the user selected
    """
    if message != "":
        print(message)

    menu = "Options: [" + '/'.join(options) + "]\n"
    response = input(menu)
    while response not in options:
        response = input(menu)
    return response
