from .redis_service import RedisService
from globals.services.project.redis.client import RedisClient


#
def get_redis(name: str = None) -> RedisService:
    """Gives new redis service.

    :param name:
    :return:RedisService
    """
    redis_client = RedisClient().client
    return RedisService(redis_client, name)


__all__ = [
    "get_redis",
    "RedisService",
]
