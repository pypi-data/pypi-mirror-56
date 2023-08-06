#!/usr/bin/env python

import os
import sys

import click
from click import pass_context, command, option, secho, echo
import requests
import logging

from nextcode.config import get_profile_config, get_default_profile, create_profile
from nextcode.exceptions import InvalidProfile
from nextcodecli.utils import abort, dumps

log = logging.getLogger(__name__)


@command()
@option('-u', '--username')
@option('-p', '--password')
@option('-r', '--realm', default='wuxinextcode.com')
@option(
    '-h',
    '--host',
    default=None,
    help="Host override if not using profile, e.g. platform.wuxinextcodedev.com",
)
@option(
    '-t',
    '--token',
    'is_token',
    is_flag=True,
    help="Return access tokens as json instead of writing into current profile",
)
@pass_context
def cli(ctx, username, password, realm, host, is_token):
    """
    Authenticate against keycloak.
    """
    config = get_profile_config()
    profile_name = get_default_profile()

    if username and password:
        if not is_token:
            echo("Authenticating from commandline parameters")
        client_id = 'api-key-client'
        body = {
            'grant_type': 'password',
            'client_id': client_id,
            'password': password,
            'username': username,
            'scope': 'offline_access',
        }
        if host:
            auth_server = "https://%s/auth" % host
        else:
            auth_server = config["root_url"] + "/auth"
        log.info("Using auth server '%s'" % auth_server)
        url = '%s/realms/%s/protocol/openid-connect/token' % (auth_server, realm)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        log.debug("Calling POST %s with headers %s and body %s", url, headers, body)
        resp = requests.post(url, headers=headers, data=body)
        log.debug("Response (%s): %s", resp.status_code, resp.text)
        if resp.status_code != 200:
            click.secho("Error logging in: %s" % resp.text, fg='red')
            sys.exit(1)
        if is_token:
            echo(dumps(resp.json()))
            return
        with open(config.token_files['refresh_token'], 'w') as f:
            f.write(resp.json()['refresh_token'])
        echo("You have been logged in")
    else:
        if host:
            root_url = "https://%s" % host
        else:
            root_url = config["root_url"]
        login_server = root_url + "/api-key-service"

        if login_server:
            echo("Launching login webpage ==> Please authenticate and then press continue.")
            click.launch(login_server)
            click.pause()
        else:
            click.secho(
                "No login server configured. Please aquire a refresh_token from "
                "somewhere manually.",
                fg='yellow',
            )

        # Note: readline must be imported for click.prompt() to accept long strings. Don't ask me why.
        import readline

        api_key = click.prompt("API Key", type=str)
        try:
            create_profile(profile_name, api_key=api_key)
        except InvalidProfile as ex:
            abort(ex)
