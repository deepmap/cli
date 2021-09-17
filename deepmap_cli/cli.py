#!/usr/bin/env python3
""" A command line interface for the Deepmap API. """

import argparse
import sys
import os

from deepmap_cli.constants import USER_CONFIG_PATH
from deepmap_cli.cli_requests import make_request


def init_cli():
    """ Initializes the CLI. """
    parser = argparse.ArgumentParser(
        prog='deepmap',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Possible commands are:"
        "\n"
        "    login          Receives and stores an authentication token for the api.\n"
        "    reset_password Reset a password for an account.\n"
        "    create         Create a new access token, or session token from an access token.\n"
        "    download       Downloads the specified files and pipes output to stdout.\n"
        "    list           List valid users, maps, tokens, tiles_diff, or tiles.\n"
        "    search         Search valid tiles.\n"
        "    invite         Invite a user to join your account.\n"
        "    get user       Get a description of your account.\n"
        "    edit user      Edit the email or admin permissions of a user.\n"
        "    delete         Delete a user or token from your account.\n"
        "\n"
        "Use the -h flag for help information.\n"
        "For example, for general help, run \"deepmap -h\"\n"
        "For help on using a command, run: \"deepmap <command> -h\", replacing <command>\n"
        "with the specific command e.g. \"deepmap login -h\" for login command help.\n"
        "\n"
        "Also, prefix abbreviations are allowed for parameter names,\n"
        "as long as the abbreviation is unique e.g. --u or --user or --usern for\n"
        "--username in the login command.\n"
        "\n")
    subparsers = parser.add_subparsers(dest='command')

    init_login_parser(subparsers)
    init_reset_password_parser(subparsers)
    init_create_parser(subparsers)
    init_download_parser(subparsers)
    init_list_parser(subparsers)
    init_search_parser(subparsers)
    init_invite_parser(subparsers)
    init_get_parser(subparsers)
    init_edit_parser(subparsers)
    init_delete_parser(subparsers)

    args = parser.parse_args(sys.argv[1:])

    url_passed_in = False
    # Cast args to namespace for membership testing
    if 'server_url' in vars(args).keys():
        # Check if args.server_url is not None
        if args.server_url:
            server_url = args.server_url
            url_passed_in = True

    if not url_passed_in:
        # Retrieve url if a previous url is stored.
        if os.path.isfile(USER_CONFIG_PATH):
            with open(USER_CONFIG_PATH, mode='r') as config_file:
                server_url = config_file.readline()
        # Default url.
        else:
            server_url = 'https://api.deepmap.com'

    # Call the correct command if valid
    if args.command:
        make_request(args, server_url)
    else:
        parser.print_help()


def init_login_parser(subparsers):
    """ Sets up login parser args.

    Args:
        subparsers: subparsers object for the main parser.
    """

    login_parser = subparsers.add_parser(
        'login',
        description=
        'Login to receive an authorization token using an API access token.')
    login_parser.add_argument(
        '--server_url',
        help="The base url of the api server requested. "
        "Will persist if not reset with a new --server_url.")

    login_parser.add_argument('token', help='An API access token.')


def init_reset_password_parser(subparsers):
    """ Sets up password reset args.

    Args:
        subparsers: subparsers object for the main parser.
    """

    reset_password_parser = subparsers.add_parser(
        'reset_password', description='Trigger a password reset.')
    reset_password_parser.add_argument(
        'email', help='The email of the account to reset password.')


def init_create_parser(subparsers):
    """ Sets up create args.

    Args:
        subparsers: subparsers object for the main parser.
    """

    create_parser = subparsers.add_parser(
        'create', description='Create an access token or session token.')
    create_subparser = create_parser.add_subparsers(dest='create_target')

    # Create an access token.
    create_token_parser = create_subparser.add_parser(
        'token', description='Create an access token.')
    create_token_subparsers = create_token_parser.add_subparsers(
        dest='create_token_target')

    # Create a vehicle access token
    create_vehicle_token_parser = create_token_subparsers.add_parser(
        'vehicle', description='Create a vehicle access token.')
    create_vehicle_token_parser.add_argument(
        'vehicle_id', help='User-provided id for the vehicle.')
    create_vehicle_token_parser.add_argument(
        'description', help='User-provided description for the vehicle.')

    # Create an API access token
    create_api_token_parser = create_token_subparsers.add_parser(
        'api', description='Create an API access token.')
    create_api_token_parser.add_argument(
        'description', help='User-provided description for the token user.')

    # Create a session token.
    create_session_parser = create_subparser.add_parser(
        'session', description='Create a session token.')
    create_session_subparsers = create_session_parser.add_subparsers(
        dest='create_session_target')

    # Create a vehicle session token
    create_vehicle_session_parser = create_session_subparsers.add_parser(
        'vehicle', description='Create a vehicle session token.')
    create_vehicle_session_parser.add_argument(
        'token', help='A valid vehicle access token.')

    # Create an API session token
    create_api_session_parser = create_session_subparsers.add_parser(
        'api', description='Create an API session token.')
    create_api_session_parser.add_argument('token',
                                           help='A valid API access token.')


def init_download_parser(subparsers):
    """ Sets up download parser args.

    Args:
        subparsers: subparsers object for the main parser.
    """

    download_parser = subparsers.add_parser('download',
                                            description='Download data.')
    download_subparsers = download_parser.add_subparsers(
        dest='download_target')

    # Features tile is target of download.
    download_feature_tile_parser = download_subparsers.add_parser(
        'feature_tile', help='Download a feature tile of a map.')
    download_feature_tile_parser.add_argument(
        'id', help='The id of the feature_tile to download')

    # Map distribution is target of download.
    download_distribution_parser = download_subparsers.add_parser(
        'distribution', help='Download a map distribution.')
    download_distribution_parser.add_argument(
        'id', help='The id of the map distribution to download')
    download_distribution_parser.add_argument(
        '--format',
        help=
        'Format of the distribution to download. Required if multiple formats are available.'
    )
    download_distribution_parser.add_argument(
        '--version',
        help=
        'Optional: Version of the map to download. Otherwise latest version is downloaded.'
    )

    # Tile is target of download.
    download_tile_parser = download_subparsers.add_parser(
        'tile', help='Download a tile of a map.')
    download_tile_parser.add_argument(
        'id', help='The id of the map')
    download_tile_parser.add_argument(
        'z', help='Zoom level of the map.')
    download_tile_parser.add_argument(
        'x', help='The x offset into the tile grid at the specified zoom level. '
                  'Each level has 2^z x 2^z tiles, so level 0 is 1x1, level 10 is 1024x1024. '
                  'Our (0, 0) map offset is at the top left of the map.')
    download_tile_parser.add_argument(
        'y', help='The y offset into the tile grid at the specified zoom level. '
                  'Each level has 2^z x 2^z tiles, so level 0 is 1x1, level 10 is 1024x1024. '
                  'Our (0, 0) map offset is at the top left of the map.')
    download_tile_parser.add_argument(
        'format', help='The format for the desired tile. This must be a format that is available for this map. '
                       'The available formats of this map could be found by `deepmap list maps [-h]`.')
    download_tile_parser.add_argument(
        '--before', help='Optional: The timestamp in milliseconds. The upper bound of the time range which '
                       'targeted tile should belong to. If the field is set, it will only fetch tiles '
                       'which version is older than or equal to the given timestamp.')
    download_tile_parser.add_argument(
        '--after', help='Optional: The timestamp in milliseconds. The lower bound of the time range which targeted '
                      'tile should belong to. If the field is set, it will only fetch tiles which version '
                      'is newer than or equal to the given timestamp.')


def init_invite_parser(subparsers):
    """ Sets up invite parser args.

    Args:
        subparsers: subparsers object for the main parser.
    """

    invite_parser = subparsers.add_parser(
        'invite', description='Invite a user to join your account.')

    invite_parser.add_argument('email',
                               help='The email of the user to invite.')
    invite_parser.add_argument(
        '--admin',
        help='Optional: True if the user should be an admin.',
        choices=['True', 'False'])


def init_list_parser(subparsers):
    """ Sets up list parser args.

    Args:
        subparsers: subparsers object for the main parser.
    """
    list_parser = subparsers.add_parser('list',
                                        description='List the target objects.')
    list_subparsers = list_parser.add_subparsers(dest='list_target')

    # Maps are targets of list.
    list_subparsers.add_parser('maps', description='List maps.')

    # Feature tiles are targets of list.
    list_feature_tiles_parser = list_subparsers.add_parser(
        'feature_tiles', description='List feature tiles for a map.')
    list_feature_tiles_parser.add_argument('id', help='Id of the map.')

    # Users are targets of list.
    list_subparsers.add_parser('users', description='List users.')

    # Tokens are targets of list.
    list_tokens_parser = list_subparsers.add_parser('tokens',
                                                    description='List tokens.')
    list_tokens_subparsers = list_tokens_parser.add_subparsers(
        dest='list_tokens_target')

    # API token is target of list.
    list_tokens_subparsers.add_parser(
        'api', description='List issued API access tokens.')

    # Vehicle token is target of list.
    list_tokens_subparsers.add_parser(
        'vehicle', description='List issued vehicle access tokens.')

    # Updated tiles during given time gap.
    list_tiles_diff_parser = list_subparsers.add_parser(
        'tiles_diff', description='List updated tiles for a map.')
    list_tiles_diff_parser.add_argument(
        'id', help='Id of the map.')
    list_tiles_diff_parser.add_argument(
        'z', help='Zoom level of the map.')
    list_tiles_diff_parser.add_argument(
        'format', help='The format for the desired tile. This must be a format that is available for this map. '
                       'The available formats of this map could be found by `deepmap list maps [-h]`.')
    list_tiles_diff_parser.add_argument(
        '--before', help='Optional: The timestamp in milliseconds. The upper bound of the time range which '
                       'targeted tile should belong to. If the field is set, it will only fetch tiles '
                       'which version is older than or equal to the given timestamp.')
    list_tiles_diff_parser.add_argument(
        '--after', help='Optional: The timestamp in milliseconds. The lower bound of the time range which targeted '
                      'tile should belong to. If the field is set, it will only fetch tiles which version '
                      'is newer than or equal to the given timestamp.')

def init_search_parser(subparsers):
    """ Sets up search parser args.

    Args:
        subparsers: subparsers object for the main parser.
    """
    search_parser = subparsers.add_parser('search',
                                        description='Search the target objects.')
    search_subparsers = search_parser.add_subparsers(dest='search_target')

    # Updated tiles during given time gap.
    search_tile_parser = search_subparsers.add_parser(
        'tiles', description='Search tiles for a map.')
    search_tile_parser.add_argument(
        'id', help='Id of the map.')
    search_tile_parser.add_argument(
        'z', help='Zoom level of the map.')
    search_tile_parser.add_argument(
        'lat1', help='The first latitude of the web mercator bounding box.')
    search_tile_parser.add_argument(
        'lat2', help='The second latitude of the web mercator bounding box.')
    search_tile_parser.add_argument(
        'lng1', help='The first longitude of the web mercator bounding box.')
    search_tile_parser.add_argument(
        'lng2', help='The second longitude of the web mercator bounding box.')
    search_tile_parser.add_argument(
        'format', help='The format for the desired tile. This must be a format that is available for this map. '
                       'The available formats of this map could be found by `deepmap list maps [-h]`.')
    search_tile_parser.add_argument(
        '--before', help='Optional: The timestamp in milliseconds. The upper bound of the time range which '
                       'targeted tile should belong to. If the field is set, it will only fetch tiles '
                       'which version is older than or equal to the given timestamp.')
    search_tile_parser.add_argument(
        '--after', help='Optional: The timestamp in milliseconds. The lower bound of the time range which targeted '
                      'tile should belong to. If the field is set, it will only fetch tiles which version '
                      'is newer than or equal to the given timestamp.')

def init_get_parser(subparsers):
    """ Sets up get parser args.

    Args:
        subparsers: subparsers object for the main parser.
    """

    get_parser = subparsers.add_parser(
        'get', description='Get information about an object.')
    get_subparsers = get_parser.add_subparsers(dest='get_target')

    # A user is target of get.
    get_user_parser = get_subparsers.add_parser(
        'user', description='Get user information.')
    get_user_parser.add_argument('id', help='The id of the user.')


def init_delete_parser(subparsers):
    """ Sets up delete parser args.

    Args:
        subparsers: subparsers object for the main parser.
    """

    delete_parser = subparsers.add_parser('delete',
                                          description='Delete something.')
    delete_subparsers = delete_parser.add_subparsers(dest='del_target')

    # A user is target of delete.
    delete_user_parser = delete_subparsers.add_parser(
        'user', description='Delete a user.')
    delete_user_parser.add_argument('id', help='The id of the user.')

    # A token is target of delete.
    delete_token_parser = delete_subparsers.add_parser(
        'token', description='Delete a token.')
    delete_token_subparsers = delete_token_parser.add_subparsers(
        dest='del_token_target')

    # API token is target of delete.
    delete_api_token_parser = delete_token_subparsers.add_parser(
        'api', description='Delete an issued API access token.')
    delete_api_token_parser.add_argument('id', help='The id of the API token.')

    # Vehicle token is target of delete.
    delete_vehicle_token_parser = delete_token_subparsers.add_parser(
        'vehicle', description='Delete an issued vehicle access token.')
    delete_vehicle_token_parser.add_argument(
        'id', help='The id of the vehicle token.')


def init_edit_parser(subparsers):
    """ Sets up edit parser args.

    Args:
        subparsers: subparsers object for the main parser.
    """

    edit_parser = subparsers.add_parser('edit', description='Edit something.')
    edit_subparsers = edit_parser.add_subparsers(dest='edit_target')

    # A user is target of edit.
    edit_user_parser = edit_subparsers.add_parser(
        'user', description='Edit a user\'s information.')
    edit_user_parser.add_argument('id', help='The target user to edit.')
    edit_user_parser.add_argument('--email',
                                  help='Optional: The user\'s new email.')
    edit_user_parser.add_argument(
        '--admin',
        help='Optional: True or False, if the user is to be an admin.',
        choices=['True', 'False'])


if __name__ == '__main__':
    init_cli()
