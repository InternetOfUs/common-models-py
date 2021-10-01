from __future__ import absolute_import, annotations

from unittest import TestCase
from unittest.mock import Mock

from test.unit.wenet.interface.mock.client import MockApikeyClient
from test.unit.wenet.interface.mock.response import MockResponse
from wenet.interface.exceptions import AuthenticationException, NotFound, CreationError
from wenet.interface.profile_manager import ProfileManagerInterface
from wenet.model.user.profile import WeNetUserProfile, UserIdentifiersPage, WeNetUserProfilesPage, PatchWeNetUserProfile


class TestProfileManagerInterface(TestCase):

    def setUp(self):
        super().setUp()
        self.profile_manager = ProfileManagerInterface(MockApikeyClient(), "")

    def test_get_user_profile(self):
        response = MockResponse(WeNetUserProfile.empty("user_id").to_repr())
        response.status_code = 200
        self.profile_manager._client.get = Mock(return_value=response)
        self.assertEqual(WeNetUserProfile.from_repr(response.json()), self.profile_manager.get_user_profile("user_id"))

    def test_get_user_profile_exception(self):
        response = MockResponse(None)
        response.status_code = 400
        self.profile_manager._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.profile_manager.get_user_profile("user_id")

    def test_get_user_profile_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.profile_manager._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.profile_manager.get_user_profile("user_id")

    def test_get_user_profile_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.profile_manager._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.profile_manager.get_user_profile("user_id")

    def test_update_user_profile(self):
        user_profile = WeNetUserProfile.empty("user_id")
        response = MockResponse(user_profile.to_repr())
        response.status_code = 200
        self.profile_manager._client.put = Mock(return_value=response)
        self.assertEqual(user_profile, self.profile_manager.update_user_profile(user_profile))

    def test_update_user_profile_exception(self):
        user_profile = WeNetUserProfile.empty("user_id")
        response = MockResponse(None)
        response.status_code = 400
        self.profile_manager._client.put = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.profile_manager.update_user_profile(user_profile)

    def test_update_user_profile_unauthorized(self):
        user_profile = WeNetUserProfile.empty("user_id")
        response = MockResponse(None)
        response.status_code = 401
        self.profile_manager._client.put = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.profile_manager.update_user_profile(user_profile)

    def test_patch_user_profile(self):
        user_profile = PatchWeNetUserProfile("user_id")
        response = MockResponse(WeNetUserProfile.empty("user_id").to_repr())
        response.status_code = 200
        self.profile_manager._client.patch = Mock(return_value=response)
        self.assertEqual(WeNetUserProfile.empty("user_id"), self.profile_manager.patch_user_profile(user_profile))

    def test_patch_user_profile_exception(self):
        user_profile = PatchWeNetUserProfile("user_id")
        response = MockResponse(None)
        response.status_code = 400
        self.profile_manager._client.patch = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.profile_manager.patch_user_profile(user_profile)

    def test_patch_user_profile_unauthorized(self):
        user_profile = PatchWeNetUserProfile("user_id")
        response = MockResponse(None)
        response.status_code = 401
        self.profile_manager._client.patch = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.profile_manager.patch_user_profile(user_profile)

    def test_create_empty_user_profile(self):
        response = MockResponse(None)
        response.status_code = 200
        self.profile_manager._client.put = Mock(return_value=response)
        self.assertEqual(WeNetUserProfile.empty("user_id"), self.profile_manager.create_empty_user_profile("user_id"))

    def test_create_empty_user_profile_exception(self):
        response = MockResponse(None)
        response.status_code = 400
        self.profile_manager._client.put = Mock(return_value=response)
        with self.assertRaises(CreationError):
            self.profile_manager.create_empty_user_profile("user_id")

    def test_create_empty_user_profile_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.profile_manager._client.put = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.profile_manager.create_empty_user_profile("user_id")

    def test_delete_user_profile(self):
        response = MockResponse(None)
        response.status_code = 204
        self.profile_manager._client.delete = Mock(return_value=response)
        self.assertIsNone(self.profile_manager.delete_user_profile("user_id"))

    def test_delete_user_profile_exception(self):
        response = MockResponse(None)
        response.status_code = 400
        self.profile_manager._client.delete = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.profile_manager.delete_user_profile("user_id")

    def test_delete_user_profile_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.profile_manager._client.delete = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.profile_manager.delete_user_profile("user_id")

    def test_delete_user_profile_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.profile_manager._client.delete = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.profile_manager.delete_user_profile("user_id")

    def test_get_profiles(self):
        response = MockResponse(WeNetUserProfilesPage(0, 0, []).to_repr())
        response.status_code = 200
        self.profile_manager._client.get = Mock(return_value=response)
        self.assertListEqual([], self.profile_manager.get_profiles())

    def test_get_profiles_exception(self):
        response = MockResponse(None)
        response.status_code = 400
        self.profile_manager._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.profile_manager.get_profiles()

    def test_get_profiles_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.profile_manager._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.profile_manager.get_profiles()

    def test_get_profile_user_ids(self):
        response = MockResponse(UserIdentifiersPage(0, 0, []).to_repr())
        response.status_code = 200
        self.profile_manager._client.get = Mock(return_value=response)
        self.assertListEqual([], self.profile_manager.get_profile_user_ids())

    def test_get_profile_user_ids_exception(self):
        response = MockResponse(None)
        response.status_code = 400
        self.profile_manager._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.profile_manager.get_profile_user_ids()

    def test_get_profile_user_ids_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.profile_manager._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.profile_manager.get_profile_user_ids()
