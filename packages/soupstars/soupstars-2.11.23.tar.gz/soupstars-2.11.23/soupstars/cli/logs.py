import click

from soupstars.config import Config
from soupstars.resources import RunsResource, RunsLogResource
from soupstars.cli.printers import tableify


@click.group()
@click.option('--token', '-t', help="Token to use. Default None")
@click.option('--host', '-h', default=None, help="Host to use")
@click.pass_context
def logs(context, token, host):
    """
    Commands for viewing run logs
    """

    context.obj = Config(token=token, host=host)


@logs.command()
@click.pass_obj
def ls(config):
    """
    List available logs
    """

    runs = RunsResource(config=config)
    resp = runs.get()
    if resp.ok:
        headers = ['Id', 'Parser', 'Active', 'Archived']
        rows = []
        for run in resp.json():
            id = run['id']
            parser = run['parser']['name']
            active = run.get('instance_created_at') and not run.get('instance_deleted_at')
            archived = run['archived_at']
            rows.append([id, parser, active, archived])
        tableify(headers=headers, rows=rows)


@logs.command()
@click.pass_obj
@click.argument('run_id')
def download(config, run_id):
    """
    Download a log
    """

    logs = RunsLogResource(config=config, run_id=run_id)
    resp = logs.get()
    if resp.ok:
        for log in resp.json():
            print(log['created_at'], log['message'])
