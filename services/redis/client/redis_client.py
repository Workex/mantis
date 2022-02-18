import redis

from globals.exceptions import ValidationException
from globals.utils import WxLogger
from wx_hrms import settings


class RedisClient:
    _client: redis.Redis = None
    logger = None
    client_name = __name__

    @property
    def client(self):
        RedisClient.logger.debug("Giving Redis Client")
        return RedisClient._client

    @client.setter
    def client(self, value: redis.Redis):
        RedisClient.logger.info("Trying to set Redis client")
        if type(value) == redis.Redis and not RedisClient._client:
            RedisClient._client = value
        else:
            RedisClient.logger.error("RedisClient Already Set or Error!")
            raise ValidationException(message="Redis Configuration Issue")

    def __init__(self):
        if not RedisClient.logger:
            RedisClient.logger = WxLogger(__name__).getLogger()

        if not RedisClient._client:
            RedisClient._client = redis.Redis(
                host=settings.REDIS.get("HOST"),
                port=settings.REDIS.get("PORT"),
            )
            RedisClient.logger.info("Initialization Redis Client")
        else:
            RedisClient.logger.debug("Redis Client Already Configured!")
