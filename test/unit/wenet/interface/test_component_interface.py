from __future__ import absolute_import, annotations

from unittest import TestCase

from test.unit.wenet.interface.mock.response import MockResponse
from wenet.interface.component import ComponentInterface
from wenet.interface.exceptions import ApiException, BadRequest, AuthenticationException, BadGateway


class TestComponentInterface(TestCase):

    def test_get_api_exception_for_response(self):
        response = MockResponse({})
        response.status_code = 400

        ex = ComponentInterface.get_api_exception_for_response(response)
        self.assertIsInstance(ex, ApiException)
        self.assertIsInstance(ex, BadRequest)
        self.assertEqual(response.status_code, ex.http_status_code)

        response = MockResponse({})
        response.status_code = 401

        ex = ComponentInterface.get_api_exception_for_response(response)
        self.assertIsInstance(ex, ApiException)
        self.assertIsInstance(ex, AuthenticationException)
        self.assertEqual(response.status_code, ex.http_status_code)

        response = MockResponse({})
        response.status_code = 403

        ex = ComponentInterface.get_api_exception_for_response(response)
        self.assertIsInstance(ex, ApiException)
        self.assertIsInstance(ex, AuthenticationException)
        self.assertEqual(response.status_code, ex.http_status_code)

        response = MockResponse({})
        response.status_code = 502

        ex = ComponentInterface.get_api_exception_for_response(response)
        self.assertIsInstance(ex, ApiException)
        self.assertIsInstance(ex, BadGateway)
        self.assertEqual(response.status_code, ex.http_status_code)

        response = MockResponse({})
        response.status_code = 303

        ex = ComponentInterface.get_api_exception_for_response(response)
        self.assertIsInstance(ex, ApiException)
        self.assertEqual(response.status_code, ex.http_status_code)
