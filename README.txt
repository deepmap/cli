The DeepMap Command Line Interface

A CLI that provides a convenient method of making requests to the DeepMap API.
Using the API requires a Bearer JWT token, which can be obtained in two ways:

1. Through an http PUT request to the '/api/auth/v1/login' endpoint of the
   relevant API. Requires a body with string fields "username" and "password".

   However, this endpoint will be deprecated, and replaced with an Auth0 PKCE
   login, accessible through an online portal, for improved security.

   Once this method has been used, method #2 is most likely preferable for
   convenience.

2. Using the Login command. This requires a valid API access token, which is
   returned by the 'Create API Token Subcommand', but requires method #1 for
   first time login.

   Once an API access token has been created, it can be used to login until
   it is deleted by the creator.

_______________________________________________________________________________
Installation

Pull from GitHub with 'git clone https://github.com/deepmap/cli.git'.

If installing from pulled source code, run 'pip install .' on the directory
containing 'setup.py'. Then, the CLI is accessible with 'deepmap' in a
terminal.

Also requires the 'deepmap-sdk' python package, which can be pulled with
'git clone https://github.com/deepmap/sdk.git'.

Both will eventually be published to the PyPI, and installable with
'pip install deepmap-cli' and 'pip install deepmap-sdk'.

_______________________________________________________________________________
Help Information

Use the -h flag for help information.
For example, for general help, run "deepmap -h"
For help on using a command, run: "deepmap <command> -h", replacing <command>
with the specific command e.g. "deepmap login -h" for login command help.

Also, prefix abbreviations are allowed for parameter names,
as long as the abbreviation is unique e.g. --u or --user or --usern for
--username in the login command.

_______________________________________________________________________________
Possible commands are:

    login

    		Receives and stores an authentication token for the api.

    reset_password

    		Reset a password for an account.

    create

    		Create a new access token, or session token from an access token.

    download
    		{feature_tile, distribution}

    		Downloads the specified files and pipes output to stdout.

    list
    		{users, maps, tokens, feature_tiles}

    		List valid users, maps, tokens, or tiles.

    get
    		{user}

    		Get an object, like a user's information.

    invite

    		Invite a user to join your account.

    edit
    		{user}

    		Edit the email or admin permissions of a user.

    delete
    		{user, token}

    		Delete a user or token from your account.

_______________________________________________________________________________
Login Command

usage: deepmap login [-h] [--server_url SERVER_URL] token

Login to receive an authorization token using an API access token.

positional arguments:
  token                 An API access token.

optional arguments:
  --server_url SERVER_URL
                        The base url of the api server requested. Will persist
                        if not reset with a new --server_url.

_______________________________________________________________________________
Reset Password Command

usage: deepmap reset_password [-h] email

Trigger a password reset.

positional arguments:
  email       The email of the account to reset password.

_______________________________________________________________________________
Create Command

usage: deepmap create [-h] {token,session} ...

Create an access token or session token.

positional arguments:
  {token,session}

...............................................................................
Create Token Subcommand

usage: deepmap create token [-h] {vehicle,api} ...

Create an access token.

positional arguments:
  {vehicle,api}

...............................................................................
Create API Token Subcommand

usage: deepmap create token api [-h] description

Create an API access token.

positional arguments:
  description  User-provided description for the token user.

...............................................................................
Create Vehicle Token Subcommand

usage: deepmap create token vehicle [-h] vehicle_id description

Create a vehicle access token.

positional arguments:
  vehicle_id   User-provided id for the vehicle.
  description  User-provided description for the vehicle.

...............................................................................
Create Session Subcommand

usage: deepmap create session [-h] {vehicle,api} ...

Create a session token.

positional arguments:
  {vehicle,api}

...............................................................................
Create API Session Subcommand

usage: deepmap create session api [-h] token

Create an API session token.

positional arguments:
  token       A valid API access token.

...............................................................................
Create Vehicle Session Subcommand

usage: deepmap create session vehicle [-h] token

Create a vehicle session token.

positional arguments:
  token       A valid vehicle access token.

_______________________________________________________________________________
List Command

usage: deepmap list [-h] {maps,feature_tiles,tokens,users} ...

List the target objects.

positional arguments:
  {maps,feature_tiles,tokens,users}

...............................................................................
List Maps Subcommand

usage: deepmap list maps [-h]

List maps.

...............................................................................
List Users Subcommand

usage: deepmap list users [-h]

List users.

...............................................................................
List Feature Tiles Subcommand

usage: deepmap list feature_tiles [-h] id

List feature tiles for a map.

positional arguments:
  id          Id of the map.

...............................................................................
List Tokens Subcommand

usage: deepmap list tokens [-h] {api,vehicle} ...

List tokens.

positional arguments:
  {api,vehicle}

...............................................................................
List API Tokens Subcommand

usage: deepmap list tokens api [-h]

List issued API access tokens.

................................................................................
List Vehicle Tokens Subcommand

usage: deepmap list tokens vehicle [-h]

List issued vehicle access tokens.

_______________________________________________________________________________
Download Command

usage: deepmap download [-h] {feature_tile,distribution} ...

Download data.

positional arguments:
  {feature_tile,distribution}
    feature_tile        Download a feature tile of a map.
    distribution        Download a map distribution.

...............................................................................
Download Feature Tile Subcommand

usage: deepmap download feature_tile [-h] id

positional arguments:
  id          The id of the feature_tile to download

...............................................................................
Download Map Distribution Subcommand

usage: deepmap download distribution [-h] [--format FORMAT]
                                     [--version VERSION]
                                     id

positional arguments:
  id                 The id of the map distribution to download

optional arguments:
  --format FORMAT    Format of the distribution to download. Required if
                     multiple formats are available.
  --version VERSION  Optional: Version of the map to download. Otherwise
                     latest version is downloaded.

_______________________________________________________________________________
Invite Command

usage: deepmap invite [-h] [--admin {True,False}] email

Invite a user to join your account.

positional arguments:
  email                 The email of the user to invite.

optional arguments:
  --admin {True,False}  Optional: True if the user should be an admin.

_______________________________________________________________________________
Get Command

usage: deepmap get [-h] {user} ...

Get information about an object.

positional arguments:
  {user}

...............................................................................
Get User Subcommand

usage: deepmap get user [-h] id

Get user information.

positional arguments:
  id          The id of the user.

_______________________________________________________________________________
Edit Command

usage: deepmap edit [-h] {user} ...

Edit something.

positional arguments:
  {user}

...............................................................................
Edit User Subcommand

usage: deepmap edit user [-h] [--email EMAIL] [--admin {True,False}] id

Edit a user's information.

positional arguments:
  id                    The target user to edit.

optional arguments:
  --email EMAIL         Optional: The user's new email.
  --admin {True,False}  Optional: True or False, if the user is to be an
                        admin.

_______________________________________________________________________________
Delete Command

usage: deepmap delete [-h] {user,token} ...

Delete something.

positional arguments:
  {user,token}

...............................................................................
Delete User Subcommand

usage: deepmap delete user [-h] id

Delete a user.

positional arguments:
  id          The id of the user.

...............................................................................
Delete Token Subcommand

usage: deepmap delete token [-h] {api,vehicle} ...

Delete a token.

positional arguments:
  {api,vehicle}

...............................................................................
Delete API Token Subcommand

usage: deepmap delete token api [-h] id

Delete an issued API access token.

positional arguments:
  id          The id of the API token.

...............................................................................
Delete Vehicle Token Subcommand

usage: deepmap delete token vehicle [-h] id

Delete an issued vehicle access token.

positional arguments:
  id          The id of the vehicle token.

_______________________________________________________________________________
