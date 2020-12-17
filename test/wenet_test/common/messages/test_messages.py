import random
from unittest import TestCase
from uuid import uuid4

from wenet.common.model.message.message import Message, TextualMessage, TaskProposalNotification, \
    TaskVolunteerNotification, TaskSelectionNotification, TaskConcludedNotification


class TestMessage(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        community_id = str(uuid4())
        receiver_id = str(uuid4())
        task_id = str(uuid4())
        label = str(uuid4())
        attributes = {"key": "value"}
        message = Message(app_id, community_id, task_id, receiver_id, label, attributes)
        message_repr = message.to_repr()
        self.assertEqual(Message.from_repr(message_repr), message)


class TestTextualMessage(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        community_id = str(uuid4())
        receiver_id = str(uuid4())
        task_id = str(uuid4())
        title = str(uuid4())
        text = str(uuid4())
        message = TextualMessage(app_id, community_id, task_id, receiver_id, title, text)
        message_repr = message.to_repr()
        self.assertEqual(Message.from_repr(message_repr), message)
        self.assertEqual(TextualMessage.LABEL, message.label)


class TestTaskProposalNotification(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        community_id = str(uuid4())
        receiver_id = str(uuid4())
        task_id = str(uuid4())
        notification = TaskProposalNotification(app_id, community_id, task_id, receiver_id)
        notification_repr = notification.to_repr()
        self.assertEqual(TaskProposalNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskProposalNotification.LABEL, notification.label)


class TestTaskConcludedNotification(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        community_id = str(uuid4())
        receiver_id = str(uuid4())
        task_id = str(uuid4())
        possible_outcomes = [TaskConcludedNotification.OUTCOME_FAILED, TaskConcludedNotification.OUTCOME_COMPLETED,
                             TaskConcludedNotification.OUTCOME_CANCELLED]
        outcome = random.choice(possible_outcomes)
        notification = TaskConcludedNotification(app_id, community_id, task_id, receiver_id, outcome)
        notification_repr = notification.to_repr()
        self.assertEqual(TaskConcludedNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskConcludedNotification.LABEL, notification.label)


class TestTaskSelectionNotification(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        community_id = str(uuid4())
        receiver_id = str(uuid4())
        task_id = str(uuid4())
        possible_outcomes = [TaskSelectionNotification.OUTCOME_REFUSED, TaskSelectionNotification.OUTCOME_ACCEPTED]
        outcome = random.choice(possible_outcomes)
        notification = TaskSelectionNotification(app_id, community_id, task_id, receiver_id, outcome)
        notification_repr = notification.to_repr()
        self.assertEqual(TaskSelectionNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskSelectionNotification.LABEL, notification.label)


class TestTaskVolunteerNotification(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        community_id = str(uuid4())
        receiver_id = str(uuid4())
        task_id = str(uuid4())
        volunteer_id = str(uuid4())
        notification = TaskVolunteerNotification(app_id, community_id, task_id, receiver_id, volunteer_id)
        notification_repr = notification.to_repr()
        self.assertEqual(TaskVolunteerNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskVolunteerNotification.LABEL, notification.label)
