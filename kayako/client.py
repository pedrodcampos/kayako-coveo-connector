from kayako.core.errors import KayakoAPIError
from kayako.resources.users import KayakoUsers
from kayako.resources.cases import KayakoCases
from kayako.resources.search import KayakoSearch
from kayako.core.requests import KayakoRequests
from kayako.resources.kre_channel import KayakoKreChannel


class KayakoClient():
    def __init__(self, api_url, auth):
        self.__requests = KayakoRequests(api_url, auth)
        self.users = KayakoUsers(self.__requests)
        self.cases = KayakoCases(self.__requests)
        self.search = KayakoSearch(self.__requests)
        self.kre_channel = KayakoKreChannel(self.__requests)

    @property
    def session(self):
        return self.__requests.user_session
