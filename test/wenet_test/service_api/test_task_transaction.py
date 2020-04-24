from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.service_api.task import TaskAttribute
from wenet.service_api.task_transaction import TaskTransaction


class TestTaskTransaction(TestCase):

    def test_repr(self):
        task_transaction = TaskTransaction("taskId", "typeId", [TaskAttribute("name", "value")])

        from_repr = TaskTransaction.from_repr(task_transaction.to_repr())

        self.assertIsInstance(from_repr, TaskTransaction)
        self.assertEqual(task_transaction, from_repr)

    def test_equals(self):
        task_transaction = TaskTransaction("taskId", "typeId", [TaskAttribute("name", "value")])
        task_transaction1 = TaskTransaction("taskId", "typeId", [TaskAttribute("name", "value")])
        task_transaction2 = TaskTransaction("taskId1", "typeId", [TaskAttribute("name", "value")])
        task_transaction3 = TaskTransaction("taskId", "typeId1", [TaskAttribute("name", "value")])
        task_transaction4 = TaskTransaction("taskId", "typeId", [TaskAttribute("name1", "value")])
        task_transaction5 = TaskTransaction("taskId", "typeId", [TaskAttribute("name", "value"), TaskAttribute("name", "value")])
        
        self.assertEqual(task_transaction, task_transaction1)
        self.assertNotEqual(task_transaction, task_transaction2)
        self.assertNotEqual(task_transaction, task_transaction3)
        self.assertNotEqual(task_transaction, task_transaction4)
        self.assertNotEqual(task_transaction, task_transaction5)
