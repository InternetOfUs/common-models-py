from __future__ import absolute_import, annotations

from json import JSONDecodeError
from unittest import TestCase
from unittest.mock import Mock

import redis

from wenet.storage.cache import RedisCache, InMemoryCache


class MockRedisCache(RedisCache):

    def __init__(self) -> None:
        r = redis.Redis()
        super().__init__(r)


class TestInMemoryCache(TestCase):

    def test_cache_with_id(self):
        cache = InMemoryCache()

        expected_key = "expectedKey"
        expected_value = {
            "key": "value"
        }
        key = cache.cache(expected_value, key=expected_key)

        self.assertEqual(expected_key, key)
        self.assertEqual(cache._cache[expected_key], expected_value)

    def test_cache_without_id(self):
        cache = InMemoryCache()

        expected_key = "expectedKey"
        cache._generate_id = Mock(return_value=expected_key)
        expected_value = {
            "key": "value"
        }
        key = cache.cache(expected_value)

        self.assertEqual(expected_key, key)
        self.assertEqual(cache._cache[expected_key], expected_value)

    def test_get(self):
        cache = InMemoryCache()

        target_key = "key"
        expected_value = {
            "key": "value"
        }
        cache._cache[target_key] = expected_value

        result = cache.get(target_key)

        self.assertEqual(expected_value, result)

    def test_get_non_existing_key(self):
        cache = InMemoryCache()

        result = cache.get("nonExistingKey")

        self.assertEqual(None, result)


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
