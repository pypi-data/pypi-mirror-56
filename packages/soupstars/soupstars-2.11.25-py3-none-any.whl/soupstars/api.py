"""
API
===

Entrypoints for some of the functionality exposed by the package
"""

from soupstars.runners import Runner
from soupstars.loaders import Loader
from soupstars.parsers import BeautifulSoupStar, Url


def run(parser, **kwargs):
    """
    Executes a parser, returning the data from the run
    """

    return Runner(parser, **kwargs).run()


def fetch(url) -> BeautifulSoupStar:
    """
    Downloads a url and converts it into a BeautifulSoupStars object
    """

    loader = Loader()
    load = loader.load(url)
    soup = BeautifulSoupStar(load)
    return soup


def parse(parser, url):
    """
    Download a url and process it with a parser, returning the data and links
    discovered by the parsers
    """

    loader = Loader()
    load = loader.load(url)
    data, links = parser.parse(load)
    return data, links
