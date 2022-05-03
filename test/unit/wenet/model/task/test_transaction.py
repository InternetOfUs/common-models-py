from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.callback_message.message import TaskProposalNotification, TextualMessage
from wenet.model.task.transaction import TaskTransaction, TaskTransactionPage


class TestTransaction(TestCase):

    def test_repr_empty(self):
        task_transaction = TaskTransaction("transaction_id", "taskId", "taskLabel", 123, 123, "actioneer_id",
                                           {"key": "value"}, [])

        from_repr = TaskTransaction.from_repr(task_transaction.to_repr())

        self.assertIsInstance(from_repr, TaskTransaction)
        self.assertEqual(task_transaction, from_repr)

    def test_equals(self):
        task_transaction = TaskTransaction("transaction_id", "taskId", "taskLabel", 123, 123, "actioneer_id",
                                           {"key": "value"})
        task_transaction1 = TaskTransaction("transaction_id", "taskId", "taskLabel", 123, 123, "actioneer_id",
                                            {"key": "value"})
        task_transaction2 = TaskTransaction("transaction_id", "taskId1", "taskLabel", 123, 123, "actioneer_id",
                                            {"key": "value"})
        task_transaction3 = TaskTransaction("transaction_id", "taskId", "taskLabel1", 123, 123, "actioneer_id",
                                            {"key": "value"})
        task_transaction4 = TaskTransaction("transaction_id", "taskId", "taskLabel", 123, 123, "actioneer_id",
                                            {"key": "value1"})
        task_transaction5 = TaskTransaction("transaction_id", "taskId", "taskLabel", 123, 123, "actioneer_id",
                                            {"key": "value", "key2": "value"})

        self.assertEqual(task_transaction, task_transaction1)
        self.assertNotEqual(task_transaction, task_transaction2)
        self.assertNotEqual(task_transaction, task_transaction3)
        self.assertNotEqual(task_transaction, task_transaction4)
        self.assertNotEqual(task_transaction, task_transaction5)

    def test_repr(self):
        message_1 = TaskProposalNotification("app_id", "receiver_id", {
            "communityId": "communityId",
            "taskId": "taskID",
        })
        message_2 = TextualMessage("app_id", "receiver_id", "title", "text", {
            "communityId": "communityId",
            "taskId": "taskID",
        })
        transaction = TaskTransaction("transaction_id", "task_id", "label", 123456, 1234567, "actioneer", {},
                                      [message_1, message_2])
        self.assertEqual(transaction, TaskTransaction.from_repr(transaction.to_repr()))

    def test_repr_without_messages(self):
        transaction = TaskTransaction("transaction_id", "task_id", "label", 123456, 1234567, "actioneer", {})
        self.assertEqual(transaction, TaskTransaction.from_repr(transaction.to_repr()))

    def test_repr_without_id(self):
        transaction = TaskTransaction(None, "task_id", "label", 123456, 1234567, "actioneer", {})
        self.assertEqual(transaction, TaskTransaction.from_repr(transaction.to_repr()))

    def test_repr_without_creation_ts(self):
        transaction = TaskTransaction(None, "task_id", "label", None, 1234567, "actioneer", {})
        to_repr = transaction.to_repr()

        self.assertNotIn("_creationTs", to_repr)
        self.assertEqual(transaction, TaskTransaction.from_repr(to_repr))

    def test_repr_without_last_update_ts(self):
        transaction = TaskTransaction(None, "task_id", "label", 1234567, None, "actioneer", {})
        to_repr = transaction.to_repr()

        self.assertNotIn("_lastUpdateTs", to_repr)
        self.assertEqual(transaction, TaskTransaction.from_repr(to_repr))


class TestTaskTransactionPage(TestCase):
    def test_repr(self):
        task_transaction_page = TaskTransactionPage(0, 0, None)
        self.assertEqual(task_transaction_page, TaskTransactionPage.from_repr(task_transaction_page.to_repr()))

        transaction = TaskTransaction(
            None,
            "task_id",
            "label",
            123456,
            1234567,
            "actioneer",
            None
        )
        task_transaction_page = TaskTransactionPage(0, 0, [transaction])
        self.assertEqual(task_transaction_page, TaskTransactionPage.from_repr(task_transaction_page.to_repr()))

    def test_null_task_repr(self):
        task_transaction_page_repr = {
            "offset": 0,
            "total": 0,
            "transactions": None
        }
        self.assertIsInstance(TaskTransactionPage.from_repr(task_transaction_page_repr), TaskTransactionPage)
