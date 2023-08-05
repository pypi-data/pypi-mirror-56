# Soup Stars :stew: :star: :boom:

[![Build Status](https://travis-ci.org/soupstars/soupstars.svg?branch=master)](https://travis-ci.org/soupstars/soupstars)
<!-- [![Coverage Status](https://coveralls.io/repos/github/tjwaterman99/soupstars/badge.svg?branch=master)](https://coveralls.io/github/tjwaterman99/soupstars?branch=master) -->
<!-- [![Docs](https://readthedocs.org/projects/soupstars/badge/?version=latest)](https://soupstars.readthedocs.io/en/latest/?badge=latest) -->
[![Version](https://badge.fury.io/py/soupstars.svg)](https://badge.fury.io/py/soupstars)
[![Python](https://img.shields.io/pypi/pyversions/soupstars.svg)](https://pypi.org/project/soupstars/)

Soup Stars is a framework for building web parsers with Python. It is designed to make building, deploying, and scheduling web parsers easier by simplifying what you need to get started.

## Quickstart

```
pip install soupstars
```

### Creating a parser

New parsers are created by typing `soupstars create` into a terminal, and supplying the name of a python module.

```
soupstars create myparser.py
```

Soup Stars will use a template parser to help you get started. This example creates a parser that extracts headlines from articles on the New York Times website.

```python
from soupstars import data, follow

url = "https://www.nytimes.com"

@follow
def follow(url):
    return (url.domain == "www.nytimes.com") and (url.match("\d{4}\/\d{2}\/\d{2}"))

@parse
def h1(soup):
    return soup.h1.text
```

You can test that the parser functions correctly.

```
soupstars run myparser
```

Use `soupstars --help` to see a full list of available commands.

More documentation is available [here](http://soupstars-docs.s3-website-us-west-2.amazonaws.com/).

## Development

Start the docker services.

```
docker-compose up -d
```

Set up the containers.

```
docker-compose exec web flask s3 mb soupstars-archive
docker-compose exec web flask db upgrade
docker-compose exec web flask seed schedules
docker-compose exec web flask seed plans
docker-compose exec web flask seed user
docker-compose exec web flask seed parsers
```

Run the tests.

```
docker-compose run --rm client pytest -vs
```

## Releasing

New tags that pass on CI will automatically be pushed to docker hub.

To deploy to PyPI requires manually running the following commands.

```
pip3 install twine
python3 setup.py sdist bdist_wheel
twine upload dist/*
```
