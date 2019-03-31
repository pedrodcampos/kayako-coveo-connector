from src.settings import (kayako_api_url, kayako_password, kayako_user,
                        mongodb_database,mongodb_url)

from kayako import KayakoClient
from dependency_injector import providers, containers
from src.mongodb_connector import get_client

database = get_client(mongodb_url, mongodb_database,  3)
kayako_client = KayakoClient(kayako_api_url, auth=(kayako_user, kayako_password))

