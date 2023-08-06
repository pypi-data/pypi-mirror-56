""" Constructing the body of response, depending of input params. """

from ._version import _version_ctx


def _construct_data(
        data: (str, list, dict),
        kind: str = None,
        next_link: str = None,
        previous_link: str = None) -> dict:
    res = {}

    if kind is not None:
        if not isinstance(kind, str):
            raise TypeError('kind field must have an str type')
        res['kind'] = kind

    if isinstance(data, list):
        res['currentItemCount'] = len(data)
        res['items'] = data
    elif isinstance(data, dict):
        res.update(data)

    if next_link is not None:
        if not isinstance(kind, str):
            raise TypeError('kind field must have an str type')
        res['nextLink'] = next_link

    if previous_link is not None:
        res['previousLink'] = previous_link

    return res


def _construct_error(errors: (str, list, Exception), status_code: int) -> dict:
    if not isinstance(errors, list):
        errors = [errors]
    # Convert all Exceptions to strings representation.
    errors = list(map(str, errors))
    res = {'code': status_code}
    res['message'] = errors[0]
    res['errors'] = []
    for error in errors:
        res['errors'].append({"message": error})
    return res


def get_google_body(
        data='',
        kind: str = None,
        errors=None,
        next_link: str = None,
        status: int = 200
    ):
    body = {
        "apiVersion": _version_ctx.value,
    }

    if errors:
        body['error'] = _construct_error(errors, status)
    else:
        data = _construct_data(data, kind, next_link)
        body['data'] = data

    return body
