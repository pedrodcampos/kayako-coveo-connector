
from kayako.api.requests import KayakoRequests
from kayako.resources.core import KayakoUsers  # , KayakoCases, KayakoSearch
from kayako.resources.helpcenter import KayakoHelpcenter
from kayako.resources.core import KayakoInsights
#from kayako.resources.realtime_channel import KayakoKreChannel


class KayakoClient():
    def __init__(self, api_url, auth):
        self.__requests = KayakoRequests(api_url, auth)
        self.users = KayakoUsers(self.__requests)
 #       self.cases = KayakoCases(self.__requests)
 #       self.search = KayakoSearch(self.__requests)
        self.helpcenter = KayakoHelpcenter(self.__requests)
 #       self.kre_channel = KayakoKreChannel(self.__requests)
        self.insights = KayakoInsights(self.__requests)

    @property
    def session(self):
        return self.__requests.user_session
