""" VersionContext is used to pass api_version into responses. """


class VersionContext():
    def __init__(self, value):
        self.value = value


_version_ctx = VersionContext('0.1.0')


def set_api_version(version: str):
    _version_ctx.value = version
