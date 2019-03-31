from kayako.api.endpoint import KayakoEndpoint
from kayako.api.requests import KayakoRequests


class KayakoSearch(KayakoEndpoint):

    __endpoint_name__ = 'search'

    def __init__(self, requests: KayakoRequests):
        self.__endpoint = KayakoEndpoint(self.__endpoint_name__,requests)

    def cases(self, query, fields: None, include: None):
        params = self.__endpoint.bulk_build_params(locals())
        params.update({'query': 'in:conversations '+params['query']})

        url = self.__endpoint.build_url()
        return self.__endpoint.requests.get(url, params)
