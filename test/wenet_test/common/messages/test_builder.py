import random
from unittest import TestCase
from uuid import uuid4

from wenet.common.model.message.builder import MessageBuilder
from wenet.common.model.message.exception import MessageTypeError, NotificationTypeError
from wenet.common.model.message.message import TextualMessage, TaskNotification, TaskProposalNotification, \
    TaskVolunteerNotification, MessageFromUserNotification, TaskConcludedNotification, NewUserForPlatform, Event, \
    TaskSelectionNotification


class TestBuilder(TestCase):
    def test_incoming_textual_message_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        raw_message = TextualMessage(recipient, title, text)
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TextualMessage)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)
        self.assertEqual(text, message.text)

    def test_notification_proposal_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        task_id = str(uuid4())
        description = str(uuid4())
        raw_message = TaskProposalNotification(recipient, title, text, description, task_id)
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TaskProposalNotification)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)
        self.assertEqual(recipient, message.recipient_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(description, message.description)
        self.assertEqual(TaskNotification.TYPE, message.type)
        self.assertEqual(TaskProposalNotification.TYPE, message.notification_type)

    def test_notification_volunteer_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        task_id = str(uuid4())
        description = str(uuid4())
        raw_message = TaskVolunteerNotification(recipient, title, text, description, task_id)
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TaskVolunteerNotification)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)
        self.assertEqual(recipient, message.recipient_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(description, message.description)
        self.assertEqual(TaskNotification.TYPE, message.type)
        self.assertEqual(TaskVolunteerNotification.TYPE, message.notification_type)

    def test_message_from_user_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        task_id = str(uuid4())
        description = str(uuid4())
        sender = str(uuid4())
        raw_message = MessageFromUserNotification(recipient, title, text, description, task_id, sender)
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, MessageFromUserNotification)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)
        self.assertEqual(recipient, message.recipient_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(description, message.description)
        self.assertEqual(TaskNotification.TYPE, message.type)
        self.assertEqual(MessageFromUserNotification.TYPE, message.notification_type)
        self.assertEqual(sender, message.sender_id)

    def test_message_task_concluded_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        task_id = str(uuid4())
        description = str(uuid4())
        outcome = random.choice([TaskConcludedNotification.OUTCOME_CANCELLED,
                                 TaskConcludedNotification.OUTCOME_SUCCESSFUL,
                                 TaskConcludedNotification.OUTCOME_FAILED])
        raw_message = TaskConcludedNotification(recipient, title, text, description, task_id, outcome)
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TaskConcludedNotification)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)
        self.assertEqual(recipient, message.recipient_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(description, message.description)
        self.assertEqual(TaskNotification.TYPE, message.type)
        self.assertEqual(TaskConcludedNotification.TYPE, message.notification_type)
        self.assertEqual(outcome, message.outcome)

    def test_wrong_message_type_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        raw_message = {
            "type": "puppa",
            "recipientId": recipient,
            "title": title,
            "text": text
        }
        self.assertRaises(MessageTypeError, MessageBuilder.build, raw_message)

    def test_wrong_notification_type_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        task_id = str(uuid4())
        description = str(uuid4())
        raw_message = {
            "type": TaskNotification.TYPE,
            "notificationType": "puppa",
            "title": title,
            "text": text,
            "recipientId": recipient,
            "taskId": task_id,
            "description": description
        }
        self.assertRaises(NotificationTypeError, MessageBuilder.build, raw_message)

    def testNewUserForPlatformType(self):
        app_id = str(uuid4())
        user_id = str(uuid4())
        platform = str(uuid4())
        new_user = NewUserForPlatform(app_id, user_id, platform)
        message = MessageBuilder.build(new_user.to_repr())
        self.assertIsInstance(message, NewUserForPlatform)
        self.assertEqual(app_id, message.app_id)
        self.assertEqual(user_id, message.user_id)
        self.assertEqual(platform, message.platform)
        self.assertEqual(Event.TYPE, message.type)
        self.assertEqual(NewUserForPlatform.TYPE, message.event_type)

    def testTaskSelectionNotification(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        task_id = str(uuid4())
        description = str(uuid4())
        outcome = random.choice([TaskSelectionNotification.OUTCOME_ACCEPTED,
                                 TaskSelectionNotification.OUTCOME_REFUSED])
        start_message = TaskSelectionNotification(recipient, title, text, description, task_id, outcome)
        message = MessageBuilder.build(start_message.to_repr())
        self.assertIsInstance(message, TaskSelectionNotification)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)
        self.assertEqual(recipient, message.recipient_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(description, message.description)
        self.assertEqual(TaskNotification.TYPE, message.type)
        self.assertEqual(TaskSelectionNotification.TYPE, message.notification_type)
        self.assertEqual(outcome, message.outcome)
