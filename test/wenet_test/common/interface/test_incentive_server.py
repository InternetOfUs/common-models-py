from __future__ import absolute_import, annotations

from unittest import TestCase
from unittest.mock import Mock

from test.wenet_test.common.interface.mock.client import MockApikeyClient, MockOauth2Client
from test.wenet_test.common.interface.mock.response import MockResponse
from wenet.common.interface.client import NoAuthenticationClient
from wenet.common.interface.exceptions import AuthenticationException
from wenet.common.interface.incentive_server import IncentiveServerInterface


class TestIncentiveServerInterface(TestCase):

    def test_creation(self):
        with self.assertRaises(AuthenticationException):
            IncentiveServerInterface(NoAuthenticationClient())
        self.assertIsInstance(IncentiveServerInterface(MockApikeyClient()), IncentiveServerInterface)
        with self.assertRaises(AuthenticationException):
            IncentiveServerInterface(MockOauth2Client())

    def setUp(self):
        super().setUp()
        self.incentive_server_interface = IncentiveServerInterface(MockApikeyClient())

    def test_get_cohorts(self):
        response = MockResponse([
            {
                "id": 1,
                "user_id": "user_id",
                "app_id": "app_id",
                "created_at": "2021-03-01T21:00:02.695964Z",
                "email": "email",
                "cohort": 0
            }
        ])
        response.status_code = 200
        self.incentive_server_interface._client.get = Mock(return_value=response)
        self.assertEqual(response.json(), self.incentive_server_interface.get_cohorts())

        response.status_code = 400
        with self.assertRaises(Exception):
            self.incentive_server_interface.get_cohorts()