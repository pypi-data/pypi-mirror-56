#!/usr/bin/env python

import os
import logging
import click
import yaml
import json
import requests

log = logging.getLogger(__name__)


@click.command()
@click.argument('url')
def cli(url):
    """
    Authenticate against CSA (for import).

    Example:
       nextcode csa_authenticate https://ci.wuxinextcodedev.com
    """
    username = click.prompt(click.style('USERNAME'), type=str)
    password = click.prompt(click.style('PASSWORD'), type=str, hide_input=True)

    credentials = {'username': username, 'password': password, 'url': url}

    is_verified = verify_credentials(credentials)

    if is_verified:
        full_path = os.path.expanduser('~/.nextcode/csa_authentication')
        dir_name = os.path.dirname(full_path)

        # Workaround if-statement to make the module compatible with Python2
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(full_path, 'w+') as outfile:
            yaml.safe_dump(credentials, outfile, default_flow_style=False, allow_unicode=True)
        click.echo(click.style('AUTHENTICATION SUCCESSFUL', fg='green'))

    else:
        click.echo(click.style('AUTHENTICATION FAILED', fg='red'))


def verify_credentials(credentials):
    try:
        response = authenticate(credentials)
    except requests.exceptions.ConnectionError:
        raise SystemExit(
            click.style('COULD NOT CONNECT TO SERVER - is the url correct ?', fg='red')
        )
    try:
        data = response.json()
    # ValueError includes JSONDecoderError and is compatible with Python2
    except ValueError:
        data = {}

    error = data.get('error', None)
    full_message_is_valid = error and error.get('full_message') == "Couldn't find Subject"
    return response.status_code == 404 and full_message_is_valid


def authenticate(credentials):
    username = credentials.get('username')
    password = credentials.get('password')
    url = credentials.get('url') + '/csa/api/subjects/key.json'
    response = requests.get(url, auth=(username, password))
    return response
