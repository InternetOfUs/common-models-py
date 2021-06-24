from __future__ import absolute_import, annotations

from unittest import TestCase
from unittest.mock import Mock

from test.wenet_test.common.interface.mock.client import MockApikeyClient, MockOauth2Client
from test.wenet_test.common.interface.mock.response import MockResponse
from wenet.common.interface.client import NoAuthenticationClient
from wenet.common.interface.exceptions import AuthenticationException
from wenet.common.interface.task_manager import TaskManagerInterface
from wenet.common.model.task.task import TaskPage, Task, TaskGoal
from wenet.common.model.task.transaction import TaskTransactionPage, TaskTransaction


class TestTaskManagerInterface(TestCase):

    def test_creation(self):
        with self.assertRaises(AuthenticationException):
            TaskManagerInterface(NoAuthenticationClient())
        self.assertIsInstance(TaskManagerInterface(MockApikeyClient()), TaskManagerInterface)
        with self.assertRaises(AuthenticationException):
            TaskManagerInterface(MockOauth2Client())

    def setUp(self):
        super().setUp()
        self.task_manager = TaskManagerInterface(MockApikeyClient())

    def test_get_tasks(self):
        response = MockResponse(TaskPage(0, 1, [Task("task_id", None, None, "", "", "app_id", None, TaskGoal("", ""))]).to_repr())
        response.status_code = 200
        self.task_manager._client.get = Mock(return_value=response)
        self.assertEqual([Task("task_id", None, None, "", "", "app_id", None, TaskGoal("", ""))], self.task_manager.get_tasks("app_id"))

        response.status_code = 404
        with self.assertRaises(Exception):
            self.task_manager.get_tasks("app_id")

    def test_get_transactions(self):
        response = MockResponse(TaskTransactionPage(0, 1, [TaskTransaction("transaction_id", "task_id", "", 1, 1, "", None)]).to_repr())
        response.status_code = 200
        self.task_manager._client.get = Mock(return_value=response)
        self.assertEqual([TaskTransaction("transaction_id", "task_id", "", 1, 1, "", None)], self.task_manager.get_transactions("app_id"))

        response.status_code = 404
        with self.assertRaises(Exception):
            self.task_manager.get_transactions("app_id")

    def test_get_task(self):
        response = MockResponse(Task("task_id", None, None, "", "", "app_id", None, TaskGoal("", "")).to_repr())
        response.status_code = 200
        self.task_manager._client.get = Mock(return_value=response)
        self.assertEqual(Task.from_repr(response.json()), self.task_manager.get_task("task_id"))

        response.status_code = 404
        with self.assertRaises(Exception):
            self.task_manager.get_task("task_id")

    def test_get_task_page(self):
        response = MockResponse(TaskPage(0, 1, [Task("task_id", None, None, "", "", "app_id", None, TaskGoal("", ""))]).to_repr())
        response.status_code = 200
        self.task_manager._client.get = Mock(return_value=response)
        self.assertEqual(TaskPage.from_repr(response.json()), self.task_manager.get_task_page("app_id"))

        response.status_code = 404
        with self.assertRaises(Exception):
            self.task_manager.get_task_page("app_id")

    def test_get_transaction_page(self):
        response = MockResponse(TaskTransactionPage(0, 1, [TaskTransaction("transaction_id", "task_id", "", 1, 1, "", None)]).to_repr())
        response.status_code = 200
        self.task_manager._client.get = Mock(return_value=response)
        self.assertEqual(TaskTransactionPage.from_repr(response.json()), self.task_manager.get_transaction_page("app_id"))

        response.status_code = 404
        with self.assertRaises(Exception):
            self.task_manager.get_transaction_page("app_id")

    def test_create_task(self):
        task = Task("task_id", None, None, "", "", "", None, TaskGoal("", ""))
        response = MockResponse(task.to_repr())
        response.status_code = 200
        self.task_manager._client.post = Mock(return_value=response)
        self.assertIsNone(self.task_manager.create_task(task))

        response.status_code = 400
        with self.assertRaises(Exception):
            self.task_manager.create_task(task)

    def test_update_task(self):
        task = Task("task_id", None, None, "", "", "", None, TaskGoal("", ""))
        response = MockResponse(task.to_repr())
        response.status_code = 200
        self.task_manager._client.put = Mock(return_value=response)
        self.assertIsNone(self.task_manager.update_task(task))

        response.status_code = 400
        with self.assertRaises(Exception):
            self.task_manager.update_task(task)

    def test_create_task_transaction(self):
        transaction = TaskTransaction(None, "", "", 1, 1, "", None)
        response = MockResponse(None)
        response.status_code = 200
        self.task_manager._client.post = Mock(return_value=response)
        self.assertIsNone(self.task_manager.create_task_transaction(transaction))

        response.status_code = 400
        with self.assertRaises(Exception):
            self.task_manager.create_task_transaction(transaction)
