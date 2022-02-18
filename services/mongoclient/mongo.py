from pymongo import MongoClient
from utils.wxlogger import WxLogger
from settings.setting import Settings
from logging import Logger
from utils.exceptions import SystemExitException


class MongoDBClient:
    """
    MongoClient Object and it's methods
    """
    logger: Logger = None
    client: MongoClient = None
    db = None

    def __init__(self, config: Settings):

        if self.__class__.logger is None:
            self.__class__.logger = WxLogger(__name__).getLogger()
        try:
            if MongoDBClient.client is None:
                self.__class__.client = MongoClient(host=config.MONGODB_URL)
                self.ping()
                self.__class__.logger.info('MongoDB connected')
            else:
                MongoDBClient.logger.info('MongoDB already connected')
            if MongoDBClient.db is None:
                MongoDBClient.logger.info(f'MongoDB {config.MONGODB_NAME}')
                MongoDBClient.db = MongoDBClient.client[config.MONGODB_NAME]
        except Exception as ex:
            raise SystemExitException(message="MongoDB Connection Issue!")

    def ping(self):
        self.__class__.logger.info(MongoDBClient.client.db_name.command('ping'))

    def collections(self):
        if self.__class__.db is not None:
            self.__class__.logger.info(self.__class__.db.list_collection_names())
        else:
            raise SystemExitException(message="MongoDB not Set!")

    @staticmethod
    def get_client():
        """
        :return: MongoClient object
        :rtype:
        """
        return MongoDBClient.client

    @staticmethod
    def find_one(collection, query={}):
        """
        Given the DB find one
        :param collection:
        :type collection:
        :return:
        :rtype:
        """
        try:
            return MongoDBClient.db[collection].find_one(filter=query)
        except Exception as ex:
            raise ex

    def get_data(self, collection, filter=None, projection=None, skip=0, limit=0, sort=None):
        """
        Fetch data from mongo based on the query
        :param filter: mongo query
        :return: array of docs
        """
        docs = []
        try:
            collection = MongoDBClient.db[collection]
            cursor = collection.find(filter=filter, projection=projection, skip=skip, limit=limit, sort=sort)
            for document in cursor:
                docs.append(document)
            return docs
        except Exception as ex:
            MongoDBClient.logger.error(ex)
            return False
