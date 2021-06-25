from __future__ import absolute_import, annotations

from unittest import TestCase
from unittest.mock import Mock

from test.unit.wenet.interface.mock.client import MockApikeyClient
from test.unit.wenet.interface.mock.response import MockResponse
from wenet.interface.exceptions import AuthenticationException, NotFound
from wenet.interface.hub import HubInterface
from wenet.model.app.app_dto import App


class TestHubInterface(TestCase):

    def setUp(self):
        super().setUp()
        self.hub_interface = HubInterface(MockApikeyClient(), "")

    def test_get_user_ids_for_app(self):
        response = MockResponse(["user_id"])
        response.status_code = 200
        self.hub_interface._client.get = Mock(return_value=response)
        self.assertEqual(response.json(), self.hub_interface.get_user_ids_for_app("app_id"))

    def test_get_user_ids_for_app_exception(self):
        response = MockResponse(None)
        response.status_code = 400
        self.hub_interface._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.hub_interface.get_user_ids_for_app("app_id")

    def test_get_user_ids_for_app_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.hub_interface._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.hub_interface.get_user_ids_for_app("app_id")

    def test_get_user_ids_for_app_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.hub_interface._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.hub_interface.get_user_ids_for_app("app_id")

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
        self.assertEqual(App.from_repr(response.json()), self.hub_interface.get_app_details("app_id"))

    def test_get_app_details_exception(self):
        response = MockResponse(None)
        response.status_code = 400
        self.hub_interface._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.hub_interface.get_app_details("app_id")

    def test_get_app_details_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.hub_interface._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.hub_interface.get_app_details("app_id")

    def test_get_app_details_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.hub_interface._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.hub_interface.get_app_details("app_id")

    def test_get_app_developers(self):
        response = MockResponse(["developer_id"])
        response.status_code = 200
        self.hub_interface._client.get = Mock(return_value=response)
        self.assertEqual(response.json(), self.hub_interface.get_app_developers("app_id"))

    def test_get_app_developers_exception(self):
        response = MockResponse(None)
        response.status_code = 400
        self.hub_interface._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.hub_interface.get_app_developers("app_id")

    def test_get_app_developers_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.hub_interface._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.hub_interface.get_app_developers("app_id")

    def test_get_app_developers_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.hub_interface._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.hub_interface.get_app_developers("app_id")

    def test_get_user_ids(self):
        response = MockResponse(["user_id"])
        response.status_code = 200
        self.hub_interface._client.get = Mock(return_value=response)
        self.assertEqual(response.json(), self.hub_interface.get_user_ids())

    def test_get_user_ids_exception(self):
        response = MockResponse(None)
        response.status_code = 400
        self.hub_interface._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.hub_interface.get_user_ids()

    def test_get_user_ids_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.hub_interface._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.hub_interface.get_user_ids()
