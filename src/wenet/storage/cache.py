from __future__ import absolute_import, annotations

import json
import logging
import os
import uuid
from abc import ABC
from json import JSONDecodeError
from typing import Optional

import redis

logger = logging.getLogger("wenet.storage.cache")


class BaseCache(ABC):

    def cache(self, data: dict, key: Optional[str] = None, **kwargs) -> str:
        """
        Cache data in dictionary format.

        :param dict data: the data to cache
        :param key: the key to save the data
        :return: the identifier associated to the data entry
        """
        pass

    def get(self, key: str) -> Optional[dict]:
        """
        Get cached data associated to the specified key.

        :param str key: the data key
        :return: the requested data, if it exists
        """
        pass


class RedisCache(BaseCache):
    """
    Cache allows to store data in Redis.
    Cached data will only be available for a limited and specified amount of time.
    """

    def __init__(self, r: redis.Redis) -> None:
        self._r = r

    def cache(self, data: dict, key: Optional[str] = None, **kwargs) -> str:
        """
        Cache data in dictionary format.

        Among the kwargs:

        * ttl: the time to live of the data entry (expressed in seconds)

        :param dict data: the data to cache
        :param key: the key to save the data
        :return: the identifier associated to the data entry
        """
        if key is None:
            key = str(uuid.uuid4())

        logger.debug(f"Caching data for key [{key}] and ttl [{kwargs.get('ttl')}]")
        if kwargs.get("ttl") is not None:
            self._r.set(key, json.dumps(data), ex=kwargs.get("ttl"))
        else:
            self._r.set(key, json.dumps(data))
        return key

    def get(self, key: str) -> Optional[dict]:
        logger.debug(f"Getting cached data for key [{key}]")
        result = self._r.get(key)
        if result is not None:
            try:
                result = json.loads(result)
            except JSONDecodeError as e:
                logger.exception(f"Could not parse cached data for key [{key}]", exc_info=e)
        else:
            logger.debug(f"No data for key [{key}]")

        return result

    @staticmethod
    def _build_redis_from_env() -> redis.Redis:
        """
        Build the Redis connection using environment variables.

        Required environment variables are:
          - REDIS_HOST - default to 'localhost'
          - REDIS_PORT - default to '6379'
          - REDIS_DB - default to '0'

        :return: the redis connection
        """
        return redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0))
        )

    @staticmethod
    def build_from_env() -> RedisCache:
        """
        Build the Redis cache using environment variables.

        Required environment variables are:
          - REDIS_HOST - default to 'localhost'
          - REDIS_PORT - default to '6379'
          - REDIS_DB - default to '0'

        :return: the redis cache
        """
        r = RedisCache._build_redis_from_env()
        return RedisCache(r)
