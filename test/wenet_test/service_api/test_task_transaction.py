from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.common.model.task.task import TaskAttribute
from wenet.common.model.task.transaction import TaskTransaction


class TestTaskTransaction(TestCase):

    def test_repr(self):
        task_transaction = TaskTransaction("taskId", TaskTransaction.LABEL_TASK_COMPLETED, [TaskAttribute("name", "value")])

        from_repr = TaskTransaction.from_repr(task_transaction.to_repr())

        self.assertIsInstance(from_repr, TaskTransaction)
        self.assertEqual(task_transaction, from_repr)

    def test_equals(self):
        task_transaction = TaskTransaction("taskId", TaskTransaction.LABEL_TASK_COMPLETED, [TaskAttribute("name", "value")])
        task_transaction1 = TaskTransaction("taskId", TaskTransaction.LABEL_TASK_COMPLETED, [TaskAttribute("name", "value")])
        task_transaction2 = TaskTransaction("taskId1", TaskTransaction.LABEL_TASK_COMPLETED, [TaskAttribute("name", "value")])
        task_transaction3 = TaskTransaction("taskId", TaskTransaction.LABEL_REFUSE_TASK, [TaskAttribute("name", "value")])
        task_transaction4 = TaskTransaction("taskId", TaskTransaction.LABEL_TASK_COMPLETED, [TaskAttribute("name1", "value")])
        task_transaction5 = TaskTransaction("taskId", TaskTransaction.LABEL_TASK_COMPLETED, [TaskAttribute("name", "value"), TaskAttribute("name", "value")])
        
        self.assertEqual(task_transaction, task_transaction1)
        self.assertNotEqual(task_transaction, task_transaction2)
        self.assertNotEqual(task_transaction, task_transaction3)
        self.assertNotEqual(task_transaction, task_transaction4)
        self.assertNotEqual(task_transaction, task_transaction5)

    def test_wrong_label(self):
        self.assertRaises(ValueError, TaskTransaction, "taskId", "typeId", [])
