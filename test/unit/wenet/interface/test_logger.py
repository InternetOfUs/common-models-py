from __future__ import absolute_import, annotations

from unittest import TestCase
from unittest.mock import Mock

from test.unit.wenet.interface.mock.client import MockApikeyClient
from test.unit.wenet.interface.mock.response import MockResponse
from wenet.interface.exceptions import AuthenticationException, CreationError
from wenet.interface.logger import LoggerInterface


class TestLoggerInterface(TestCase):

    def setUp(self):
        super().setUp()
        self.logger_interface = LoggerInterface(MockApikeyClient(), "")

    def test_post_messages(self):
        response = MockResponse({
            "traceIds": [],
            "status": "Created: messages stored",
            "code": 201
        })
        response.status_code = 201
        self.logger_interface._client.post = Mock(return_value=response)
        self.assertEqual(response.json()["traceIds"], self.logger_interface.post_messages([]))

    def test_post_messages_exception(self):
        response = MockResponse(None)
        response.status_code = 400
        self.logger_interface._client.post = Mock(return_value=response)
        with self.assertRaises(CreationError):
            self.logger_interface.post_messages([])

    def test_post_messages_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.logger_interface._client.post = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.logger_interface.post_messages([])
