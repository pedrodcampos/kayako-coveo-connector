from kayako.api import KayakoAPIController, extract_params, KayakoRequests


class KayakoCategories():

    __resource_name__ = 'categories'

    def __init__(self, requests: KayakoRequests):
        self.__api = KayakoAPIController(self.__resource_name__, requests)

    def get(self, id: int = None, brand_id=None, legacy_ids: list = None):
        params = extract_params(locals(), ignore_keys=['id'])
        return self.__api.get(id, params=params)
