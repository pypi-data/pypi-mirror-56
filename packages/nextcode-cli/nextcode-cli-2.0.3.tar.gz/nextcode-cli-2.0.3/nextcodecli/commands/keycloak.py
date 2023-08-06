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
from nextcode.usermanage import KeycloakSession
from nextcode.exceptions import AuthServerError
from nextcodecli.utils import abort, dumps, print_tab

log = logging.getLogger(__name__)

CLIENT_ID = 'api-key-client'

def _get_user(ctx, user_name):
    try:
        user = ctx.obj.session.get_user(user_name)
    except AuthServerError as ex:
        abort(ex)
    return user


@click.group()
@click.option(
    '-u',
    '--username',
    default='admin',
    help="Administrator user in the keycloak instance",
    show_default=True,
)
@click.option(
    '-p',
    '--password',
    envvar='KEYCLOAK_PASSWORD',
    prompt=True,
    help="Password for administrator user",
    hide_input=True,
)
@click.option(
    '-r', '--realm', default='wuxinextcode.com', help="Keycloak realm to manage", show_default=True
)
@pass_context
def cli(ctx, username, password, realm):
    """
    Manage keycloak users

    Requires the keycloak admin password, which you can put into envivonment as KEYCLOAK_PASSWORD
    """
    client = nextcode.Client()
    root_url = client.profile.root_url
    session = KeycloakSession(root_url, username, password, realm)
    log.info("Managing users on keycloak server %s..." % session.auth_server)
    ctx.obj.session = session


@command(help="List all keycloak users in the realm")
@click.option('-r', '--raw', 'is_raw', is_flag=True, help='Dump raw json response')
@pass_context
def users(ctx, is_raw):
    users = ctx.obj.session.get_users()
    if is_raw:
        echo(dumps(users))
        return
    fields = ['username', 'email', 'name', 'enabled', 'created']
    table = []
    for user in users:
        table.append(
            [
                user['username'],
                user['email'],
                user.get('firstName', '') + ' ' + user.get('lastName', ''),
                user['enabled'],
                datetime.datetime.fromtimestamp(user['createdTimestamp'] // 1000),
            ]
        )
    tbl = tabulate(sorted(table), headers=fields)
    echo(tbl)


@command(help="View information about a keycloak user")
@argument('user_name', nargs=1)
@click.option('-r', '--raw', 'is_raw', is_flag=True, help='Dump raw json response')
@pass_context
def user(ctx, user_name, is_raw):
    user = _get_user(ctx, user_name)
    roles = ctx.obj.session.get_user_roles(user_name)

    if is_raw:
        echo(dumps(user))
        echo(dumps(roles))
        return
    print_tab('Username', user['username'])
    print_tab('Email', user['email'])
    print_tab('Enabled', user['enabled'])
    print_tab('Name', "%s %s" % (user.get('firstName') or '', user.get('lastName') or ''))
    print_tab('Created', datetime.datetime.fromtimestamp(user['createdTimestamp'] // 1000))
    if user.get('federatedIdentities'):
        print_tab('Federation', user['federatedIdentities'][0]['identityProvider'])
    else:
        print_tab('Federation', '(Local user)')
    available_roles = ctx.obj.session.get_available_roles_for_user(user_name)
    if available_roles:
        echo(
            "\nThe following roles can be added to the user: %s"
            % ', '.join(available_roles)
        )


@command(help="Add a new keycloak user")
@argument('user_name', nargs=1)
@click.option('-p', '--new_password', help='Password for new user', prompt=True)
@pass_context
def add_user(ctx, user_name, new_password):
    try:
        ctx.obj.session.create_user(user_name, new_password)
    except AuthServerError as ex:
        abort(ex)
    echo("Success! User has been created. Please use the following authentication information:\n")
    echo(
        "Username: %s\nPassword: %s"
        % (click.style(user_name, bold=True), click.style(new_password, bold=True))
    )
    echo("")


@command(help="Reset the password of a keycloak user")
@argument('user_name', nargs=1)
@click.option('-p', '--new_password', help='Password for new user', prompt=True)
@pass_context
def reset_password(ctx, user_name, new_password):
    user = _get_user(ctx, user_name)
    ctx.obj.session.set_user_password(user_name, new_password)
    echo("Password has been reset. Please use the following authentication information:\n")
    echo(
        "Username: %s\nPassword: %s"
        % (click.style(user_name, bold=True), click.style(new_password, bold=True))
    )
    echo("")


@command(help="Remove a keycloak user")
@argument('user_name', nargs=1)
@pass_context
def remove_user(ctx, user_name):
    user = _get_user(ctx, user_name)
    session = ctx.obj.session
    session.delete_user(user_name)
    secho("User '%s' has been deleted" % (user_name), bold=True)


@command(help="Add a new role to a keycloak user")
@argument('user_name', nargs=1)
@argument('role_name', nargs=1)
@pass_context
def add_role(ctx, user_name, role_name):
    user = _get_user(ctx, user_name)
    session = ctx.obj.session
    role_name = role_name.lower()
    user_roles = session.get_user_roles(user_name)
    if role_name in user_roles:
        abort("User '%s' already has role '%s'" % (user_name, role_name))

    available_roles = session.get_available_roles_for_user(user_name)
    if role_name not in available_roles:
        abort("Role '%s' is not available for user '%s'" % (role_name, user_name))

    ctx.obj.session.add_role_to_user(user_name, role_name)
    secho(
        "Role '%s' has been added to user '%s'"
        % (role_name, user_name),
        bold=True,
        fg='green',
    )


@command(help="Remove a role from a keycloak user")
@argument('user_name', nargs=1)
@argument('role_name', nargs=1)
@pass_context
def remove_role(ctx, user_name, role_name):
    user = _get_user(ctx, user_name)
    session = ctx.obj.session
    role_name = role_name.lower()
    user = session.get_user(user_name)
    try:
        session.remove_role_from_user(user_name, role_name)
    except AuthServerError as ex:
        abort(ex)
    secho(
        "Role '%s' has been removed from user '%s'"
        % (role_name, user_name),
        bold=True,
        fg='green',
    )

@command(help="Create a new role on the server")
@argument('role_name', nargs=1)
@pass_context
def create_server_role(ctx, role_name):
    session = ctx.obj.session
    role_name = role_name.lower()
    try:
        session.create_role(role_name)
    except AuthServerError as ex:
        abort(ex)
    secho(
        "Role '%s' has been created on the server"
        % (role_name),
        bold=True,
        fg='green',
    )

@command(help="Create a new role on the server")
@argument('role_name', nargs=1)
@pass_context
def delete_server_role(ctx, role_name):
    session = ctx.obj.session
    role_name = role_name.lower()
    try:
        session.delete_role(role_name)
    except AuthServerError as ex:
        abort(ex)
    secho(
        "Role '%s' has been deleted from the server"
        % (role_name),
        bold=True,
        fg='green',
    )



cli.add_command(users)
cli.add_command(user)
cli.add_command(add_user)
cli.add_command(remove_user)
cli.add_command(reset_password)
cli.add_command(add_role)
cli.add_command(remove_role)
cli.add_command(create_server_role)
cli.add_command(delete_server_role)
