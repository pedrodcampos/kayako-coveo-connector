from kayako.api import KayakoAPIController, extract_params


class KayakoArticles():

    __resource_name__ = 'articles'

    def __init__(self, requests):
        self.__api = KayakoAPIController(self.__resource_name__, requests)

    def get(self, id: int = None, section_id=None, tags: list = None,
            legacy_ids: list = None, fields=None, include=None, **kwargs):

        params = extract_params(locals(), 'id')
        return self.__api.get(id, params=params, **kwargs)
