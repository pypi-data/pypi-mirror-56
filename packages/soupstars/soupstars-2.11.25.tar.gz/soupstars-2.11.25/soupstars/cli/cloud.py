import click
import os
import sys
import textwrap
import getpass
from importlib import import_module

from soupstars.cli.printers import jsonify, pythonify, tableify, integer_cents_to_usd
from soupstars.config import Config
from soupstars.resources import (
    UsersResource, StatusResource, AuthResource, ParsersResource,
    ProfileResource, RunsResource, ParserResource, ResultsResource,
    TopResource, PlansResource, AccountResource, ParserArchivesResource
)


@click.group()
@click.option('--token', '-t', help="Token to use. Default None")
@click.option('--host', '-h', default=None, help="Host to use")
@click.pass_context
def cloud(context, token, host):
    """
    Commands to interact with Soup Stars cloud
    """

    context.obj = Config(token=token, host=host)


@cloud.command()
@click.pass_obj
def health(config):
    """
    Print the status of the Soup Stars api
    """

    status = StatusResource(config=config)
    resp = status.get()
    jsonify(resp.json())


@cloud.command()
@click.pass_obj
def register(config):
    """
    Register a new account on Soup Stars cloud
    """

    email = input('Email: ')
    password = getpass.getpass(prompt='Password: ')
    password2 = getpass.getpass(prompt='Confirm password: ')

    if password != password2:
        print("Passwords did not match.")
        return

    users = UsersResource(config=config)
    resp = users.post(email=email, password=password)

    if resp.ok:
        auth = AuthResource(config=config)
        resp = auth.post(email=email, password=password)
        config.token = resp.json()['access_token']
        config.save()
    jsonify(resp.json())


@cloud.command()
@click.pass_obj
def login(config):
    """
    Log in with an existing email
    """

    email = input('Email: ')
    password = getpass.getpass(prompt='Password: ')
    auth = AuthResource(config=config)
    resp = auth.post(email=email, password=password)
    if resp.ok:
        config.token = resp.json()['access_token']
        config.save()

    jsonify(resp.json())


@cloud.command()
@click.pass_obj
def ls(config):
    """
    Print the list of parsers uploaded to Soup Stars cloud
    """

    parsers = ParsersResource(config=config)
    resp = parsers.get()
    if resp.ok:
        headers = ['Parser', 'Hash', 'Schedule', 'Last ran at', 'Last run results', 'Last updated']
        rows = []
        for row in resp.json():
            if row['schedule']:
                schedule_name = row['schedule']['name']
            else:
                schedule_name = None
            rows.append([
                row['name'],
                row['module_hash'],
                schedule_name,
                row['last_ran_at'],
                row['last_run_results'],
                row['updated_at']
            ])
        tableify(headers, rows)
    else:
        jsonify(resp.json())



@cloud.command()
@click.argument('module')
@click.option('--name', '-n', help="Name of the crawler. If not given, uses the module's file name.")
@click.pass_obj
def push(config, module, name):
    """
    Push a parser to Soup Stars cloud. Must be an importable module, eg `myparser` or `examples.parsers.myparser`
    """

    module = import_module(module)
    module_contents = open(module.__file__, 'r').read()
    name = name or module.__name__.split('.')[-1]
    parser = ParserResource(config=config, name=name)
    resp = parser.put(module=module_contents)
    jsonify(resp.json())


@cloud.command()
@click.argument('name')
@click.option('--force', is_flag=True, default=False, help="Overwrite existing module if it exists")
@click.pass_obj
def pull(config, name, force):
    """
    Pull a parser from Soup Stars cloud into a local module
    """

    parser = ParserResource(config=config, name=name)
    resp = parser.get()
    filename = resp.json()['name'] + '.py'
    module = resp.json()['module']
    if os.path.exists(filename) and not force:
        jsonify(f"{filename} already exists. Use --force to overwrite.")
    else:
        with open(filename, 'w') as o:
            o.write(module)
        jsonify(f"Finished writing module to {o.name}")


@cloud.command()
@click.argument('name')
@click.pass_obj
def show(config, name):
    """
    Print the contents of a parser on Soup Stars cloud
    """

    parser = ParserResource(config=config, name=name)
    resp = parser.get()
    if resp.ok:
        pythonify(resp.json()['module'])
    else:
        jsonify(resp.json())


@cloud.command()
@click.pass_obj
def recent(config):
    """
    Print recent pages that have been parsed
    """

    results = ResultsResource(config=config)
    resp = results.get()
    if resp.ok:
        headers = ['Parser', 'Status', 'URL', 'Created']
        rows = [(r['parser_name'], r['status_code'], r['url'][:75], r['created_at']) for r in resp.json()]
        tableify(headers, rows)
    else:
        jsonify(resp.json())


@cloud.command()
@click.pass_obj
def profile(config):
    """
    Print information about your profile
    """

    profile = ProfileResource(config=config)
    resp = profile.get()
    if not resp.ok:
        jsonify(resp.json())
        return
    data = resp.json()

    # It would be nice to add the downgrade date if the account is scheduled
    # to downgrade
    headers = ['Email', 'Plan', 'Price', 'Billing Cycle', 'Last billed']
    rows = [
        (
            data['email'],
            data['account']['plan']['name'].capitalize(),
            integer_cents_to_usd(data['account']['plan']['price'], round=True),
            data['account']['billing_cycle_duration'].split(',')[0],
            data['account']['last_billed_at']
        )
    ]
    tableify(headers, rows)


@cloud.command()
@click.pass_obj
def top(config):
    """
    Print recently active runs
    """

    top = TopResource(config=config)
    resp = top.get()
    if resp.ok:
        headers = ['Parser', 'Started', 'Status', 'Results']
        rows = []
        for r in resp.json():
            started = r['created_at']
            parser = r['parser']['name']
            results = r['results_count']
            if r['succeeded'] == True:
                status = click.style(r['status'], fg='green')
            elif r['succeeded'] == False:
                status = click.style(r['status'], fg='red')
            else:
                status = click.style(r['status'], fg='cyan')
            rows.append([parser, started, status, results])
        tableify(headers, rows)
    else:
        jsonify(resp.json())


@cloud.command()
@click.pass_obj
@click.pass_context
@click.argument('name')
@click.option('--interval', '-i', help="Interval to use. `daily` or `hourly`")
@click.option('--rm', is_flag=True, default=False, help="Add this flag to unschedule the parser")
def schedule(ctx, config, name, interval, rm):
    """
    Schedule or unschedule a parser
    """

    parser = ParserResource(config=config, name=name)
    if rm:
        resp = parser.patch(schedule=None)
    elif interval not in ('daily', 'hourly'):
        print("Must specify an interval to use, either `daily` or `hourly`")
    else:
        resp = parser.patch(schedule=interval)
    if resp.ok:
        ctx.invoke(ls)


@cloud.command()
@click.pass_obj
@click.pass_context
@click.argument('name')
@click.option('--confirm', help="Use the flag to confirm deleting the parser")
def rm(ctx, config, name, confirm):
    """
    Remove a parser and all related data
    """

    if not confirm:
        print(f"WARNING: Deleting a parser will permanently delete all associated data")
        print("This operation can NOT be undone")
        print(f"Please confirm the parser to delete with --confirm")
        print()
        print(f"\t soupstars cloud rm {name} --confirm {name}")
        print()
    elif confirm != name:
        print(f"Confirmation value did not match the parser's name: {name}")
    else:
        parser = ParserResource(config=config, name=name)
        resp = parser.delete()
        if resp.ok:
            ctx.invoke(ls)
        else:
            jsonify(resp.json())


@cloud.command()
@click.pass_obj
def plans(config):
    """
    Print the list of available plans
    """

    plans = PlansResource(config).get()
    if not plans.ok:
        jsonify(plans.json())
        return

    headers = ['Plan', 'Price', 'Results / run', 'Scheduled', 'Frequency']
    data = []
    for plan in plans.json():
        result = [
            plan['name'].capitalize(),
            integer_cents_to_usd(plan['price'], round=True),
            plan['max_results_per_run'],
            plan['max_scheduled_runs'],
            plan['schedule']['name'].capitalize()
        ]
        data.append(result)
    else:
        tableify(headers=headers, rows=data)


# @cloud.command()
@click.pass_obj
@click.option('--plan', '-p', help="The plan to use (type `soupstars cloud plans` for options)")
@click.option('--billing-cycle', '-b', help="The billing cycle to use. Must be (monthly, annual)")
def upgrade(config, plan, billing_cycle):
    """
    Upgrade or downgrade plans
    """

    if not plan and not billing_cycle:
        print("At least one of `plan` or `billing-cycle` must be set")
        print("Using soupstars cloud upgrade --help for options")
        return

    plan_name = plan.lower()
    available_plans = ('free', 'hobby', 'developer', 'professional', 'enterprise')
    if plan_name not in available_plans:
        print(f"Plan {plan_name} is not valid. Must be one of {available_plans}")

    if billing_cycle == "annual":
        bcd_days = 360
    elif billing_cycle == "monthly":
        bcd_days = 30
    else:
        bcd_days = None

    profile = ProfileResource(config).get().json()
    account = AccountResource(config, account_id=profile['account']['id'])
    resp = account.patch(billing_cycle_duration_days=bcd_days, plan_name=plan_name)
    # Ideally we'd call into `soupstars cloud profile` instead of print this
    jsonify(resp.json())


@cloud.command()
@click.pass_obj
@click.argument('name')
@click.option('--last', '-l', default=1, help="The run to download. last=1 is the most recent, last=2 the second most recent, etc. Defaults to most recent")
@click.option('--save', '-s', help="A file name to save to.")
def download(config, name, last, save):
    """
    Download the results of a parser's run
    """

    archive = ParserArchivesResource(config, name=name, last=last)
    resp = archive.get(stream=True)
    if save:
        with open(save, 'wb') as o:
            for data in resp.iter_lines():
                o.write(data + b'\n')
    else:
        for data in resp.iter_lines():
            print(data.decode('utf8'))


@cloud.command()
@click.argument('name')
@click.pass_obj
@click.pass_context
def run(ctx, config, name):
    """
    Run a parser on Soup Stars cloud
    """

    resp = RunsResource(config).post(parser_name=name)
    if resp.ok:
        ctx.invoke(top)
    else:
        jsonify(resp.json())
