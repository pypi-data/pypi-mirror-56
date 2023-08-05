import click
import os
import sys
import pkg_resources

from soupstars.api import fetch, run as _run
from soupstars.loaders import Loader
from soupstars.parsers import Parser, BeautifulSoupStar, Url
from soupstars.version import __version__
from soupstars.config import Config
from soupstars.cli.printers import jsonify


@click.group()
def base():
    """
    CLI for managing Soup Stars parsers
    """

    if '.' not in sys.path:
        sys.path.append('.')


@base.command()
def config():
    """
    Print the configuration used by the client
    """

    data = {
        "soupstars": {
            "version": __version__,
            "path": pkg_resources.require('soupstars')[0].module_path
        },
        "python": {
            "version": f"{sys.version})".replace('\n', ''),
            "path": sys.executable,
        },
        "config": Config().to_dict()
    }

    jsonify(data)


@base.command()
@click.argument('parser')
@click.option('--url', '-u', required=False, help="Url to parse")
def debug(parser, url):
    """
    Open a python prompt with a parser result
    """

    parser = Parser.from_string(parser)

    if url:
        url = Url(url)
        parser.module.url = url
    else:
        url = parser.seeds()[0]

    soup = fetch(url)
    response = soup.response
    request = soup.request

    result, links = parser.parse(response)
    data = result['data']
    errors = result['errors']
    status_code = result['status_code']

    del(result)

    try:
        import IPython
        IPython.embed(colors="neutral")
    except ImportError:
        import code
        code.InteractiveConsole(locals=vars()).interact()


@base.command()
@click.argument('name')
@click.option('--template', '-t', required=False, default='nytimes', help="Name of the template to use. Default is `nytimes`")
@click.option('--force/--no-force', default=False, help="Overwrite an existing file")
def create(name, template, force):
    """
    Create a new parser from a template
    """

    parser = Parser.from_string(f'soupstars.examples.{template}')
    text = open(parser.module.__file__, 'r').read()
    if os.path.exists(name) and not force:
        raise FileExistsError(
            f"{name} already exists. Use --force to overwrite."
        )
    with open(name, 'w') as o:
        o.write(text)
        jsonify({"state": "done", "parser": name})


@base.command()
@click.argument('parser')
@click.option('--limit', '-l', required=False, default=100, help="Number of results to parse")
def run(parser, limit):
    """
    Run a parser
    """

    _run(parser, max_results=limit)
