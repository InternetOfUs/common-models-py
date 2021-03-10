from unittest import TestCase

from wenet.common.model.task.task import Task, TaskGoal, TaskPage
from wenet.common.model.task.transaction import TaskTransaction


class TestTask(TestCase):
    def test_repr_with_transactions(self):
        transaction = TaskTransaction("transaction_id", "task_id", "label", 123456, 1234567, "actioneer", {})
        task = Task(
            "task_id",
            12345,
            67486,
            "type",
            "requester",
            "app_id",
            "community_id",
            TaskGoal("name", "description", ["key1", "key2"]),
            [],
            {"attribute": "value"},
            12345667,
            [transaction]
        )
        self.assertEqual(task, Task.from_repr(task.to_repr()))

    def test_repr_with_all_null_fields(self):
        task = Task(
            None,
            None,
            None,
            "type",
            "requester",
            "app_id",
            None,
            TaskGoal("name", "description")
        )
        self.assertEqual(task, Task.from_repr(task.to_repr()))

    def test_old_task_version(self):
        data = {
            "taskId": "task_id",
            "taskTypeId": "taskTypeId",
            "requesterId": "requesterId",
            "appId": "appId",
            "goal": {
                "name": "name",
                "description": "description",
            },
        }
        try:
            task = Task.from_repr(data)
            self.assertIsInstance(task, Task)
        except Exception:
            self.fail("From repr should not fail")

    def test_task_with_no_description(self):
        data = {
            "taskId": "task_id",
            "taskTypeId": "taskTypeId",
            "requesterId": "requesterId",
            "appId": "appId",
            "goal": {
                "name": "name",
            },
        }
        try:
            task = Task.from_repr(data)
            self.assertIsInstance(task, Task)
            self.assertEqual(task.goal.description, "")
        except Exception:
            self.fail("From repr should not fail")


class TestTaskPage(TestCase):
    def test_repr(self):
        task_page = TaskPage(0, 0, None)
        self.assertEqual(task_page, TaskPage.from_repr(task_page.to_repr()))

        task = Task(
            None,
            None,
            None,
            "type",
            "requester",
            "app_id",
            None,
            TaskGoal("name", "description")
        )
        task_page = TaskPage(0, 0, [task])
        self.assertEqual(task_page, TaskPage.from_repr(task_page.to_repr()))

    def test_null_task_repr(self):
        task_page_repr = {
            "offset": 0,
            "total": 0,
            "tasks": None
        }
        self.assertIsInstance(TaskPage.from_repr(task_page_repr), TaskPage)
