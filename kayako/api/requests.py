import requests
import json
import logging
from kayako.api.errors import KayakoAPIError, KayakoError
from kayako.api.session import KayakoSession
from requests.exceptions import ConnectionError, ReadTimeout, RequestException


def request_error_wrapper(f):
    def decorator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ConnectionError as e:
            if isinstance(args[0], KayakoRequests):
                logging.warning('Session was expired. Renewing...')
                args[0].new_session()
                return f(*args, **kwargs)
        except ReadTimeout as e:
            logging.critical('Kayko API Server read timeout.')
            raise KayakoAPIError(e)
        except RequestException as e:
            raise KayakoError
        else:
            raise KayakoError(e)
    return decorator


class KayakoRequests(KayakoSession):
    __default_results_limit__ = 10

    def __init__(self, api_url, auth):
        super().__init__(api_url, auth)

    def __inject_limit_param(self, kwargs):
        if 'params' in kwargs:
            if 'limit' not in kwargs['params']:
                kwargs['params'].update(
                    {'limit':  self.__default_results_limit__})
        else:
            kwargs.update(
                {'params': {'limit': self.__default_results_limit__}})
        return kwargs

    def _parse_response(self,  response, method, target, ** kwargs):
        if type(response["data"]) == dict:
            return response["data"]

        data = response["data"]
        if "next_url" in response:
            offset = response['offset']+self.__default_results_limit__
            kwargs.update({'offset': offset})

            if method == "GET":
                response = self.get(target, ** kwargs)
            elif method == "POST":
                response = self.post(target, ** kwargs)
            data = data + response

        return data

    @request_error_wrapper
    def get(self, target, ** kwargs):

        kwargs = self.__inject_limit_param(kwargs)
        response = super().session.get(target, **kwargs)

        if response.status_code != 200:
            raise KayakoAPIError(response)

        return self._parse_response(response.json(), method='GET', target=target, **kwargs)

    @request_error_wrapper
    def put(self, target, data={}, params={},  ** kwargs):

        response = self.session.put(
            target, data=data, params=params, **kwargs)

        if response.status_code != 200:
            raise KayakoAPIError(response)

        return response.json()

    @request_error_wrapper
    def post(self, target, data={}, params={},  ** kwargs):

        json_data = json.dumps(data)
        response = self.session.post(
            target, data=json_data, params=params, **kwargs)

        if response.status_code != 200:
            raise KayakoAPIError(response)

        return self._parse_response(response.json(), method='POST', target=target, **kwargs)
