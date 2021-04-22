from __future__ import absolute_import, annotations

from unittest import TestCase
from unittest.mock import Mock

from test.wenet_test.common.interface.mock.client import MockApikeyClient, MockOauth2Client
from test.wenet_test.common.interface.mock.response import MockResponse
from wenet.common.interface.client import NoAuthenticationClient
from wenet.common.interface.exceptions import AuthenticationException
from wenet.common.interface.hub import HubInterface
from wenet.common.model.app.app_dto import App


class TestHubInterface(TestCase):

    def test_creation(self):
        self.assertIsInstance(HubInterface(NoAuthenticationClient()), HubInterface)
        self.assertIsInstance(HubInterface(MockApikeyClient()), HubInterface)
        with self.assertRaises(AuthenticationException):
            HubInterface(MockOauth2Client())

    def setUp(self):
        super().setUp()
        self.hub_interface = HubInterface(MockApikeyClient())

    def test_get_user_ids_for_app(self):
        response = MockResponse([])
        response.status_code = 200
        self.hub_interface._client.get = Mock(return_value=response)
        self.assertEqual(response.json(), self.hub_interface.get_user_ids_for_app(""))

        response.status_code = 400
        with self.assertRaises(Exception):
            self.hub_interface.get_user_ids_for_app("")

    def test_get_app_details(self):
        response = MockResponse({
            "id": "id",
            "name": "name",
            "status": 1,
            "ownerId": 1,
            "image_url": "image_url",
            "createdAt": 1612518873,
            "updatedAt": 1612532618,
            "metadata": {},
            "messageCallbackUrl": "messageCallbackUrl"
        })
        response.status_code = 200
        self.hub_interface._client.get = Mock(return_value=response)
        self.assertEqual(App.from_repr(response.json()), self.hub_interface.get_app_details(""))

        response.status_code = 400
        with self.assertRaises(Exception):
            self.hub_interface.get_app_details("")

    def test_get_app_developers(self):
        response = MockResponse([])
        response.status_code = 200
        self.hub_interface._client.get = Mock(return_value=response)
        self.assertEqual(response.json(), self.hub_interface.get_app_developers(""))

        response.status_code = 400
        with self.assertRaises(Exception):
            self.hub_interface.get_app_developers("")

    def test_get_user_ids(self):
        response = MockResponse([])
        response.status_code = 200
        self.hub_interface._client.get = Mock(return_value=response)
        self.assertEqual(response.json(), self.hub_interface.get_user_ids())

        response.status_code = 400
        with self.assertRaises(Exception):
            self.hub_interface.get_user_ids()
