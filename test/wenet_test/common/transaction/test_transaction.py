from unittest import TestCase

from wenet.common.model.message.message import TaskProposalNotification, TextualMessage
from wenet.common.model.task.transaction import TaskTransaction


class TestTransaction(TestCase):
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
