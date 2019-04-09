from kayako.api import KayakoAPIController, KayakoRequests, extract_params


class KayakoInsightsHelpcenter():
    def __init__(self, articles_func, search_func):
        self.__articles = articles_func
        self.__search = search_func

    @property
    def articles(self, fields=None, include=None):
        def func(**kwargs):
            return self.__articles(**kwargs)
        return func

    @property
    def search(self, start_at, end_at, fields=None, include=None):
        def func(**kwargs):
            return self.__search(**kwargs)
        return func


class KayakoInsights():

    __resource_name__ = 'insights'
    __helpcenter_path__ = 'helpcenter'
    __articles_path__ = 'articles'
    __search_path__ = 'search'

    def __init__(self, requests: KayakoRequests):
        self.__api = KayakoAPIController(self.__resource_name__, requests)
        self.__helpcenter = KayakoInsightsHelpcenter(
            self.__helpcenter_articles, self.__helpcenter_search)

    @property
    def helpcenter(self):
        return self.__helpcenter

    def __helpcenter_articles(self, **kwargs):
        params = extract_params(kwargs)
        return self.__api.get(self.__helpcenter_path__, self.__articles_path__, params=params)

    def __helpcenter_search(self, *args, **kwargs):
        params = extract_params(locals())
        return self.__api.get(self.__helpcenter_path__, self.__search_path__, params=params)
