#!/usr/bin/env python

import click

from functools import wraps

from nextcode import get_service
from nextcode.exceptions import ServerError, InvalidProfile
from nextcodecli.utils import print_error, abort, check_profile

status_to_color = {
    'PENDING': 'yellow',
    'COMPLETED': 'green',
    'STARTED': 'yellow',
    'ERROR': 'red',
    'CANCELLED': 'white',
}


def check_project(func):
    @wraps(func)
    def _check(*args, **kwargs):
        ctx = click.get_current_context()
        svc = ctx.obj.service
        if not svc.project:
            abort("Please set a project by running: nextcode query project [name]")
        else:
            return func(*args, **kwargs)

    return _check


@click.group()
@click.pass_context
def cli(ctx):
    """Root subcommand for query api functionality"""
    if ctx.obj.service is None:
        check_profile(ctx)
        ctx.obj.service = ctx.obj.client.service("query")


from nextcodecli.commands.query.run import run, project, info, results, cancel, list_queries
from nextcodecli.commands.query.templates import templates
from nextcodecli.commands.query.status import status

cli.add_command(run)
cli.add_command(project)
cli.add_command(info)
cli.add_command(results)
cli.add_command(cancel)
cli.add_command(list_queries)

cli.add_command(templates)

cli.add_command(status)
