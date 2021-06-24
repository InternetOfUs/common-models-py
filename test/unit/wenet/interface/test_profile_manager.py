from __future__ import absolute_import, annotations

from unittest import TestCase
from unittest.mock import Mock

from test.unit.wenet.interface.mock.client import MockApikeyClient
from test.unit.wenet.interface.mock.response import MockResponse
from wenet.interface.exceptions import AuthenticationException
from wenet.interface.profile_manager import ProfileManagerInterface
from wenet.model.user.user_profile import WeNetUserProfile, UserIdentifiersPage, WeNetUserProfilesPage


class TestProfileManagerInterface(TestCase):

    def setUp(self):
        super().setUp()
        self.profile_manager = ProfileManagerInterface(MockApikeyClient(), "")

    def test_get_user_profile(self):
        response = MockResponse(WeNetUserProfile.empty("user_id").to_repr())
        response.status_code = 200
        self.profile_manager._client.get = Mock(return_value=response)
        self.assertEqual(WeNetUserProfile.from_repr(response.json()), self.profile_manager.get_user_profile("user_id"))

        response.status_code = 400
        with self.assertRaises(Exception):
            self.profile_manager.get_user_profile("user_id")

        response.status_code = 401
        with self.assertRaises(AuthenticationException):
            self.profile_manager.get_user_profile("user_id")

    def test_update_user_profile(self) -> None:
        user_profile = WeNetUserProfile.empty("user_id")
        response = MockResponse(None)
        response.status_code = 200
        self.profile_manager._client.put = Mock(return_value=response)
        self.assertIsNone(self.profile_manager.update_user_profile(user_profile))

        response.status_code = 400
        with self.assertRaises(Exception):
            self.profile_manager.update_user_profile(user_profile)

        response.status_code = 401
        with self.assertRaises(AuthenticationException):
            self.profile_manager.update_user_profile(user_profile)

    def test_create_empty_user_profile(self):
        response = MockResponse(None)
        response.status_code = 200
        self.profile_manager._client.put = Mock(return_value=response)
        self.assertEqual(WeNetUserProfile.empty("user_id"), self.profile_manager.create_empty_user_profile("user_id"))

        response.status_code = 400
        with self.assertRaises(Exception):
            self.profile_manager.create_empty_user_profile("user_id")

        response.status_code = 401
        with self.assertRaises(AuthenticationException):
            self.profile_manager.create_empty_user_profile("user_id")

    def test_delete_user_profile(self):
        response = MockResponse(None)
        response.status_code = 204
        self.profile_manager._client.delete = Mock(return_value=response)
        self.assertIsNone(self.profile_manager.delete_user_profile("user_id"))

        response.status_code = 400
        with self.assertRaises(Exception):
            self.profile_manager.delete_user_profile("user_id")

        response.status_code = 401
        with self.assertRaises(AuthenticationException):
            self.profile_manager.delete_user_profile("user_id")

    def test_get_profiles(self):
        response = MockResponse(WeNetUserProfilesPage(0, 0, []).to_repr())
        response.status_code = 200
        self.profile_manager._client.get = Mock(return_value=response)
        self.assertListEqual([], self.profile_manager.get_profiles())

        response.status_code = 400
        with self.assertRaises(Exception):
            self.profile_manager.get_profiles()

        response.status_code = 401
        with self.assertRaises(AuthenticationException):
            self.profile_manager.get_profiles()

    def test_get_profile_user_ids(self):
        response = MockResponse(UserIdentifiersPage(0, 0, []).to_repr())
        response.status_code = 200
        self.profile_manager._client.get = Mock(return_value=response)
        self.assertListEqual([], self.profile_manager.get_profile_user_ids())

        response.status_code = 400
        with self.assertRaises(Exception):
            self.profile_manager.get_profile_user_ids()

        response.status_code = 401
        with self.assertRaises(AuthenticationException):
            self.profile_manager.get_profile_user_ids()
