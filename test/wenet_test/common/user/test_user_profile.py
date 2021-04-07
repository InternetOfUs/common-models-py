from unittest import TestCase

from wenet.common.model.user.user_profile import WeNetUserProfilesPage, UserIdentifiersPage, WeNetUserProfile


class TestWeNetUserProfilesPage(TestCase):

    def test_repr(self):
        profiles_page = WeNetUserProfilesPage(0, 0, None)
        self.assertEqual(profiles_page, WeNetUserProfilesPage.from_repr(profiles_page.to_repr()))

        profile = WeNetUserProfile(
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "profile_id",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None
        )
        profiles_page = WeNetUserProfilesPage(0, 0, [profile])
        self.assertEqual(profiles_page, WeNetUserProfilesPage.from_repr(profiles_page.to_repr()))

    def test_null_task_repr(self):
        profiles_page_repr = {
            "offset": 0,
            "total": 0,
            "transactions": None
        }
        self.assertIsInstance(WeNetUserProfilesPage.from_repr(profiles_page_repr), WeNetUserProfilesPage)


class TestUserIdentifiersPage(TestCase):

    def test_repr(self):
        user_ids_page = UserIdentifiersPage(0, 0, None)
        self.assertEqual(user_ids_page, UserIdentifiersPage.from_repr(user_ids_page.to_repr()))

        user_id = "user_id"
        user_ids_page = UserIdentifiersPage(0, 0, [user_id])
        self.assertEqual(user_ids_page, UserIdentifiersPage.from_repr(user_ids_page.to_repr()))

    def test_null_task_repr(self):
        user_ids_page_repr = {
            "offset": 0,
            "total": 0,
            "transactions": None
        }
        self.assertIsInstance(UserIdentifiersPage.from_repr(user_ids_page_repr), UserIdentifiersPage)
