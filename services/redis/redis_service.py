from json import dumps
from json import loads
from typing import Any
from typing import Dict

from redis import Redis

from globals.utils import WxLogger


class RedisService:
    """RedisService to use across project.

    Inject the redis client required.
    """

    _logger = None

    def __init__(self, client: Redis, name: str = None):
        if not name:
            name = __name__
        if not RedisService._logger:
            RedisService._logger = WxLogger(name).getLogger()
        RedisService._logger.debug(f"Redis Service initialized")
        self.client = client

    def ping(self):
        return self.client.ping()

    def set_key(self, key, payload: Any):
        """Set payload against key.

        :param key: Key
        :param payload:
        :return:
        """
        if type(payload) == dict:
            return self.client.set(key, dumps(payload, ensure_ascii=False))
        if type(payload) == str:
            return self.client.set(key, payload)
        return False

    def set_with_expiration(self, key: str, payload: Any, exp: int):
        """Set payload against key with expiration in seconds.

        :param key: Key
        :param payload:
        :param exp:
        :return:
        """
        if type(payload) == dict:
            return self.client.setex(key, exp, dumps(payload, ensure_ascii=False))
        if type(payload) == str:
            return self.client.setex(key, exp, payload)
        return False

    def get(self, key: str) -> Any:
        """Get payload against key.

        :param key: Key
        :return:
        """
        try:
            item = self.client.get(key)
            if "{" in item.decode("utf-8"):
                return loads(item.decode("utf-8"))
            return item
        except Exception:
            return False

    def is_exists(self, key: str) -> bool:
        """Check if payload exists against key.

        :param key: Key
        :return:
        """
        return self.client.exists(key) == 1

    def expire_key_in(self, key: str, exp_in: int):
        """Updates expire time in seconds of a key.

        :param key: Key
        :param exp_in: Time in seconds
        :return:
        """
        return self.client.expire(key, exp_in)

    def bulk_insert_with_ex(
        self,
        data: Dict,
        exp: int = 36000,
    ):
        """Bulk insert with expiration.

        :param data:
        :param exp:
        :return:
        """
        pipeline = self.client.pipeline()
        for k in data.keys():
            if type(data[k]) == dict:
                data[k] = dumps(data[k], ensure_ascii=False)

            pipeline.setex(k, exp, data[k])

        pipeline.execute()

    def bulk_insert_hmset_expiration(self, hash_namespace, data: Dict, exp: int = 3600):
        """Achieves HMSET with expiration using setx.

        :param hash_namespace:
        :param data:
        :param exp:
        :return:
        """
        pipeline = self.client.pipeline()

        for k in data.keys():
            if type(data[k]) == dict:
                data[k] = dumps(data[k], ensure_ascii=False)

            pipeline.setex(f"{hash_namespace}__{k}", exp, data[k])

        pipeline.execute()

    def get_hget(self, hash_namespace, key):
        """Get value by namespace and key custom as hget via get.

        :param hash_namespace:
        :param key:
        :return:
        """
        try:
            item = self.client.get(f"{hash_namespace}_{key}")
            if "{" in item.decode("utf-8"):
                return loads(item.decode("utf-8"))
            return item
        except Exception:
            return False

    def bulk_insert_hmset(self, hash_namespace, data: Dict):
        """HMSET Redis via hset.

        :param hash_namespace:
        :param data:
        :return:
        """
        # pipeline = self.client.pipeline()
        # data = data.copy()
        for k, v in data.items():
            if type(data[k]) == dict:
                data[k] = dumps(data[k], ensure_ascii=False)

        return self.client.hset(hash_namespace, mapping=data)

    def hget(self, hash_namespace, keys: str):
        """HMGET Redis.

        :param hash_namespace:
        :param keys:
        :return:
        """
        return self.client.hget(hash_namespace, keys)

    def delete(self, key: str):
        """Delete a given key.

        :param key: redis key
        :return:
        """
        return self.client.delete(key)
