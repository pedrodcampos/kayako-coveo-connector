from kayako.api import KayakoAPIController, KayakoRequests, extract_params


class KayakoSections():

    __resource_name__ = 'sections'

    def __init__(self, requests: KayakoRequests):
        self.__api = KayakoAPIController(self.__resource_name__, requests)

    def get(self, id: int = None, category_ids: list = None,
            legacy_ids: list = None, fields=None, include=None):
        params = extract_params(locals(), ignore_keys=['id'])
        return self.__api.get(id, params=params)
