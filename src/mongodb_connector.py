import pymongo
import logging


def get_client(url, database, retries):
    def do_get():
        try:
            mongo_client = pymongo.MongoClient(url)
            logging.info('Connecting to mongdb')
            mongo_client.server_info()
            logging.info('Connected')
            return mongo_client[database]
        except pymongo.errors.ServerSelectionTimeoutError:
            logging.critical('mongodb connection timedout')
            return None
    while retries > 0:
        db = do_get()
        if db != None:
            return db
        retries -= 1
        logging.warning(f'Remaining attempts: {retries}')

    raise SystemExit('Could not connect to mongodb.')
