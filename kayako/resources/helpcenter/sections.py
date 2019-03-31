from kayako.api.endpoint import KayakoEndpoint
from kayako.api.requests import KayakoRequests, extract_params


class KayakoSections(KayakoEndpoint):

    __endpoint_name__ = 'sections'

    def __init__(self, requests: KayakoRequests):
        super().__init__(requests)

    def get(self, id: int = None, category_ids: list = None,
            legacy_ids: list = None, fields=None, include=None):
        params = extract_params(locals(), ignore_keys=['id'])
        return super().get(id, params=params)
