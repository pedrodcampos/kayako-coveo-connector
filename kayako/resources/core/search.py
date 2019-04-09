from kayako.api import KayakoAPIController, KayakoRequests, extract_params


class KayakoSearch():

    __resource_name__ = 'search'

    def __init__(self, requests: KayakoRequests):
        self.__api = KayakoAPIController(self.__resource_name__, requests)

    def cases(self, query, fields: None, include: None):
        params = extract_params(locals())
        params.update({'query': 'in:conversations '+params['query']})
        params.pop('query')

        return self.__api.get(params=params)
