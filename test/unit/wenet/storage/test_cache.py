from __future__ import absolute_import, annotations

from json import JSONDecodeError
from unittest import TestCase
from unittest.mock import Mock

import redis

from wenet.storage.cache import RedisCache


class MockRedisCache(RedisCache):

    def __init__(self) -> None:
        r = redis.Redis()
        super().__init__(r)


class TestRedisCache(TestCase):

    def test_cache_with_id(self):
        cache = MockRedisCache()
        cache._set = Mock(return_value=None)

        expected_key = "expectedKey"
        key = cache.cache({}, key=expected_key)

        self.assertEqual(expected_key, key)

    def test_cache_without_id(self):
        cache = MockRedisCache()
        cache._set = Mock(return_value=None)

        expected_key = "expectedKey"
        cache._generate_id = Mock(return_value=expected_key)

        key = cache.cache({})

        self.assertEqual(expected_key, key)

    def test_get(self):
        cache = MockRedisCache()
        cache._get = Mock(return_value="{}")

        result = cache.get("key")

        self.assertEqual({}, result)

    def test_get_non_existing_key(self):
        cache = MockRedisCache()
        cache._get = Mock(return_value=None)

        result = cache.get("nonExistingKey")

        self.assertEqual(None, result)

    def test_get_malformed_data(self):
        cache = MockRedisCache()
        cache._get = Mock(return_value="notAJson")

        with self.assertRaises(JSONDecodeError):
            cache.get("key")
