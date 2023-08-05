"""
Writers control where the results of crawls are stored.
"""

import csv
import importlib
import json
import os
import io
import datetime as dt

from soupstars.resources import ResultsResource
from soupstars.config import Config


class Writer(object):

    @classmethod
    def from_string(klass, string, url=None):
        class_name = f"{string.capitalize()}Writer"
        module = importlib.import_module('soupstars.writers')
        _Writer = getattr(module, class_name)
        return _Writer(url=url)

    def __init__(self, url=None):
        self.url = url

    def flush(self):
        pass


# I think we could do a TextWriter that optionally logs to the current direcfory
# or the soupstars home directory
class JsonWriter(Writer):
    def write(self, result):
        with open(self.url, 'a') as o:
            json.dump(result, o)
            o.write('\n')


class CsvWriter(Writer):
    def flatten(self, result):
        _result = {}
        errors = {f'{k}_error': v for k, v in result['errors'].items()}
        data = {k: str(v) for k, v in result['data'].items()}
        _result.update(url=result['url'])
        _result.update(status_code=result['status_code'])
        _result.update(data)
        _result.update(errors)
        return _result

    def write(self, result, buffer=None):
        with open(self.url, 'a') as o:
            result = self.flatten(result)
            _writer = csv.DictWriter(o, fieldnames=result.keys(), delimiter='\t')
            if o.tell() == 0:
                _writer.writeheader()
            _writer.writerow(result)


class S3Writer(CsvWriter):
    def __init__(self, bucket, key, client):
        self.key = key
        self.bucket = bucket
        self.client = client
        self.buffer = io.StringIO()
        self.url = f"{bucket}/{key}"

    def flush(self):
        return self.client.put_object(Bucket=self.bucket, Body=self.buffer.getvalue().encode('utf8'), Key=self.key)

    def write(self, result, created_at=None):
        created_at = created_at or dt.datetime.now()
        result = self.flatten(result)
        result['created_at'] = created_at
        _writer = csv.DictWriter(self.buffer, fieldnames=result.keys(), delimiter='\t')
        if self.buffer.tell() == 0:
            _writer.writeheader()
        _writer.writerow(result)


class CloudWriter(Writer):

    def __init__(self, run_id, parser_id, host=None, token=None):
        self.parser_id = parser_id
        self.run_id = run_id
        self.config = Config(host=host, token=token)
        self.resource = ResultsResource(config=self.config)
        self.url = self.config.host

    def write(self, result):
        return self.resource.post(
            run_id=self.run_id,
            parser_id=self.parser_id,
            data=result['data'],
            url=result['url'],
            status_code=result['status_code'],
            errors=result['errors']
        )
