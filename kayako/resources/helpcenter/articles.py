from kayako.api.endpoint import KayakoEndpoint, extract_params
from kayako.api.requests import KayakoRequests


class KayakoArticles(KayakoEndpoint):

    __endpoint_name__ = 'articles'

    def __init__(self, requests: KayakoRequests):
        super().__init__(requests)

    def get(self, id: int = None, section_id=None, tags: list = None,
            legacy_ids: list = None, fields=None, include=None, **kwargs):

        params = extract_params(locals(), 'id')
        return super().get(id, params=params, **kwargs)
