import requests
import json
import logging
from kayako.core.errors import KayakoAPIError, KayakoError
from kayako.core.parsers.user_session import KayakoUserSession
from requests.exceptions import ConnectionError, ReadTimeout, RequestException


def request_error_wrapper(f):
    def decorator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ConnectionError as e:
            if isinstance(args[0], KayakoRequests):
                logging.warning('Session was expired. Renewing...')
                args[0]._KayakoRequests__new_session()
                return f(*args, **kwargs)
        except ReadTimeout as e:
            logging.critical('Kayko API Server read timeout.')
            raise KayakoAPIError(e)
        except RequestException as e:
            raise KayakoError
        else:
            raise KayakoError(e)
    return decorator


class KayakoSession():
    __session_endpoint__ = 'session'

    def __init__(self, api_url, auth):
        self.__api_url = api_url
        self.__auth = auth
        self.__session = None
        self.__user_session = None
        self.new_session()

    @property
    def api_url(self):
        return self.__api_url

    @property
    def user_session(self):
        return self.__user_session

    @property
    def session(self):
        return self.__session

    def __update_session_headers(self):
        self.__session.headers.update(
            {'X-Session-ID': self.user_session.id})

    def new_session(self):
        session = requests.Session()
        session.headers.update({
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json',
            'User-Agent': 'Kayako Bot/1.0',
            'X-CSRF': 'false',
        })
        self.__session = session
        self.__user_session = self.__get_user_session(self.__auth)
        self.__update_session_headers()

    def __get_user_session(self, auth):
        session_url = '/'.join([self.__api_url, self.__session_endpoint__])
        response = self.session.get(session_url, auth=auth).json()
        session = KayakoUserSession(response['data'])
        return session
