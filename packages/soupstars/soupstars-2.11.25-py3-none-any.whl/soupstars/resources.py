import requests

from soupstars.config import Config
from soupstars.json import normalize


class Resource(object):

    def __init__(self, config):
        self.config = config

    def send(self, path, method, **kwargs):
        url = self.config.host + self.route
        headers = {'Authorization': f'jwt {self.config.token}'}
        headers.update(kwargs.get('headers', {}))
        json = normalize(kwargs)
        resp = requests.request(
            url=url,
            method=method,
            headers=headers,
            json=json
        )
        return resp

    def get(self, **kwargs):
        return self.send(self.route, method='GET', **kwargs)

    def post(self, **kwargs):
        return self.send(self.route, method='POST', **kwargs)

    def patch(self, **kwargs):
        return self.send(self.route, method='PATCH', **kwargs)

    def put(self, **kwargs):
        return self.send(self.route, method='PUT', **kwargs)

    def delete(self, **kwargs):
        return self.send(self.route, method='DELETE', **kwargs)


class AuthResource(Resource):
    route = '/auth'

    def post(self, email, password):
        return super().post(email=email, password=password)


class ConfigResource(Resource):
    route = '/config'


class StatusResource(Resource):
    route = '/status'


class UsersResource(Resource):
    route = '/users'

    def post(self, email, password):
        return super().post(email=email, password=password)


class AccountsResource(Resource):
    route = '/accounts'


class AccountResource(Resource):
    route = '/accounts/{account_id}'

    def __init__(self, config, account_id):
        super().__init__(config)
        self.route = self.route.format(account_id=account_id)


class ProfileResource(Resource):
    route = '/profile'


class PlansResource(Resource):
    route = '/plans'


class ParsersResource(Resource):
    route = '/parsers'

    def post(self, name, module):
        return super().post(name=name, module=module)


class ParserResource(Resource):
    route = '/parsers/{parser_name}'

    def __init__(self, config, name):
        super().__init__(config)
        self.route = self.route.format(parser_name=name)


class RunsResource(Resource):
    route = '/runs'

    def post(self, parser_name):
        return super().post(parser_name=parser_name)


class RunsLogResource(Resource):
    route = '/runs/{run_id}/logs'

    def __init__(self, config, run_id):
        super().__init__(config)
        self.run_id = run_id
        self.route = self.route.format(run_id=run_id)

    def post(self, created_at, message, **kwargs):
        return super().post(created_at=created_at, message=message, **kwargs)


class RunResource(Resource):
    route = '/runs/{run_id}'

    def __init__(self, config, run_id):
        super().__init__(config)
        self.route = self.route.format(run_id=run_id)


class ResultsResource(Resource):
    route = '/results'

    def post(self, run_id, parser_id, status_code, url, data, errors):
        return super().post(run_id=run_id, parser_id=parser_id,
                         status_code=status_code, url=url, data=data,
                         errors=errors)


class InstancesResource(Resource):
    route = '/instances'


class TopResource(Resource):
    route = '/top'


class ParserArchivesResource(Resource):
    route = '/parsers/{parser_name}/archives'

    def __init__(self, config, name, last):
        super().__init__(config)
        self.route = self.route.format(parser_name=name)

    def get(self, stream=True):
        return super().get(headers={'accept': 'text/csv'})
