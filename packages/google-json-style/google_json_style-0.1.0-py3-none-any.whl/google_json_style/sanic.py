from sanic.response import json

from ._google import get_google_body


def json_resp(data = '', status: int = 200, *args, **kwargs):
    return json(get_google_body(data, status=status, *args, **kwargs))
