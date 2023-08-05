import json as _json


class JSONEncoder(_json.JSONEncoder):
    def default(self, o):
        return str(o)


def dumps(obj, **kwargs):
    return _json.dumps(obj, cls=JSONEncoder, **kwargs)


def normalize(dict):
    encoded = dumps(dict)
    decoded = _json.loads(encoded)
    return decoded
