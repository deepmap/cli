""" Deepmap CLI util functions. """

import pprint
import stat
import sys

# constants
DEFAULT_PERMISSIONS = stat.S_IWUSR | stat.S_IRUSR  # user read write only


def init_headers(token):
    """ Returns a dictionary of headers with authorization token.

    Args:
        token: The string representation of an authorization token.
    Returns:
        The headers for a request with the api.
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    return headers


def print_formatted_json(data, fd=sys.stdout):
    """ Prints out a json prettily.

    Args:
        data: The json to print.
        fd: File descriptor where printing should be.
    """
    _pp = pprint.PrettyPrinter(width=80, compact=False, stream=fd)
    _pp.pprint(data)
