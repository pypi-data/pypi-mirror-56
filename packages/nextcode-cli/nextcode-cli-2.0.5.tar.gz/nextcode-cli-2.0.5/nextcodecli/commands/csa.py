import sys
import datetime
import click
from click import command, argument, pass_context, secho, echo
import requests
import logging
from tabulate import tabulate
from requests import codes
from urllib.parse import urljoin

import nextcode
from nextcode.utils import check_resp_error
from nextcode.usermanage import CSASession
from nextcode.exceptions import AuthServerError
from nextcodecli.utils import abort, dumps, print_tab

log = logging.getLogger(__name__)

CLIENT_ID = 'api-key-client'


@click.group()
@click.option(
    '-u',
    '--username',
    envvar='CSA_USERNAME',
    prompt=True,
    help="Administrator user in the CSA instance",
)
@click.option(
    '-p',
    '--password',
    envvar='CSA_PASSWORD',
    prompt=True,
    help="Password for administrator user",
    hide_input=True,
)
@pass_context
def cli(ctx, username, password):
    """
    Manage CSA users

    Requires the CSA admin username and passwords, which you can put into envivonment as CSA_USERNAME and CSA_PASSWORD
    """
    client = nextcode.Client()
    root_url = client.profile.root_url
    session = CSASession(root_url, username, password)
    log.info("Managing users on CSA server %s..." % session.csa_url)
    ctx.obj.session = session


@command(help="Create a user in the CSA instance")
@argument('user_name', nargs=1)
@argument('password', nargs=1)
@pass_context
def create_user(ctx, user_name, password):
    try:
        ctx.obj.session.create_user(user_name, password)
    except AuthServerError as ex:
        abort(ex)
    secho("User '%s' has been created" % (user_name), bold=True)


@command(help="Add a user to a project")
@argument('user_name', nargs=1)
@argument('project', nargs=1)
@click.option('-r', '--role', default="researcher", help='Role for this user')
@pass_context
def add_to_project(ctx, user_name, project, role):
    try:
        ctx.obj.session.add_user_to_project(user_name, project, role)
    except AuthServerError as ex:
        abort(ex)
    secho("User '%s' has been added to project %s" % (user_name, project), bold=True)


@command(help="Get a list of all projects in the CSA instance")
@click.option('-r', '--raw', 'is_raw', is_flag=True)
@pass_context
def projects(ctx, is_raw):
    projects = ctx.obj.session.get_projects()
    if is_raw:
        echo(projects)
    else:
        table = tabulate([[p] for p in projects], headers=["Project Name"])
        echo(table)


cli.add_command(create_user)
cli.add_command(add_to_project)
cli.add_command(projects)
