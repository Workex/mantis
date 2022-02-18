from elasticsearch import Elasticsearch

from utils.exceptions import SystemExitException
from utils.wxlogger import WxLogger
from settings.setting import Settings
from logging import Logger

"""
Creating ELastic Client
"""


class ElasticClient:
    """Elastic Client Class."""

    logger: Logger = None
    _client: Elasticsearch = None

    @property
    def client(self):
        self.__class__.logger.debug("Giving Elastic Client")
        return self.__class__._client

    @client.setter
    def client(self, value: Elasticsearch):
        self.__class__.logger.info("Trying to set Elastic client")
        if type(value) == Elasticsearch and not self.__class__._client:
            self.__class__._client = value
        else:
            raise SystemExitException(message="Elastic Configuration Issue")

    def __init__(self, config: Settings):
        """Constructor Function."""
        if not self.__class__.logger:
            self.__class__.logger = WxLogger(__name__).getLogger()

        if not self.__class__._client:
            self.__class__.logger.info("Initialization Elastic Client")
            self.__class__._client = Elasticsearch(hosts=config.ELASTICSEARCH_HOSTS)
            response = self.__class__._client.cat.indices(index='*', h='index', s='index:desc')
            print(response)
            self.__class__.logger.debug("*" * 40)
            self.__class__.logger.info(
                f"Elastic Connected: {self.__class__._client.ping()}",
            )
            self.__class__.logger.debug("*" * 40)
        else:
            self.__class__.logger.debug("Elastic client Already Configured")
