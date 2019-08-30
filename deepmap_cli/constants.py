""" File for computing and storing constants. """
import os
import stat

# Constants
DIR_PATH = os.path.expanduser('~/.deepmap')
TOKEN_PATH = os.path.join(DIR_PATH, 'token')
USER_CONFIG_PATH = os.path.join(DIR_PATH, 'config')
DEFAULT_PERMISSIONS = stat.S_IWUSR | stat.S_IRUSR  # user read write only
DIR_PERMISSIONS = DEFAULT_PERMISSIONS | stat.S_IXUSR  # add execute permissions
