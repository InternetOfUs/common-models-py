import random
from unittest import TestCase
from uuid import uuid4

from wenet.common.model.message.message import TextualMessage, TaskNotification, Event, BaseMessage, Message, \
    MessageFromUserNotification, TaskConcludedNotification, TaskVolunteerNotification, TaskProposalNotification, \
    NewUserForPlatform, TaskSelectionNotification


class TestBaseMessage(TestCase):
    def test_repr(self):
        types = [TextualMessage.TYPE, TaskNotification.TYPE, Event.TYPE]
        message = BaseMessage(random.choice(types))
        message_repr = message.to_repr()
        self.assertEqual(BaseMessage.from_repr(message_repr), message)

    def test_strict_types(self):
        type = str(uuid4())
        self.assertRaises(ValueError, BaseMessage, type)


class TestMessage(TestCase):
    def test_repr(self):
        types = [TextualMessage.TYPE, TaskNotification.TYPE]
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
        self.assertEqual(TextualMessage.TYPE, message.type)


class TestTaskNotification(TestCase):
    def test_repr(self):
        recipient_id = str(uuid4())
        title = str(uuid4())
        text = str(uuid4())
        description = str(uuid4())
        task_id = str(uuid4())
        types = [MessageFromUserNotification.TYPE, TaskConcludedNotification.TYPE,
                 TaskVolunteerNotification.TYPE, TaskProposalNotification.TYPE]
        type = random.choice(types)
        notification = TaskNotification(recipient_id, title, text, description, task_id, type)
        notification_repr = notification.to_repr()
        self.assertEqual(TaskNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskNotification.TYPE, notification.type)


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
        self.assertEqual(TaskProposalNotification.TYPE, notification.notification_type)


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
        self.assertEqual(MessageFromUserNotification.TYPE, notification.notification_type)


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
        self.assertEqual(TaskConcludedNotification.TYPE, notification.notification_type)


class TestEvent(TestCase):
    def test_repr(self):
        event = Event(NewUserForPlatform.TYPE)
        event_repr = event.to_repr()
        self.assertEqual(Event.from_repr(event_repr), event)


class TestNewUserForPlatform(TestCase):
    def test_repr(self):
        message = NewUserForPlatform(str(uuid4()), str(uuid4()), str(uuid4()))
        message_repr = message.to_repr()
        self.assertEqual(NewUserForPlatform.from_repr(message_repr), message)


class TestTaskSelectionNotification(TestCase):
    def test_repr(self):
        recipient_id = str(uuid4())
        title = str(uuid4())
        text = str(uuid4())
        description = str(uuid4())
        task_id = str(uuid4())
        possible_outcomes = [TaskSelectionNotification.OUTCOME_REFUSED, TaskSelectionNotification.OUTCOME_ACCEPTED]
        outcome = random.choice(possible_outcomes)
        notification = TaskSelectionNotification(recipient_id, title, text, description, task_id, outcome)
        notification_repr = notification.to_repr()
        self.assertEqual(TaskSelectionNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskSelectionNotification.TYPE, notification.notification_type)
