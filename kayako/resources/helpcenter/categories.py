from kayako.api.endpoint import KayakoEndpoint, extract_params
from kayako.api.requests import KayakoRequests


class KayakoCategories(KayakoEndpoint):

    __endpoint_name__ = 'categories'

    def __init__(self, requests: KayakoRequests):
        super().__init__(requests)

    def get(self, id: int = None, brand_id=None, legacy_ids: list = None):
        params = extract_params(locals(), ignore_keys=['id'])
        return super().get(id, params=params)
