from __future__ import absolute_import, annotations

from unittest import TestCase
from unittest.mock import Mock

from test.wenet_test.common.interface.mock.client import MockApikeyClient, MockOauth2Client
from test.wenet_test.common.interface.mock.response import MockResponse
from wenet.common.interface.client import NoAuthenticationClient
from wenet.common.interface.exceptions import AuthenticationException
from wenet.common.interface.logger import LoggerInterface


class TestIncentiveServerInterface(TestCase):

    def test_creation(self):
        with self.assertRaises(AuthenticationException):
            LoggerInterface(NoAuthenticationClient())
        self.assertIsInstance(LoggerInterface(MockApikeyClient()), LoggerInterface)
        with self.assertRaises(AuthenticationException):
            LoggerInterface(MockOauth2Client())

    def setUp(self):
        super().setUp()
        self.logger_interface = LoggerInterface(MockApikeyClient())

    def test_post_messages(self):
        response = MockResponse({
            "traceIds": [],
            "status": "Created: messages stored",
            "code": 201
        })
        response.status_code = 201
        self.logger_interface._client.post = Mock(return_value=response)
        self.assertEqual(response.json()["traceIds"], self.logger_interface.post_messages([]))

        response.status_code = 400
        with self.assertRaises(Exception):
            self.logger_interface.post_messages([])
