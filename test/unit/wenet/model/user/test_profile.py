from __future__ import absolute_import, annotations

from datetime import datetime
from unittest import TestCase

import pytz

from wenet.model.protocol_norm import ProtocolNorm
from wenet.model.scope import Scope
from wenet.model.user.common import Date, Gender
from wenet.model.user.competence import Competence
from wenet.model.user.material import Material
from wenet.model.user.meaning import Meaning
from wenet.model.user.personal_behaviors import PersonalBehavior, ScoredLabel, Label
from wenet.model.user.planned_activity import PlannedActivity, ActivityStatus
from wenet.model.user.profile import UserName, WeNetUserProfile, WeNetUserProfilesPage, UserIdentifiersPage, \
    PatchWeNetUserProfile
from wenet.model.user.relationship import Relationship, RelationType
from wenet.model.user.relevant_location import RelevantLocation


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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[
                {
                    "description": "Notify to all the participants that the task is closed.",
                    "whenever": "is_received_do_transaction('close',Reason) and not(is_task_closed()) and get_profile_id(Me) and get_task_requester_id(RequesterId) and =(Me,RequesterId) and get_participants(Participants)",
                    "thenceforth": "add_message_transaction() and close_task() and send_messages(Participants,'close',Reason)",
                    "ontology": "get_participants(P) :- get_task_state_attribute(UserIds,'participants',[]), get_profile_id(Me), wenet_remove(P,Me,UserIds)."
                }
            ],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
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
            occupation=None,
            creation_ts=None,
            last_update_ts=None,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
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
            occupation=None,
            creation_ts=None,
            last_update_ts=None,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertIsInstance(from_repr, WeNetUserProfile)
        self.assertEqual(user_profile, from_repr)

    def test_public_profile(self):

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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        to_repr = user_profile.to_public_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertIsInstance(from_repr, WeNetUserProfile)
        self.assertNotEqual(user_profile, from_repr)

        self.assertIsNotNone(from_repr.profile_id)
        self.assertIsNotNone(from_repr.name.first)
        self.assertIsNotNone(from_repr.name.last)
        self.assertIsNone(from_repr.name.middle)
        self.assertIsNone(from_repr.name.prefix)
        self.assertIsNone(from_repr.name.suffix)
        self.assertIsNone(from_repr.gender)
        self.assertIsNone(from_repr.email)
        self.assertIsNone(from_repr.phone_number)
        self.assertIsNone(from_repr.locale)
        self.assertIsNone(from_repr.nationality)
        self.assertIsNone(from_repr.date_of_birth)

    def test_filtered_repr(self):

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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        to_repr = user_profile.to_filtered_repr(scope_list=[Scope.ID, Scope.PHONE_NUMBER])
        from_repr = user_profile.from_repr(to_repr)

        self.assertIsInstance(from_repr, WeNetUserProfile)
        self.assertNotEqual(user_profile, from_repr)

        self.assertIsNotNone(from_repr.profile_id)
        self.assertIsNone(from_repr.name.first)
        self.assertIsNone(from_repr.name.last)
        self.assertIsNone(from_repr.name.middle)
        self.assertIsNone(from_repr.name.prefix)
        self.assertIsNone(from_repr.name.suffix)
        self.assertIsNone(from_repr.gender)
        self.assertIsNone(from_repr.email)
        self.assertIsNotNone(from_repr.phone_number)
        self.assertIsNone(from_repr.locale)
        self.assertIsNone(from_repr.nationality)
        self.assertIsNone(from_repr.date_of_birth)

    def test_norms_as_objects(self):
        norm = ProtocolNorm(
            description="description",
            whenever="whenever",
            thenceforth="thenceforth",
            ontology="ontology"
        )

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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[norm],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertEqual([norm.to_repr()], from_repr.norms)
        self.assertEqual([norm], from_repr.norms_as_objects)

    def test_planned_activities_as_objects(self):
        activity = PlannedActivity(
            activity_id="activity_id",
            start_time=datetime.now(tz=pytz.UTC),
            end_time=datetime.now(tz=pytz.UTC),
            description="description",
            attendees=["user_id"],
            status=ActivityStatus.CONFIRMED
        )

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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[],
            planned_activities=[activity],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertEqual([activity.to_repr()], from_repr.planned_activities)
        self.assertEqual([activity], from_repr.planned_activities_as_objects)

    def test_relevant_locations_as_objects(self):
        relevant_location = RelevantLocation(
            location_id="location_id",
            label="label",
            latitude=67,
            longitude=134
        )

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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[relevant_location],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertEqual([relevant_location.to_repr()], from_repr.relevant_locations)
        self.assertEqual([relevant_location], from_repr.relevant_locations_as_objects)

    def test_relationships_objects(self):
        relationship = Relationship(
            app_id="app_id",
            user_id="user_id",
            relation_type=RelationType.COLLEAGUE,
            weight=0.8
        )

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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[relationship],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertEqual([relationship.to_repr()], from_repr.relationships)
        self.assertEqual([relationship], from_repr.relationships_objects)

    def test_personal_behaviours_as_objects(self):
        personal_behaviors = PersonalBehavior(
            user_id="user_id",
            weekday="monday",
            label_distribution={
                "slot": [ScoredLabel(
                    label=Label(
                        name="name",
                        semantic_class=1,
                        latitude=67,
                        longitude=134
                    ),
                    score=0.7
                )]
            },
            confidence=0.8
        )

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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[personal_behaviors],
            materials=[],
            competences=[],
            meanings=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertEqual([personal_behaviors.to_repr()], from_repr.personal_behaviours)
        self.assertEqual([personal_behaviors], from_repr.personal_behaviours_as_objects)

    def test_materials_as_objects(self):
        material = Material(
            name="name",
            description="description",
            quantity=1,
            classification="classification"
        )

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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[material],
            competences=[],
            meanings=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertEqual([material.to_repr()], from_repr.materials)
        self.assertEqual([material], from_repr.materials_as_objects)

    def test_competences_as_objects(self):
        competence = Competence(
            name="name",
            ontology="ontology",
            level=0.8
        )

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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[competence],
            meanings=[]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertEqual([competence.to_repr()], from_repr.competences)
        self.assertEqual([competence], from_repr.competences_as_objects)

    def test_meanings_as_objects(self):
        meaning = Meaning(
            name="name",
            category="category",
            level=0.8
        )

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
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id="profile_id",
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[meaning]
        )

        to_repr = user_profile.to_repr()
        from_repr = user_profile.from_repr(to_repr)

        self.assertEqual([meaning.to_repr()], from_repr.meanings)
        self.assertEqual([meaning], from_repr.meanings_as_objects)


class TestPatchWeNetUserProfile(TestCase):

    def test_patch(self):
        user_profile = PatchWeNetUserProfile(profile_id="profile_id", competences=[
            {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
            }
        ])
        user_profile_patch = user_profile.to_patch()
        self.assertIn("id", user_profile_patch)
        self.assertIn("competences", user_profile_patch)
        self.assertNotIn("norms", user_profile_patch)
        self.assertNotIn("plannedActivities", user_profile_patch)
        self.assertNotIn("relevantLocations", user_profile_patch)
        self.assertNotIn("relationships", user_profile_patch)
        self.assertNotIn("personalBehaviors", user_profile_patch)
        self.assertNotIn("materials", user_profile_patch)
        self.assertNotIn("meanings", user_profile_patch)

        self.assertEqual([{
            "name": "language_Italian_C1",
            "ontology": "esco",
            "level": 0.8
        }], user_profile_patch["competences"])

    def test_patch_with_object(self):
        user_profile = PatchWeNetUserProfile(profile_id="profile_id", competences=[
             Competence(
                name="name",
                ontology="ontology",
                level=0.8
            )
        ])
        user_profile_patch = user_profile.to_patch()
        self.assertIn("id", user_profile_patch)
        self.assertIn("competences", user_profile_patch)
        self.assertNotIn("norms", user_profile_patch)
        self.assertNotIn("plannedActivities", user_profile_patch)
        self.assertNotIn("relevantLocations", user_profile_patch)
        self.assertNotIn("relationships", user_profile_patch)
        self.assertNotIn("personalBehaviors", user_profile_patch)
        self.assertNotIn("materials", user_profile_patch)
        self.assertNotIn("meanings", user_profile_patch)

        self.assertEqual([{
            "name": "name",
            "ontology": "ontology",
            "level": 0.8
        }], user_profile_patch["competences"])


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

