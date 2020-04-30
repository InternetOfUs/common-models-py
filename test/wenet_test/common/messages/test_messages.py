import random
from unittest import TestCase
from uuid import uuid4

from wenet.common.messages.models import Message, TextualMessage, TaskNotification, TaskProposalNotification, \
    MessageFromUserNotification, TaskConcludedNotification, BaseMessage, Event, NewUserForPlatform


class TestBaseMessage(TestCase):
    def test_repr(self):
        types = [BaseMessage.TYPE_TEXTUAL_MESSAGE, BaseMessage.TYPE_TASK_NOTIFICATION, BaseMessage.TYPE_EVENT]
        message = BaseMessage(random.choice(types))
        message_repr = message.to_repr()
        self.assertEqual(BaseMessage.from_repr(message_repr), message)

    def test_strict_types(self):
        type = str(uuid4())
        self.assertRaises(ValueError, BaseMessage, type)


class TestMessage(TestCase):
    def test_repr(self):
        types = [Message.TYPE_TEXTUAL_MESSAGE, Message.TYPE_TASK_NOTIFICATION]
        recipient_id = str(uuid4())
        title = str(uuid4())
        text = str(uuid4())
        message = Message(random.choice(types), recipient_id, title, text)
        message_repr = message.to_repr()
        self.assertEqual(Message.from_repr(message_repr), message)


class TestTextualMessage(TestCase):
    def test_repr(self):
        recipient_id = str(uuid4())
        title = str(uuid4())
        text = str(uuid4())
        message = TextualMessage(recipient_id, title, text)
        message_repr = message.to_repr()
        self.assertEqual(Message.from_repr(message_repr), message)
        self.assertEqual(Message.TYPE_TEXTUAL_MESSAGE, message.type)


class TestTaskNotification(TestCase):
    def test_repr(self):
        recipient_id = str(uuid4())
        title = str(uuid4())
        text = str(uuid4())
        description = str(uuid4())
        task_id = str(uuid4())
        types = [TaskNotification.NOTIFICATION_TYPE_MESSAGE_FROM_USER, TaskNotification.NOTIFICATION_TYPE_CONCLUDED,
                 TaskNotification.NOTIFICATION_TYPE_VOLUNTEER, TaskNotification.NOTIFICATION_TYPE_PROPOSAL]
        type = random.choice(types)
        notification = TaskNotification(recipient_id, title, text, description, task_id, type)
        notification_repr = notification.to_repr()
        self.assertEqual(TaskNotification.from_repr(notification_repr), notification)
        self.assertEqual(Message.TYPE_TASK_NOTIFICATION, notification.type)


class TestTaskProposalNotification(TestCase):
    def test_repr(self):
        recipient_id = str(uuid4())
        title = str(uuid4())
        text = str(uuid4())
        description = str(uuid4())
        task_id = str(uuid4())
        notification = TaskProposalNotification(recipient_id, title, text, description, task_id)
        notification_repr = notification.to_repr()
        self.assertEqual(TaskProposalNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskNotification.NOTIFICATION_TYPE_PROPOSAL, notification.notification_type)


class TestMessageFromUserNotification(TestCase):
    def test_repr(self):
        recipient_id = str(uuid4())
        title = str(uuid4())
        text = str(uuid4())
        description = str(uuid4())
        task_id = str(uuid4())
        sender_id = str(uuid4())
        notification = MessageFromUserNotification(recipient_id, title, text, description, task_id, sender_id)
        notification_repr = notification.to_repr()
        self.assertEqual(MessageFromUserNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskNotification.NOTIFICATION_TYPE_MESSAGE_FROM_USER, notification.notification_type)


class TestTaskConcludedNotification(TestCase):
    def test_repr(self):
        recipient_id = str(uuid4())
        title = str(uuid4())
        text = str(uuid4())
        description = str(uuid4())
        task_id = str(uuid4())
        possible_outcomes = [TaskConcludedNotification.OUTCOME_FAILED, TaskConcludedNotification.OUTCOME_SUCCESSFUL,
                             TaskConcludedNotification.OUTCOME_CANCELLED]
        outcome = random.choice(possible_outcomes)
        notification = TaskConcludedNotification(recipient_id, title, text, description, task_id, outcome)
        notification_repr = notification.to_repr()
        self.assertEqual(TaskConcludedNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskNotification.NOTIFICATION_TYPE_CONCLUDED, notification.notification_type)


class TestEvent(TestCase):
    def test_repr(self):
        event = Event(Event.TYPE_NEW_USER)
        event_repr = event.to_repr()
        self.assertEqual(Event.from_repr(event_repr), event)


class TestNewUserForPlatform(TestCase):
    def test_repr(self):
        message = NewUserForPlatform(str(uuid4()), str(uuid4()), str(uuid4()))
        message_repr = message.to_repr()
        self.assertEqual(NewUserForPlatform.from_repr(message_repr), message)
