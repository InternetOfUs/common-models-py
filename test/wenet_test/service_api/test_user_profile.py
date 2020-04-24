from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.service_api.common import Date, Gender, UserLanguage
from wenet.service_api.norm import Norm, NormOperator
from wenet.service_api.user_profile import UserName, WeNetUserProfile


class TestUserName(TestCase):

    def test_repr(self):
        user_name = UserName(
            first="first",
            middle="middle",
            last="last",
            prefix="prefix",
            suffix="suffix"
        )

        to_repr = user_name.to_repr()
        from_repr = UserName.from_repr(to_repr)
        self.assertIsInstance(from_repr, UserName)
        self.assertEqual(user_name, from_repr)

    def test_equal(self):
        user_name = UserName(
            first="first",
            middle="middle",
            last="last",
            prefix="prefix",
            suffix="suffix"
        )

        user_name1 = UserName(
            first="first",
            middle="middle",
            last="last",
            prefix="prefix",
            suffix="suffix"
        )

        user_name2 = UserName(
            first="first1",
            middle="middle",
            last="last",
            prefix="prefix",
            suffix="suffix"
        )

        user_name3 = UserName(
            first="first",
            middle="middle1",
            last="last",
            prefix="prefix",
            suffix="suffix"
        )

        user_name4 = UserName(
            first="first",
            middle="middle",
            last="last1",
            prefix="prefix",
            suffix="suffix"
        )

        user_name5 = UserName(
            first="first",
            middle="middle",
            last="last",
            prefix="prefix1",
            suffix="suffix"
        )

        user_name6 = UserName(
            first="first",
            middle="middle",
            last="last",
            prefix="prefix",
            suffix="suffix1"
        )

        self.assertEqual(user_name, user_name1)
        self.assertNotEqual(user_name, user_name2)
        self.assertNotEqual(user_name, user_name3)
        self.assertNotEqual(user_name, user_name4)
        self.assertNotEqual(user_name, user_name5)
        self.assertNotEqual(user_name, user_name6)


class TestUserProfile(TestCase):

    def test_repr(self):

        user_profile = WeNetUserProfile(
            name=UserName(
                first="first",
                middle="middle",
                last="last",
                prefix="prefix",
                suffix="suffix"
            ),
            date_of_birth=Date(
                year=2020,
                month=1,
                day=20
            ),
            gender=Gender.MALE,
            email="email@example.com",
            phone_number="phone number",
            locale="it_IT",
            avatar="avatar",
            nationality="it",
            languages=[
                UserLanguage(
                    name="ita",
                    level="C2",
                    code="it"
                )
            ],
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id", norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            social_practices=[],
            personal_behaviours=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertIsInstance(from_repr, WeNetUserProfile)
        self.assertEqual(user_profile, from_repr)

    def test_repr2(self):

        user_profile = WeNetUserProfile(
            name=UserName(
                first=None,
                middle=None,
                last=None,
                prefix=None,
                suffix=None
            ),
            date_of_birth=Date(
                year=2020,
                month=1,
                day=20
            ),
            gender=None,
            email=None,
            phone_number=None,
            locale=None,
            avatar=None,
            nationality=None,
            languages=[],
            occupation=None,
            creation_ts=None,
            last_update_ts=None,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            social_practices=[],
            personal_behaviours=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertIsInstance(from_repr, WeNetUserProfile)
        self.assertEqual(user_profile, from_repr)

    def test_repr3(self):

        user_profile = WeNetUserProfile(
            name=UserName(
                first=None,
                middle=None,
                last=None,
                prefix=None,
                suffix=None
            ),
            date_of_birth=Date(
                year=2020,
                month=1,
                day=20
            ),
            gender=None,
            email=None,
            phone_number=None,
            locale=None,
            avatar=None,
            nationality=None,
            languages=[],
            occupation=None,
            creation_ts=None,
            last_update_ts=None,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            social_practices=[],
            personal_behaviours=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr, "profile_id1")

        self.assertIsInstance(from_repr, WeNetUserProfile)
        self.assertEqual("profile_id1", from_repr.profile_id)

    def test_repr4(self):

        user_profile = WeNetUserProfile(
            name=UserName(
                first="first",
                middle="middle",
                last="last",
                prefix="prefix",
                suffix="suffix"
            ),
            date_of_birth=Date(
                year=2020,
                month=1,
                day=20
            ),
            gender=Gender.OTHER,
            email="email@example.com",
            phone_number="phone number",
            locale="it_IT",
            avatar="avatar",
            nationality="it",
            languages=[
                UserLanguage(
                    name="ita",
                    level="C2",
                    code="it"
                )
            ],
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id", norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            social_practices=[],
            personal_behaviours=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertIsInstance(from_repr, WeNetUserProfile)
        self.assertEqual(user_profile, from_repr)
