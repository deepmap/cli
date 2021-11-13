""" Deepmap API CLI requests functions. """

import os
import sys
import json
import getpass
import time
import shutil
import requests
import jwt

from deepmap_cli.utils import init_headers, print_formatted_json
from deepmap_cli.constants import DIR_PATH, TOKEN_PATH, USER_CONFIG_PATH,\
    DEFAULT_PERMISSIONS, DIR_PERMISSIONS


def get_token():
    """ Verifies the validity of tokens and tells user to login if token is invalid.

    Returns:
        The authorization token stored in ~/.deepmap/token if that file exists.
    """
    expired = False
    # Check that the deepmap path exists.
    if os.path.isdir(DIR_PATH):
        # Check that the token file exists.
        if os.path.isfile(TOKEN_PATH):
            with open(TOKEN_PATH, mode='r') as token_file:
                token = token_file.readline()
            decoded_token = jwt.decode(token,
                                       algorithms=["ES256"],
                                       verify=False)
            # Compares the epoch unix timestamps of current time vs expiration time.
            if time.time() < decoded_token['exp']:
                return token
            expired = True
    if expired:
        sys.exit('Please login. Your authentication token is expired.')
    sys.exit('Please login. Your authentication token could not be found.')


def _login(args, server_url):
    """ Logs a user in, stores their authorization token, and stores the
    base api if one is provided.

    Args:
        args: A namespace of parameters automatically generated by the parser.
        server_url: String representing the base url of the API.
    """

    from deepmap_sdk.auth import create_api_session
    url, payload, headers = create_api_session(args.token, server_url)

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Valid response, store the token.
    if response.status_code == 200:
        token = response.json()['token']

        # If the token directory path doesn't exist, make it.
        if not os.path.isdir(DIR_PATH):
            os.mkdir(DIR_PATH)

        # Write the token into a file and set permissions to user read write
        with open(TOKEN_PATH, mode='w') as token_file:
            print(token, file=token_file, end='')

        # Write the url of the api if one was provided by the user
        if args.server_url:
            with open(USER_CONFIG_PATH, mode='w') as config_file:
                print(args.server_url, file=config_file, end='')
            print("Server url updated.", end=' ')
            os.chmod(USER_CONFIG_PATH, mode=DEFAULT_PERMISSIONS)

        os.chmod(TOKEN_PATH, mode=DEFAULT_PERMISSIONS)
        os.chmod(DIR_PATH, mode=DIR_PERMISSIONS)
        sys.exit("Successfully logged in.")
    else:
        print_formatted_json(response.json())


def _reset_password(args, server_url):
    """ Triggers a password reset attempt.

    Args:
        args: A namespace of paramaters automatically generated by the parser.
        server_url: String representing the base url of the API.
    """

    from deepmap_sdk.auth import reset_password_auth
    url, payload, headers = reset_password_auth(args.email, server_url)

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        sys.exit('Password reset sent if email exists.')
    else:
        print_formatted_json(response.json())


def _create(args, server_url):
    """ Create an access token or session token.

    Args:
        args: A namespace of paramaters automatically generated by the parser.
        server_url: String representing the base url of the API.
    """

    from deepmap_sdk.auth import create_api_token, create_vehicle_token, create_api_session, create_vehicle_session

    arg_missing = False
    if args.create_target:
        if args.create_target == 'token':
            if args.create_token_target:
                if args.create_token_target == 'api':
                    url, payload = create_api_token(args.description,
                                                    server_url)
                elif args.create_token_target == 'vehicle':
                    url, payload = create_vehicle_token(
                        args.vehicle_id, args.description, server_url)
                token = get_token()
                headers = init_headers(token)
            else:
                arg_missing = True
        elif args.create_target == 'session':
            if args.create_session_target:
                url, payload, headers = locals()['create_' +
                                                 args.create_session_target +
                                                 '_' + args.create_target](
                                                     args.token, server_url)
            else:
                arg_missing = True
    else:
        arg_missing = True

    if arg_missing:
        sys.exit(
            "Missing a positional argument. Use -h after your command to get help information."
        )

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print_formatted_json(response.json())

def _download_tiles_in_bbox(args, server_url):
    token = get_token()
    headers = init_headers(token)

    from deepmap_sdk.tiles import search_tiles
    print(locals().keys())
    search_url = locals()['search_tiles'](args.id,
                                       server_url,
                                       args.z,
                                       args.lat1,
                                       args.lat2,
                                       args.lng1,
                                       args.lng2,
                                       args.format,
                                       args.before,
                                       args.after)
    response = requests.get(search_url, headers=headers)
    tiles = response.json()
    response.close()

    for tile in tiles:
        print(tile)
        from deepmap_sdk.tiles import download_tile
        url = locals()['download_tile'](args.id,
                                       server_url,
                                       tile['z'],
                                       tile['x'],
                                       tile['y'],
                                       args.format,
                                       tile['release_timestamp'],
                                       tile['release_timestamp'])
        _download_tile_by_url(url, args.dest_folder, args.format, args.id,tile['x'], tile['y'], tile['z'])
    print("Downloaded {} tiles".format(len(tiles)))


def _download(args, server_url):
    """ Requests some data.

    Args:
        args: A namespace of parameters automatically generated by the parser.
        server_url: String representing the base url of the API.
    """

    from deepmap_sdk.tiles import download_feature_tile, download_tile
    from deepmap_sdk.maps import download_distribution

    if args.download_target:
        if args.download_target == 'distribution':
            url = locals()['download_' + args.download_target](args.id,
                                                               server_url,
                                                               args.format,
                                                               args.version)
        elif args.download_target == 'tile':
            url = locals()['download_' + args.download_target](args.id,
                                                               server_url,
                                                               args.z,
                                                               args.x,
                                                               args.y,
                                                               args.format,
                                                               args.before,
                                                               args.after)
        elif args.download_target == 'tile_bbox':
            _download_tiles_in_bbox(args, server_url)
            return
        else:
            url = locals()['download_' + args.download_target](args.id,
                                                               server_url)
    else:
        sys.exit(
            "Missing a positional argument. Use -h after your command to get help information."
        )

    _download_tile_by_url_with_args(url, args)

def _download_tile_by_url_with_args(url, args):
    token = get_token()
    headers = init_headers(token)
    with requests.get(url, headers=headers, stream=True) as response:
        if response.status_code == 200:
            dest = "result"
            if len(args.dest_folder) > 0:
                if args.format == "LMapTile3D" or args.format == "lmap":
                    dest = '{}/{}_{}_{}_{}_{}.pb.bin'.format(args.dest_folder, args.format, args.id, args.x, args.y, args.z)
                if args.format == "GeoJsonTile" or args.format == "geojson":
                    dest = '{}/{}_{}_{}_{}_{}.tar.gz'.format(args.dest_folder, args.format, args.id, args.x, args.y, args.z)
                else:
                    dest = '{}/{}_{}.tar.gz'.format(args.dest_folder, args.id, args.format)
            fdst = open(dest, 'wb')
            print("write to dest {}".format(dest))
            shutil.copyfileobj(response.raw, fdst)
            fdst.close()
        else:
            print_formatted_json(response.json(), fd=sys.stderr)
        response.close()

def _download_tile_by_url(url, dest_folder, format, id=None, x=None, y=None, z=None):
    token = get_token()
    headers = init_headers(token)
    with requests.get(url, headers=headers, stream=True) as response:
        if response.status_code == 200:
            dest = "result"
            if len(dest_folder) > 0:
                if format == "LMapTile3D" or format == "lmap":
                    dest = '{}/{}_{}_{}_{}_{}.pb.bin'.format(dest_folder, format, id, x, y, z)
                if format == "GeoJsonTile" or format == "geojson":
                    dest = '{}/{}_{}_{}_{}_{}.tar.gz'.format(dest_folder, format, id, x, y, z)
                else:
                    dest = '{}/{}_{}.tar.gz'.format(dest_folder, id, format)
            fdst = open(dest, 'wb')
            print("write to dest {}".format(dest))
            shutil.copyfileobj(response.raw, fdst)
            fdst.close()
        else:
            print_formatted_json(response.json(), fd=sys.stderr)
        response.close()

def _list(args, server_url):
    """ Requests a list of the target objects.

    Args:
        args: A namespace of parameters automatically generated by the parser.
        server_url: String representing the base url of the API.
    """
    token = get_token()
    headers = init_headers(token)

    from deepmap_sdk.users import list_users
    from deepmap_sdk.maps import list_maps
    from deepmap_sdk.tiles import list_feature_tiles, list_tiles_diff
    from deepmap_sdk.auth import list_api_tokens, list_vehicle_tokens

    arg_missing = False

    if args.list_target:
        if args.list_target == 'feature_tiles':
            url = list_feature_tiles(args.id, server_url)
        elif args.list_target == 'tiles_diff':
            url = locals()['list_' + args.list_target](args.id,
                                                       server_url,
                                                       args.z,
                                                       args.format,
                                                       args.before,
                                                       args.after)
        elif args.list_target == 'tokens':
            if args.list_tokens_target:
                url = locals()["list_" + args.list_tokens_target + '_' +
                               args.list_target](server_url)
            else:
                arg_missing = True
        else:
            url = locals()["list_" + args.list_target](server_url)
    else:
        arg_missing = True

    if arg_missing:
        sys.exit(
            "Missing a positional argument. Use -h after your command to get help information."
        )

    response = requests.get(url, headers=headers)
    print_formatted_json(response.json())

def _search(args, server_url):
    """ Search the target objects.

     Args:
         args: A namespace of parameters automatically generated by the parser.
         server_url: String representing the base url of the API.
     """
    token = get_token()
    headers = init_headers(token)

    from deepmap_sdk.tiles import search_tiles

    arg_missing = False

    if args.search_target:
        if args.search_target == 'tiles':
            url = locals()['search_' + args.search_target](args.id,
                                                       server_url,
                                                       args.z,
                                                       args.lat1,
                                                       args.lat2,
                                                       args.lng1,
                                                       args.lng2,
                                                       args.format,
                                                       args.before,
                                                       args.after)
        else:
            url = locals()["search_" + args.search_target1](server_url)
    else:
        arg_missing = True

    if arg_missing:
        sys.exit(
            "Missing a positional argument. Use -h after your command to get help information."
        )

    response = requests.get(url, headers=headers)
    print_formatted_json(response.json())

def _invite(args, server_url):
    """ Invites a user.

    Args:
        args: A namespace of parameters automatically generated by the parser.
        server_url: String representing the base url of the API.
    """
    token = get_token()
    headers = init_headers(token)

    from deepmap_sdk.users import invite_user
    url, payload = invite_user(args.email, args.admin, server_url)

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print_formatted_json(response.json())


def _get(args, server_url):
    """ Prints out a description of the user.

    Args:
        args: A namespace of parameters automatically generated by the parser.
        server_url: String representing the base url of the API.
    """

    token = get_token()
    headers = init_headers(token)

    from deepmap_sdk.users import get_user

    if args.get_target:
        url = get_user(args.id, server_url)
    else:
        sys.exit(
            "Missing a positional argument. Use -h after your command to get help information."
        )

    response = requests.get(url, headers=headers)
    print_formatted_json(response.json())


def _edit(args, server_url):
    """ Edits a user's admin status or email.

    Args:
        args: A namespace of parameters automatically generated by the parser.
        server_url: String representing the base url of the API.
    """

    token = get_token()
    headers = init_headers(token)

    from deepmap_sdk.users import edit_user

    if args.edit_target:
        url, payload = edit_user(args.id, args.email, args.admin, server_url)
    else:
        sys.exit(
            "Missing a positional argument. Use -h after your command to get help information."
        )

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        sys.exit("User edited.")
    else:
        print_formatted_json(response.json())


def _delete(args, server_url):
    """ Delete a user.

    Args:
        args: A namespace of parameters automatically generated by the parser.
        server_url: String representing the base url of the API.
    """
    token = get_token()
    headers = init_headers(token)

    from deepmap_sdk.users import delete_user
    from deepmap_sdk.auth import delete_api_token, delete_vehicle_token

    arg_missing = False
    if args.del_target:
        if args.del_target == 'token':
            if args.del_token_target:
                url = locals()['delete_' + args.del_token_target + '_' +
                               args.del_target](args.id, server_url)
            else:
                arg_missing = True
        else:
            url = locals()['delete_' + args.del_target](args.id, server_url)
    else:
        arg_missing = True

    if arg_missing:
        sys.exit(
            "Missing a positional argument. Use -h after your command to get help information."
        )

    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        sys.exit(args.del_target + " deleted.")
    else:
        print_formatted_json(response.json())


def make_request(args, server_url):
    """ Wrapper function to make a request.

    Args:
        args: Namespace generated by the cli parser.
        server_url: Base url for the API server.
    """
    globals()["_" + args.command](args, server_url)
