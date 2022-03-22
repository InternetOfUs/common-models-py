from __future__ import absolute_import, annotations

from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

import pytz

from test.unit.wenet.interface.mock.client import MockOauth2Client
from test.unit.wenet.interface.mock.response import MockResponse
from wenet.interface.exceptions import NotFound, BadRequest, AuthenticationException
from wenet.interface.service_api import ServiceApiInterface
from wenet.model.app import AppDTO
from wenet.model.logging_message.content import ActionRequest
from wenet.model.logging_message.message import RequestMessage
from wenet.model.protocol_norm import ProtocolNorm
from wenet.model.task.task import Task, TaskGoal, TaskPage
from wenet.model.task.transaction import TaskTransaction
from wenet.model.user.competence import Competence
from wenet.model.user.material import Material
from wenet.model.user.meaning import Meaning
from wenet.model.user.personal_behaviors import PersonalBehavior, ScoredLabel, Label
from wenet.model.user.planned_activity import PlannedActivity, ActivityStatus
from wenet.model.user.relationship import Relationship, RelationType
from wenet.model.user.relevant_location import RelevantLocation
from wenet.model.user.token import TokenDetails
from wenet.model.user.profile import WeNetUserProfile, CoreWeNetUserProfile


class TestServiceApiInterface(TestCase):

    def setUp(self):
        super().setUp()
        self.service_api = ServiceApiInterface(MockOauth2Client(), "")

    def test_get_token_details(self):
        response = MockResponse(TokenDetails("1", "app_id", []).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual(TokenDetails("1", "app_id", []), self.service_api.get_token_details())

    def test_get_token_details_exception(self):
        response = MockResponse(TokenDetails("1", "app_id", []).to_repr())
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_token_details()

    def test_get_token_details_unauthorized(self):
        response = MockResponse(TokenDetails("1", "app_id", []).to_repr())
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_token_details()

    def test_get_app_details(self):
        response = MockResponse(AppDTO(None, None, "app_id", None, None).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual(AppDTO(None, None, "app_id", None, None), self.service_api.get_app_details("app_id"))

    def test_get_app_details_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_app_details("app_id")

    def test_get_app_details_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_app_details("app_id")

    def test_get_app_details_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_app_details("app_id")

    def test_get_app_users(self):
        response = MockResponse(["user_id"])
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual(["user_id"], self.service_api.get_app_users("app_id"))

    def test_get_app_users_exception(self):
        response = MockResponse(["user_id"])
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_app_users("app_id")

    def test_get_app_users_not_found(self):
        response = MockResponse(["user_id"])
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_app_users("app_id")

    def test_get_app_users_unauthorized(self):
        response = MockResponse(["user_id"])
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_app_users("app_id")

    def test_create_task(self):
        task = Task(None, None, None, "", "", "", None, TaskGoal("", ""))
        response = MockResponse(task.to_repr())
        response.status_code = 201
        self.service_api._client.post = Mock(return_value=response)
        self.assertEqual(task, self.service_api.create_task(task))

    def test_create_task_exception(self):
        task = Task(None, None, None, "", "", "", None, TaskGoal("", ""))
        response = MockResponse(None)
        response.status_code = 400
        self.service_api._client.post = Mock(return_value=response)
        with self.assertRaises(BadRequest):
            self.service_api.create_task(task)

    def test_create_task_unauthorized(self):
        task = Task(None, None, None, "", "", "", None, TaskGoal("", ""))
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.post = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.create_task(task)

    def test_get_task(self):
        response = MockResponse(Task("task_id", None, None, "", "", "", None, TaskGoal("", "")).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual(Task("task_id", None, None, "", "", "", None, TaskGoal("", "")), self.service_api.get_task("task_id"))

    def test_get_task_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_task("task_id")

    def test_get_task_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_task("task_id")

    def test_get_task_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_task("task_id")

    def test_create_task_transaction(self):
        transaction = TaskTransaction(None, "", "", 1, 1, "", None)
        response = MockResponse(None)
        response.status_code = 201
        self.service_api._client.post = Mock(return_value=response)
        self.assertIsNone(self.service_api.create_task_transaction(transaction))

    def test_create_task_transaction_exception(self):
        transaction = TaskTransaction(None, "", "", 1, 1, "", None)
        response = MockResponse(None)
        response.status_code = 400
        self.service_api._client.post = Mock(return_value=response)
        with self.assertRaises(BadRequest):
            self.service_api.create_task_transaction(transaction)

    def test_create_task_transaction_unauthorized(self):
        transaction = TaskTransaction(None, "", "", 1, 1, "", None)
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.post = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.create_task_transaction(transaction)

    def test_get_user_profile(self):
        response = MockResponse(WeNetUserProfile.empty("user_id").to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual(WeNetUserProfile.empty("user_id"), self.service_api.get_user_profile("user_id"))

    def test_get_user_profile_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_user_profile("user_id")

    def test_get_user_profile_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_user_profile("user_id")

    def test_get_user_profile_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_user_profile("user_id")

    def test_create_user_profile(self):
        response = MockResponse(None)
        response.status_code = 200
        self.service_api._client.post = Mock(return_value=response)
        self.assertIsNone(self.service_api.create_user_profile("user_id"))

    def test_create_user_profile_exception(self):
        response = MockResponse(None)
        response.status_code = 400
        self.service_api._client.post = Mock(return_value=response)
        with self.assertRaises(BadRequest):
            self.service_api.create_user_profile("user_id")

    def test_create_user_profile_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.post = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.create_user_profile("user_id")

    def test_update_user_profile(self):
        response = MockResponse(WeNetUserProfile.empty("user_id").to_repr())
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(WeNetUserProfile.empty("user_id"), self.service_api.update_user_profile("user_id", CoreWeNetUserProfile.empty("user_id")))

    def test_update_user_profile_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.update_user_profile("user_id", CoreWeNetUserProfile.empty("user_id"))

    def test_update_user_profile_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.update_user_profile("user_id", CoreWeNetUserProfile.empty("user_id"))

    def test_update_user_profile_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.update_user_profile("user_id", CoreWeNetUserProfile.empty("user_id"))

    def test_get_user_competences(self):
        response = MockResponse([
            {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
            }
        ])
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([
            {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
            }
        ], self.service_api.get_user_competences("user_id"))

    def test_get_user_competences_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_user_competences("user_id")

    def test_get_user_competences_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_user_competences("user_id")

    def test_get_user_competences_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_user_competences("user_id")

    def test_update_user_competences(self):
        competences = [
            {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
            }
        ]
        response = MockResponse(competences)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(competences, self.service_api.update_user_competences("user_id", competences))

    def test_update_user_competences_objects(self):
        competences = [
            Competence(
                name="name",
                ontology="ontology",
                level=0.8
            )
        ]
        response = MockResponse(competences)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(competences, self.service_api.update_user_competences("user_id", competences))

    def test_update_user_competences_exception(self):
        competences = [
            {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
            }
        ]
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.update_user_competences("user_id", competences)

    def test_update_user_competences_not_found(self):
        competences = [
            {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
            }
        ]
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.update_user_competences("user_id", competences)

    def test_update_user_competences_unauthorized(self):
        competences = [
            {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
            }
        ]
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.update_user_competences("user_id", competences)

    def test_get_user_materials(self):
        response = MockResponse([
            {
                "name": "car",
                "description": "Fiat 500",
                "quantity": 1,
                "classification": "nice"
            }
        ])
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([
            {
                "name": "car",
                "description": "Fiat 500",
                "quantity": 1,
                "classification": "nice"
            }
        ], self.service_api.get_user_materials("user_id"))

    def test_get_user_materials_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_user_materials("user_id")

    def test_get_user_materials_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_user_materials("user_id")

    def test_get_user_materials_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_user_materials("user_id")

    def test_update_user_materials(self):
        materials = [
            {
                "name": "car",
                "description": "Fiat 500",
                "quantity": 1,
                "classification": "nice"
            }
        ]
        response = MockResponse(materials)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(materials, self.service_api.update_user_materials("user_id", materials))

    def test_update_user_materials_objects(self):
        materials = [
            Material(
                name="name",
                description="description",
                quantity=1,
                classification="classification"
            )
        ]
        response = MockResponse(materials)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(materials, self.service_api.update_user_materials("user_id", materials))

    def test_update_user_materials_exception(self):
        materials = [
            {
                "name": "car",
                "description": "Fiat 500",
                "quantity": 1,
                "classification": "nice"
            }
        ]
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.update_user_materials("user_id", materials)

    def test_update_user_materials_not_found(self):
        materials = [
            {
                "name": "car",
                "description": "Fiat 500",
                "quantity": 1,
                "classification": "nice"
            }
        ]
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.update_user_materials("user_id", materials)

    def test_update_user_materials_unauthorized(self):
        materials = [
            {
                "name": "car",
                "description": "Fiat 500",
                "quantity": 1,
                "classification": "nice"
            }
        ]
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.update_user_materials("user_id", materials)

    def test_get_user_meanings(self):
        response = MockResponse([
            {
                "name": "extroversion",
                "category": "big_five",
                "level": 0.8
            }
        ])
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([
            {
                "name": "extroversion",
                "category": "big_five",
                "level": 0.8
            }
        ], self.service_api.get_user_meanings("user_id"))

    def test_get_user_meanings_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_user_meanings("user_id")

    def test_get_user_meanings_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_user_meanings("user_id")

    def test_get_user_meanings_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_user_meanings("user_id")

    def test_update_user_meanings(self):
        meanings = [
            {
                "name": "extroversion",
                "category": "big_five",
                "level": 0.8
            }
        ]
        response = MockResponse(meanings)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(meanings, self.service_api.update_user_meanings("user_id", meanings))

    def test_update_user_meanings_objects(self):
        meanings = [
            Meaning(
                name="name",
                category="category",
                level=0.8
            )
        ]
        response = MockResponse(meanings)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(meanings, self.service_api.update_user_meanings("user_id", meanings))

    def test_update_user_meanings_exception(self):
        meanings = [
            {
                "name": "extroversion",
                "category": "big_five",
                "level": 0.8
            }
        ]
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.update_user_meanings("user_id", meanings)

    def test_update_user_meanings_not_found(self):
        meanings = [
            {
                "name": "extroversion",
                "category": "big_five",
                "level": 0.8
            }
        ]
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.update_user_meanings("user_id", meanings)

    def test_update_user_meanings_unauthorized(self):
        meanings = [
            {
                "name": "extroversion",
                "category": "big_five",
                "level": 0.8
            }
        ]
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.update_user_meanings("user_id", meanings)

    def test_get_user_norms(self):
        response = MockResponse([
            {
                "description": "Notify to all the participants that the task is closed.",
                "whenever": "is_received_do_transaction('close',Reason) and not(is_task_closed()) and get_profile_id(Me) and get_task_requester_id(RequesterId) and =(Me,RequesterId) and get_participants(Participants)",
                "thenceforth": "add_message_transaction() and close_task() and send_messages(Participants,'close',Reason)",
                "ontology": "get_participants(P) :- get_task_state_attribute(UserIds,'participants',[]), get_profile_id(Me), wenet_remove(P,Me,UserIds)."
            }
        ])
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([
            {
                "description": "Notify to all the participants that the task is closed.",
                "whenever": "is_received_do_transaction('close',Reason) and not(is_task_closed()) and get_profile_id(Me) and get_task_requester_id(RequesterId) and =(Me,RequesterId) and get_participants(Participants)",
                "thenceforth": "add_message_transaction() and close_task() and send_messages(Participants,'close',Reason)",
                "ontology": "get_participants(P) :- get_task_state_attribute(UserIds,'participants',[]), get_profile_id(Me), wenet_remove(P,Me,UserIds)."
            }
        ], self.service_api.get_user_norms("user_id"))

    def test_get_user_norms_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_user_norms("user_id")

    def test_get_user_norms_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_user_norms("user_id")

    def test_get_user_norms_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_user_norms("user_id")

    def test_update_user_norms(self):
        norms = [
            {
                "description": "Notify to all the participants that the task is closed.",
                "whenever": "is_received_do_transaction('close',Reason) and not(is_task_closed()) and get_profile_id(Me) and get_task_requester_id(RequesterId) and =(Me,RequesterId) and get_participants(Participants)",
                "thenceforth": "add_message_transaction() and close_task() and send_messages(Participants,'close',Reason)",
                "ontology": "get_participants(P) :- get_task_state_attribute(UserIds,'participants',[]), get_profile_id(Me), wenet_remove(P,Me,UserIds)."
            }
        ]
        response = MockResponse(norms)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(norms, self.service_api.update_user_norms("user_id", norms))

    def test_update_user_norms_objects(self):
        norms = [
            ProtocolNorm(
                description="description",
                whenever="whenever",
                thenceforth="thenceforth",
                ontology="ontology"
            )
        ]
        response = MockResponse(norms)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(norms, self.service_api.update_user_norms("user_id", norms))

    def test_update_user_norms_exception(self):
        norms = [
            {
                "description": "Notify to all the participants that the task is closed.",
                "whenever": "is_received_do_transaction('close',Reason) and not(is_task_closed()) and get_profile_id(Me) and get_task_requester_id(RequesterId) and =(Me,RequesterId) and get_participants(Participants)",
                "thenceforth": "add_message_transaction() and close_task() and send_messages(Participants,'close',Reason)",
                "ontology": "get_participants(P) :- get_task_state_attribute(UserIds,'participants',[]), get_profile_id(Me), wenet_remove(P,Me,UserIds)."
            }
        ]
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.update_user_norms("user_id", norms)

    def test_update_user_norms_not_found(self):
        norms = [
            {
                "description": "Notify to all the participants that the task is closed.",
                "whenever": "is_received_do_transaction('close',Reason) and not(is_task_closed()) and get_profile_id(Me) and get_task_requester_id(RequesterId) and =(Me,RequesterId) and get_participants(Participants)",
                "thenceforth": "add_message_transaction() and close_task() and send_messages(Participants,'close',Reason)",
                "ontology": "get_participants(P) :- get_task_state_attribute(UserIds,'participants',[]), get_profile_id(Me), wenet_remove(P,Me,UserIds)."
            }
        ]
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.update_user_norms("user_id", norms)

    def test_update_user_norms_unauthorized(self):
        norms = [
            {
                "description": "Notify to all the participants that the task is closed.",
                "whenever": "is_received_do_transaction('close',Reason) and not(is_task_closed()) and get_profile_id(Me) and get_task_requester_id(RequesterId) and =(Me,RequesterId) and get_participants(Participants)",
                "thenceforth": "add_message_transaction() and close_task() and send_messages(Participants,'close',Reason)",
                "ontology": "get_participants(P) :- get_task_state_attribute(UserIds,'participants',[]), get_profile_id(Me), wenet_remove(P,Me,UserIds)."
            }
        ]
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.update_user_norms("user_id", norms)

    def test_get_user_personal_behaviors(self):
        response = MockResponse([
            {
                "user_id": "user_id",
                "weekday": "string",
                "label_distribution": {
                    "additionalProp1": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp2": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp3": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ]
                },
                "confidence": 0
            }
        ])
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([
            {
                "user_id": "user_id",
                "weekday": "string",
                "label_distribution": {
                    "additionalProp1": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp2": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp3": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ]
                },
                "confidence": 0
            }
        ], self.service_api.get_user_personal_behaviors("user_id"))

    def test_get_user_personal_behaviors_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_user_personal_behaviors("user_id")

    def test_get_user_personal_behaviors_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_user_personal_behaviors("user_id")

    def test_get_user_personal_behaviors_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_user_personal_behaviors("user_id")

    def test_update_user_personal_behaviors(self):
        personal_behaviors = [
            {
                "user_id": "user_id",
                "weekday": "string",
                "label_distribution": {
                    "additionalProp1": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp2": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp3": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ]
                },
                "confidence": 0
            }
        ]
        response = MockResponse(personal_behaviors)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(personal_behaviors, self.service_api.update_user_personal_behaviors("user_id", personal_behaviors))

    def test_update_user_personal_behaviors_objects(self):
        personal_behaviors = [
            PersonalBehavior(
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
        ]
        response = MockResponse(personal_behaviors)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(personal_behaviors, self.service_api.update_user_personal_behaviors("user_id", personal_behaviors))

    def test_update_user_personal_behaviors_exception(self):
        personal_behaviors = [
            {
                "user_id": "user_id",
                "weekday": "string",
                "label_distribution": {
                    "additionalProp1": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp2": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp3": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ]
                },
                "confidence": 0
            }
        ]
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.update_user_personal_behaviors("user_id", personal_behaviors)

    def test_update_user_personal_behaviors_not_found(self):
        personal_behaviors = [
            {
                "user_id": "user_id",
                "weekday": "string",
                "label_distribution": {
                    "additionalProp1": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp2": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp3": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ]
                },
                "confidence": 0
            }
        ]
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.update_user_personal_behaviors("user_id", personal_behaviors)

    def test_update_user_personal_behaviors_unauthorized(self):
        personal_behaviors = [
            {
                "user_id": "user_id",
                "weekday": "string",
                "label_distribution": {
                    "additionalProp1": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp2": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ],
                    "additionalProp3": [
                        {
                            "label": {
                                "name": "string",
                                "semantic_class": 0,
                                "latitude": 0,
                                "longitude": 0
                            },
                            "score": 0
                        }
                    ]
                },
                "confidence": 0
            }
        ]
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.update_user_personal_behaviors("user_id", personal_behaviors)

    def test_get_user_planned_activities(self):
        response = MockResponse([
            {
                "id": "hfdsfs888",
                "startTime": None,
                "endTime": None,
                "description": "A few beers for relaxing",
                "attendees": [
                    "user_id"
                ],
                "status": "confirmed"
            }
        ])
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([
            {
                "id": "hfdsfs888",
                "startTime": None,
                "endTime": None,
                "description": "A few beers for relaxing",
                "attendees": [
                    "user_id"
                ],
                "status": "confirmed"
            }
        ], self.service_api.get_user_planned_activities("user_id"))

    def test_get_user_planned_activities_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_user_planned_activities("user_id")

    def test_get_user_planned_activities_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_user_planned_activities("user_id")

    def test_get_user_planned_activities_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_user_planned_activities("user_id")

    def test_update_user_planned_activities(self):
        planned_activities = [
            {
                "id": "hfdsfs888",
                "startTime": None,
                "endTime": None,
                "description": "A few beers for relaxing",
                "attendees": [
                    "user_id"
                ],
                "status": "confirmed"
            }
        ]
        response = MockResponse(planned_activities)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(planned_activities, self.service_api.update_user_planned_activities("user_id", planned_activities))

    def test_update_user_planned_activities_objects(self):
        planned_activities = [
            PlannedActivity(
                activity_id="activity_id",
                start_time=datetime.now(tz=pytz.UTC),
                end_time=datetime.now(tz=pytz.UTC),
                description="description",
                attendees=["user_id"],
                status=ActivityStatus.CONFIRMED
            )
        ]
        response = MockResponse(planned_activities)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(planned_activities, self.service_api.update_user_planned_activities("user_id", planned_activities))

    def test_update_user_planned_activities_exception(self):
        planned_activities = [
            {
                "id": "hfdsfs888",
                "startTime": None,
                "endTime": None,
                "description": "A few beers for relaxing",
                "attendees": [
                    "user_id"
                ],
                "status": "confirmed"
            }
        ]
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.update_user_planned_activities("user_id", planned_activities)

    def test_update_user_planned_activities_not_found(self):
        planned_activities = [
            {
                "id": "hfdsfs888",
                "startTime": None,
                "endTime": None,
                "description": "A few beers for relaxing",
                "attendees": [
                    "user_id"
                ],
                "status": "confirmed"
            }
        ]
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.update_user_planned_activities("user_id", planned_activities)

    def test_update_user_planned_activities_unauthorized(self):
        planned_activities = [
            {
                "id": "hfdsfs888",
                "startTime": None,
                "endTime": None,
                "description": "A few beers for relaxing",
                "attendees": [
                    "user_id"
                ],
                "status": "confirmed"
            }
        ]
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.update_user_planned_activities("user_id", planned_activities)

    def test_get_user_relationships(self):
        response = MockResponse([
            {
                "userId": "user_id1",
                "type": "friend",
                "weight": 0.2
            }
        ])
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([
            {
                "userId": "user_id1",
                "type": "friend",
                "weight": 0.2
            }
        ], self.service_api.get_user_relationships("user_id"))

    def test_get_user_relationships_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_user_relationships("user_id")

    def test_get_user_relationships_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_user_relationships("user_id")

    def test_get_user_relationships_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_user_relationships("user_id")

    def test_update_user_relationships(self):
        relationships = [
            {
                "userId": "user_id1",
                "type": "friend",
                "weight": 0.2
            }
        ]
        response = MockResponse(relationships)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(relationships, self.service_api.update_user_relationships("user_id", relationships))

    def test_update_user_relationships_objects(self):
        relationships = [
            Relationship(
                app_id="app_id",
                source_id="source_id",
                target_id="target_id",
                relation_type=RelationType.COLLEAGUE,
                weight=0.8
            )
        ]
        response = MockResponse(relationships)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(relationships, self.service_api.update_user_relationships("user_id", relationships))

    def test_update_user_relationships_exception(self):
        relationships = [
            {
                "userId": "user_id1",
                "type": "friend",
                "weight": 0.2
            }
        ]
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.update_user_relationships("user_id", relationships)

    def test_update_user_relationships_not_found(self):
        relationships = [
            {
                "userId": "user_id1",
                "type": "friend",
                "weight": 0.2
            }
        ]
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.update_user_relationships("user_id", relationships)

    def test_update_user_relationships_unauthorized(self):
        relationships = [
            {
                "userId": "user_id1",
                "type": "friend",
                "weight": 0.2
            }
        ]
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.update_user_relationships("user_id", relationships)

    def test_get_user_relevant_locations(self):
        response = MockResponse([
            {
                "id": "kdjfghd8hikdfg",
                "label": "Home",
                "latitude": 40.388756,
                "longitude": -3.588622
            }
        ])
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([
            {
                "id": "kdjfghd8hikdfg",
                "label": "Home",
                "latitude": 40.388756,
                "longitude": -3.588622
            }
        ], self.service_api.get_user_relevant_locations("user_id"))

    def test_get_user_relevant_locations_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_user_relevant_locations("user_id")

    def test_get_user_relevant_locations_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_user_relevant_locations("user_id")

    def test_get_user_relevant_locations_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_user_relevant_locations("user_id")

    def test_update_user_relevant_locations(self):
        relevant_locations = [
            {
                "id": "kdjfghd8hikdfg",
                "label": "Home",
                "latitude": 40.388756,
                "longitude": -3.588622
            }
        ]
        response = MockResponse(relevant_locations)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(relevant_locations, self.service_api.update_user_relevant_locations("user_id", relevant_locations))

    def test_update_user_relevant_locations_objects(self):
        relevant_locations = [
            RelevantLocation(
                location_id="location_id",
                label="label",
                latitude=67,
                longitude=134
            )
        ]
        response = MockResponse(relevant_locations)
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(relevant_locations, self.service_api.update_user_relevant_locations("user_id", relevant_locations))

    def test_update_user_relevant_locations_exception(self):
        relevant_locations = [
            {
                "id": "kdjfghd8hikdfg",
                "label": "Home",
                "latitude": 40.388756,
                "longitude": -3.588622
            }
        ]
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.update_user_relevant_locations("user_id", relevant_locations)

    def test_update_user_relevant_locations_not_found(self):
        relevant_locations = [
            {
                "id": "kdjfghd8hikdfg",
                "label": "Home",
                "latitude": 40.388756,
                "longitude": -3.588622
            }
        ]
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.update_user_relevant_locations("user_id", relevant_locations)

    def test_update_user_relevant_locations_unauthorized(self):
        relevant_locations = [
            {
                "id": "kdjfghd8hikdfg",
                "label": "Home",
                "latitude": 40.388756,
                "longitude": -3.588622
            }
        ]
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.put = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.update_user_relevant_locations("user_id", relevant_locations)

    def test_get_opened_tasks_of_user(self):
        response = MockResponse(TaskPage(0, 1, [Task("task_id", None, None, "", "user_id", "app_id", None, TaskGoal("", ""))]).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([Task("task_id", None, None, "", "user_id", "app_id", None, TaskGoal("", ""))], self.service_api.get_opened_tasks_of_user("user_id", "app_id"))

    def test_get_opened_tasks_of_user_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_opened_tasks_of_user("user_id", "app_id")

    def test_get_opened_tasks_of_user_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_opened_tasks_of_user("user_id", "app_id")

    def test_get_opened_tasks_of_user_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_opened_tasks_of_user("user_id", "app_id")

    def test_get_all_tasks(self):
        response = MockResponse(TaskPage(0, 1, [Task("task_id", None, None, "", "", "app_id", None, TaskGoal("", ""))]).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([Task("task_id", None, None, "", "", "app_id", None, TaskGoal("", ""))], self.service_api.get_all_tasks(app_id="app_id"))

    def test_get_all_tasks_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_all_tasks(app_id="app_id")

    def test_get_all_tasks_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_all_tasks(app_id="app_id")

    def test_get_task_page(self):
        response = MockResponse(TaskPage(0, 1, [Task("task_id", None, None, "", "", "app_id", None, TaskGoal("", ""))]).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual(TaskPage(0, 1, [Task("task_id", None, None, "", "", "app_id", None, TaskGoal("", ""))]), self.service_api.get_task_page(app_id="app_id"))

    def test_get_task_page_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_task_page(app_id="app_id")

    def test_get_task_page_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_task_page(app_id="app_id")

    def test_get_all_tasks_of_application(self):
        response = MockResponse(TaskPage(0, 1, [Task("task_id", None, None, "", "", "", None, TaskGoal("", ""))]).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([Task("task_id", None, None, "", "", "", None, TaskGoal("", ""))], self.service_api.get_all_tasks_of_application("app_id"))

    def test_get_all_tasks_of_application_exception(self):
        response = MockResponse(None)
        response.status_code = 500
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(Exception):
            self.service_api.get_all_tasks_of_application("app_id")

    def test_get_all_tasks_of_application_not_found(self):
        response = MockResponse(None)
        response.status_code = 404
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(NotFound):
            self.service_api.get_all_tasks_of_application("app_id")

    def test_get_all_tasks_of_application_unauthorized(self):
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.get = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.get_all_tasks_of_application("app_id")

    def test_log_message(self):
        message = RequestMessage("message_id", "", "", "", ActionRequest(""))
        response = MockResponse(None)
        response.status_code = 201
        self.service_api._client.post = Mock(return_value=response)
        self.assertIsNone(self.service_api.log_message(message))

    def test_log_message_exception(self):
        message = RequestMessage("message_id", "", "", "", ActionRequest(""))
        response = MockResponse(None)
        response.status_code = 400
        self.service_api._client.post = Mock(return_value=response)
        with self.assertRaises(BadRequest):
            self.service_api.log_message(message)

    def test_log_message_unauthorized(self):
        message = RequestMessage("message_id", "", "", "", ActionRequest(""))
        response = MockResponse(None)
        response.status_code = 401
        self.service_api._client.post = Mock(return_value=response)
        with self.assertRaises(AuthenticationException):
            self.service_api.log_message(message)
