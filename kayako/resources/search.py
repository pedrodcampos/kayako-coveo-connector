from kayako.core.endpoint import KayakoEndpoint
from kayako.core.requests import KayakoRequests


class KayakoSearch(KayakoEndpoint):

    __resource_endpoint__ = 'search'

    def __init__(self, requests: KayakoRequests):
        super().__init__(requests)

    def cases(self, query, fields: None, include: None):
        params = self._bulk_build_params(locals())
        params.update({'query': 'in:conversations '+params['query']})

        url = self._build_url()
        return self._requests.get(url, params)
