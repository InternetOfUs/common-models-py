from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.common.model.task.transaction import TaskTransaction


class TestTaskTransaction(TestCase):

    def test_repr(self):
        task_transaction = TaskTransaction("taskId", "taskLabel", {"key": "value"})

        from_repr = TaskTransaction.from_repr(task_transaction.to_repr())

        self.assertIsInstance(from_repr, TaskTransaction)
        self.assertEqual(task_transaction, from_repr)

    def test_equals(self):
        task_transaction = TaskTransaction("taskId", "taskLabel", {"key": "value"})
        task_transaction1 = TaskTransaction("taskId", "taskLabel", {"key": "value"})
        task_transaction2 = TaskTransaction("taskId1", "taskLabel", {"key": "value"})
        task_transaction3 = TaskTransaction("taskId", "taskLabel1", {"key": "value"})
        task_transaction4 = TaskTransaction("taskId", "taskLabel", {"key": "value1"})
        task_transaction5 = TaskTransaction("taskId", "taskLabel", {"key": "value", "key2": "value"})
        
        self.assertEqual(task_transaction, task_transaction1)
        self.assertNotEqual(task_transaction, task_transaction2)
        self.assertNotEqual(task_transaction, task_transaction3)
        self.assertNotEqual(task_transaction, task_transaction4)
        self.assertNotEqual(task_transaction, task_transaction5)
