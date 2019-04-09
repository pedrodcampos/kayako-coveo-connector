from kayako.api.requests import KayakoRequests


def extract_params(args, ignore_keys=[]):
    ignore_keys.append('self')
    return {key: value for key, value in args.items() if key not in ignore_keys and '__' not in key}


class KayakoAPIHelper():

    def __init__(self, resource_name, requests: KayakoRequests):
        self.requests = requests
        self.__resource_endpoint__ = resource_name


class KayakoAPIController():

    __resource_name__ = ''

    def __init__(self, resource_name, requests: KayakoRequests):
        self.__resource_name__ = resource_name
        self.__requests = requests

    def __build_url(self, args):
        parts = [self.__requests.api_url, self.__resource_name__] + \
            [str(arg) for arg in list(args) if arg]
        return '/'.join(parts)

    def __clean_kwargs(self, kwargs):
        return {key: value for key, value in kwargs.items() if value}

    def __prepare_args(self, url_args, kwargs):
        url = self.__build_url(url_args)
        kwargs = self.__clean_kwargs(kwargs)
        return (url, kwargs)

    def get(self, *url_args, **kwargs):
        url, kwargs = self.__prepare_args(url_args, kwargs)
        return self.__requests.get(url, **kwargs)

    def put(self, *url_args, **kwargs):
        url, kwargs = self.__prepare_args(url_args, kwargs)
        return self.__requests.requests.put(url, **kwargs)

    def post(self, *url_args, **kwargs):
        url, kwargs = self.__prepare_args(url_args, kwargs)
        return self.__requests.requests.get(url, **kwargs)
