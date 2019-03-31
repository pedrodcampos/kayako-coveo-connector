from kayako.core.parser import KayakoParser
from requests.exceptions import ConnectionError


class KayakoError(Exception):
    pass


class KayakoAPIError(KayakoError):

    class KayakoAPIErrorList(list):
        class KayakoAPIErrorItem(KayakoParser):
            pass

        def __init__(self, error_items):
            error_items = [self.KayakoAPIErrorItem(item)
                           for item in error_items]
            super().__init__(error_items)

    def __init__(self, response):
        if response.headers['Content-Type'] == 'application/json':
            __json_response = response.json()
            self.errors = self.KayakoAPIErrorList(__json_response['errors'])
            self.status_code = __json_response['status']
            super().__init__(
                f'[CODE: {self.status_code}] {self.errors[0].code}')
        elif 'text/html' in response.headers['Content-Type']:
            super().__init__(response.text)
        else:
            self.raw_response = response
            super().__init__('Unkown errorr. Check raw response.')
