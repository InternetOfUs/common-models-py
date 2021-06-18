from __future__ import absolute_import, annotations

from unittest import TestCase
from unittest.mock import Mock

from test.wenet_test.common.interface.mock.client import MockApikeyClient, MockOauth2Client
from test.wenet_test.common.interface.mock.response import MockResponse
from wenet.common.interface.client import NoAuthenticationClient
from wenet.common.interface.component import ComponentInterface
from wenet.common.interface.exceptions import AuthenticationException, NotFound, CreationError
from wenet.common.interface.service_api import ServiceApiInterface
from wenet.common.model.app.app_dto import AppDTO
from wenet.common.model.logging_messages.contents import ActionRequest
from wenet.common.model.logging_messages.messages import RequestMessage
from wenet.common.model.task.task import Task, TaskGoal, TaskPage
from wenet.common.model.task.transaction import TaskTransaction
from wenet.common.model.user.token_details import TokenDetails
from wenet.common.model.user.user_profile import WeNetUserProfile, CoreWeNetUserProfile


class TestServiceApiInterface(TestCase):

    def test_creation(self):
        with self.assertRaises(AuthenticationException):
            ServiceApiInterface(NoAuthenticationClient())
        internal_service_api = ServiceApiInterface(MockApikeyClient())
        self.assertIsInstance(internal_service_api, ServiceApiInterface)
        self.assertEqual(ComponentInterface.PRODUCTION_INSTANCE + internal_service_api.COMPONENT_PATH_INTERNAL_USAGE, internal_service_api._base_url)
        external_service_api = ServiceApiInterface(MockOauth2Client())
        self.assertIsInstance(external_service_api, ServiceApiInterface)
        self.assertEqual(ComponentInterface.PRODUCTION_INSTANCE + external_service_api.COMPONENT_PATH_EXTERNAL_USAGE, external_service_api._base_url)

    def setUp(self):
        super().setUp()
        self.service_api = ServiceApiInterface(MockOauth2Client())

    def test_get_token_details(self):
        response = MockResponse(TokenDetails("1", "app_id", []).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual(TokenDetails("1", "app_id", []), self.service_api.get_token_details())

        response.status_code = 500
        with self.assertRaises(Exception):
            self.service_api.get_token_details()

    def test_get_app_details(self):
        response = MockResponse(AppDTO(None, None, "app_id", None, None).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual(AppDTO(None, None, "app_id", None, None), self.service_api.get_app_details("app_id"))

        response.status_code = 404
        with self.assertRaises(NotFound):
            self.service_api.get_app_details("app_id")

        response.status_code = 500
        with self.assertRaises(Exception):
            self.service_api.get_app_details("app_id")

    def test_get_app_users(self):
        response = MockResponse(["user_id"])
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual(["user_id"], self.service_api.get_app_users("app_id"))

        response.status_code = 404
        with self.assertRaises(NotFound):
            self.service_api.get_app_users("app_id")

        response.status_code = 500
        with self.assertRaises(Exception):
            self.service_api.get_app_users("app_id")

    def test_create_task(self):
        task = Task(None, None, None, "", "", "", None, TaskGoal("", ""))
        response = MockResponse(None)
        response.status_code = 201
        self.service_api._client.post = Mock(return_value=response)
        self.assertIsNone(self.service_api.create_task(task))

        response.status_code = 400
        with self.assertRaises(CreationError):
            self.service_api.create_task(task)

    def test_get_task(self):
        response = MockResponse(Task("task_id", None, None, "", "", "", None, TaskGoal("", "")).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual(Task("task_id", None, None, "", "", "", None, TaskGoal("", "")), self.service_api.get_task("task_id"))

        response.status_code = 404
        with self.assertRaises(NotFound):
            self.service_api.get_task("task_id")

        response.status_code = 500
        with self.assertRaises(Exception):
            self.service_api.get_task("task_id")

    def test_create_task_transaction(self):
        transaction = TaskTransaction(None, "", "", 1, 1, "", None)
        response = MockResponse(None)
        response.status_code = 201
        self.service_api._client.post = Mock(return_value=response)
        self.assertIsNone(self.service_api.create_task_transaction(transaction))

        response.status_code = 400
        with self.assertRaises(CreationError):
            self.service_api.create_task_transaction(transaction)

    def test_get_user_profile(self):
        response = MockResponse(WeNetUserProfile.empty("user_id").to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual(WeNetUserProfile.empty("user_id"), self.service_api.get_user_profile("user_id"))

        response.status_code = 404
        with self.assertRaises(NotFound):
            self.service_api.get_user_profile("user_id")

        response.status_code = 500
        with self.assertRaises(Exception):
            self.service_api.get_user_profile("user_id")

    def test_create_user_profile(self):
        response = MockResponse(None)
        response.status_code = 200
        self.service_api._client.post = Mock(return_value=response)
        self.assertIsNone(self.service_api.create_user_profile("user_id"))

        response.status_code = 400
        with self.assertRaises(CreationError):
            self.service_api.create_user_profile("user_id")

    def test_update_user_profile(self):
        response = MockResponse(WeNetUserProfile.empty("user_id").to_repr())
        response.status_code = 200
        self.service_api._client.put = Mock(return_value=response)
        self.assertEqual(WeNetUserProfile.empty("user_id"), self.service_api.update_user_profile("user_id", CoreWeNetUserProfile.empty("user_id")))

        response.status_code = 404
        with self.assertRaises(NotFound):
            self.service_api.update_user_profile("user_id", CoreWeNetUserProfile.empty("user_id"))

        response.status_code = 500
        with self.assertRaises(Exception):
            self.service_api.update_user_profile("user_id", CoreWeNetUserProfile.empty("user_id"))

    def test_get_opened_tasks_of_user(self):
        response = MockResponse(TaskPage(0, 0, [Task("task_id", None, None, "", "", "", None, TaskGoal("", ""))]).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([Task("task_id", None, None, "", "", "", None, TaskGoal("", ""))], self.service_api.get_opened_tasks_of_user("user_id", "app_id"))

        response.status_code = 404
        with self.assertRaises(NotFound):
            self.service_api.get_opened_tasks_of_user("user_id", "app_id")

        response.status_code = 500
        with self.assertRaises(Exception):
            self.service_api.get_opened_tasks_of_user("user_id", "app_id")

    def test_get_tasks(self):
        response = MockResponse(TaskPage(0, 0, [Task("task_id", None, None, "", "", "", None, TaskGoal("", ""))]).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([Task("task_id", None, None, "", "", "", None, TaskGoal("", ""))], self.service_api.get_tasks("app_id"))

        response.status_code = 500
        with self.assertRaises(Exception):
            self.service_api.get_tasks("app_id")

    def test_get_all_tasks_of_application(self):
        response = MockResponse(TaskPage(0, 0, [Task("task_id", None, None, "", "", "", None, TaskGoal("", ""))]).to_repr())
        response.status_code = 200
        self.service_api._client.get = Mock(return_value=response)
        self.assertEqual([Task("task_id", None, None, "", "", "", None, TaskGoal("", ""))], self.service_api.get_all_tasks_of_application("app_id"))

        response.status_code = 404
        with self.assertRaises(NotFound):
            self.service_api.get_all_tasks_of_application("app_id")

        response.status_code = 500
        with self.assertRaises(Exception):
            self.service_api.get_all_tasks_of_application("app_id")

    def test_log_message(self):
        message = RequestMessage("message_id", "", "", "", ActionRequest(""))
        response = MockResponse(None)
        response.status_code = 201
        self.service_api._client.post = Mock(return_value=response)
        self.assertIsNone(self.service_api.log_message(message))

        response.status_code = 400
        with self.assertRaises(CreationError):
            self.service_api.log_message(message)

