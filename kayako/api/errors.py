from kayako.api.objects import KayakoObject
from requests.exceptions import ConnectionError


class KayakoError(Exception):
    pass


class KayakoAPIError(KayakoError):

    def __init__(self, response):
        super().__init__(response.text)
        self.raw_response = response
        if response.headers['Content-Type'] == 'application/json':
            __json_response = response.json()
            self.status_code = __json_response['status']
