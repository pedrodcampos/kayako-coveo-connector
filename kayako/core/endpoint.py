from kayako.core.requests import KayakoRequests
from kayako.core.errors import KayakoError


class KayakoEndpoint():
    __resource_endpoint__ = ""

    def __init__(self, requests: KayakoRequests):
        self._requests = requests

    def _build_url(self, *args):
        parts = [self._requests.api_url, self.__resource_endpoint__] + \
            [str(arg) for arg in list(args) if arg]
        return '/'.join(parts)

    def _bulk_build_params(self, params: dict, keys_to_ignore: list = None):
        ignore_list = ['self'] + (keys_to_ignore or [])
        return {key: value
                if type(value) != list else ','.join(map(str, value))
                for key, value in params.items()
                if value and key not in ignore_list}
