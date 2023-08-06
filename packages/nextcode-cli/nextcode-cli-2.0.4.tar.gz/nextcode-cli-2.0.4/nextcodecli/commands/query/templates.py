#!/usr/bin/env python
import click
import sys
import collections
from tabulate import tabulate
import dateutil
import yaml
from pathlib import Path

from nextcode.exceptions import ServerError
from nextcode.services.query.exceptions import TemplateError

from ...utils import print_tab, dumps, get_logger, abort

log = get_logger(name='commands.query', level='INFO')


def fmt_date(dt):
    return dateutil.parser.parse(dt).strftime("%Y-%m-%d %H:%M")


@click.group(help="Query Template management")
def templates():
    pass


@templates.command()
@click.option('-o', '--organization', help="The organization to show templates for")
@click.option('-c', '--category', help="Category for templates")
@click.option(
    '--raw', 'is_raw', is_flag=True, default=False, help='Raw JSON response from endpoint'
)
@click.pass_context
def list(ctx, organization, category, is_raw):
    """

    """
    svc = ctx.obj.service
    all_templates = svc.get_templates(organization=organization, category=category)
    template_list = []
    for name, templ in all_templates.items():
        full_name = templ['full_name']
        template_list.append(
            [
                templ['id'],
                templ['name'],
                templ['version'],
                full_name,
                fmt_date(templ['create_date']),
                templ['list_description'],
            ]
        )

    tbl = tabulate(
        template_list, headers=['id', 'name', 'version', 'full_name', 'date', 'description']
    )
    click.echo(tbl)


@templates.command()
@click.argument('name', nargs=1)
@click.pass_context
def delete(ctx, name):
    """
    Delete a template by full name (e.g. [org]/[category]/[name]/[version])
    """
    svc = ctx.obj.service
    try:
        svc.delete_template(name)
    except TemplateError as ex:
        abort(ex)
    click.secho("Template '%s' has been deleted." % (name), bold=True)


@templates.command()
@click.argument('name', nargs=1)
@click.option(
    '--raw', 'is_raw', is_flag=True, default=False, help='Raw JSON response from endpoint'
)
@click.option('--yaml', 'is_yaml', is_flag=True, default=False, help='Raw yaml template')
@click.option('--args', 'is_args', is_flag=True, default=False, help='View arguments')
@click.pass_context
def view(ctx, name, is_raw, is_yaml, is_args):
    svc = ctx.obj.service
    try:
        template = svc.get_template(name)
    except ServerError:
        abort("Template {} not found".format(name))

    if is_yaml:
        click.echo(template["file_contents"])
        return

    if is_args:
        if is_raw:
            click.echo(dumps(template['arguments']))
            return
        args_list = []
        for arg in template['arguments']:
            args_list.append(
                [
                    arg['name'],
                    arg.get('type'),
                    arg.get('optional'),
                    ", ".join(arg.get('values', [])),
                    arg.get('default', "")[:50],
                ]
            )
        args_list.sort()
        tbl = tabulate(args_list, headers=['name', 'type', 'optional', 'values', 'default'])
        click.echo(tbl)
        return
    if is_raw:
        click.echo(dumps(template))
        return
    print_tab('Template ID', template['id'])
    print_tab('Name', template['name'])
    print_tab('Organization', template['organization'])
    print_tab('Category', template['category'])
    print_tab('Date Created', fmt_date(template['create_date']))
    print_tab('Version', template['version'])
    print_tab('Description', template['list_description'])
    args = []
    for arg in template['arguments']:
        if not arg.get('optional'):
            args.append(arg['name'])
    print_tab('Required Arguments', ", ".join(args))
    print_tab('Perspectives', ", ".join([p['name'] for p in template['perspectives']]))


@templates.command()
@click.argument('filename', nargs=1)
@click.option('--replace', is_flag=True, default=False, help='Delete and replace existing template')
@click.pass_context
def add(ctx, filename, replace):
    """Add a new template from yaml file.
    """
    svc = ctx.obj.service
    try:
        full_name = svc.add_template_from_file(filename, replace=replace)
    except TemplateError as ex:
        abort(ex)

    click.secho("Template '%s' has been successfully added" % (full_name), bold=True)
    click.echo("View the template with: nextcode query templates view {}".format(full_name))


@templates.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('name', nargs=1)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def render(ctx, name, args):
    """Render a query from template
    """
    svc = ctx.obj.service
    try:
        _ = svc.get_template(name)
    except ServerError:
        abort("Template {} not found".format(name))
    params = {}
    for a in args:
        lst = a.split("=", 1)
        try:
            params[lst[0]] = lst[1]
        except IndexError:
            abort("Arguments invalid. Should be 'args=val")
    try:
        query_string = svc.render_template(name, params)
    except TemplateError as ex:
        if "Missing arguments" in str(ex):
            click.secho(str(ex), fg='red')
            click.echo(
                "Hint: You can view arguments for this template with: nextcode query templates view %s --args"
                % name
            )
            sys.exit(1)
        else:
            abort(ex)
    click.echo(query_string)
