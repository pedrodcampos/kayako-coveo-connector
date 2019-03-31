from kayako.api.requests import KayakoRequests


class KayakoEndpointHelper():

    def __init__(self, resource_name, requests: KayakoRequests):
        self.requests = requests
        self.__resource_endpoint__ = resource_name

    def build_url(self, args):
        parts = [self.requests.api_url, self.__resource_endpoint__] + \
            [str(arg) for arg in list(args) if arg]
        return '/'.join(parts)

    def clean_kwargs(self, kwargs):
        return {key: value for key, value in kwargs.items() if value}


class KayakoEndpoint():

    __endpoint_name__ = ''

    def __init__(self, requests: KayakoRequests):
        self.__endpoint = KayakoEndpointHelper(
            self.__endpoint_name__, requests)

    def __prepare_args(self, url_args, kwargs):
        url = self.__endpoint.build_url(url_args)
        kwargs = self.__endpoint.clean_kwargs(kwargs)
        return (url, kwargs)

    def get(self, *url_args, **kwargs):
        url, kwargs = self.__prepare_args(url_args, kwargs)
        return self.__endpoint.requests.get(url, **kwargs)

    def put(self, *url_args, **kwargs):
        url, kwargs = self.__prepare_args(url_args, kwargs)
        return self.__endpoint.requests.put(url, **kwargs)

    def post(self, *url_args, **kwargs):
        url, kwargs = self.__prepare_args(url_args, kwargs)
        return self.__endpoint.requests.get(url, **kwargs)
