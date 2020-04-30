import random
from unittest import TestCase
from uuid import uuid4

from wenet.common.messages.builder import MessageBuilder
from wenet.common.messages.exceptions import MessageTypeError, NotificationTypeError
from wenet.common.messages.models import TextualMessage, Message, TaskProposalNotification, TaskNotification, \
    TaskVolunteerNotification, MessageFromUserNotification, TaskConcludedNotification, NewUserForPlatform, BaseMessage, \
    Event


class TestBuilder(TestCase):
    def test_incoming_textual_message_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        raw_message = {
            "type": Message.TYPE_TEXTUAL_MESSAGE,
            "recipient_id": recipient,
            "title": title,
            "text": text
        }
        message = MessageBuilder.build(raw_message)
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
        raw_message = {
            "type": Message.TYPE_TASK_NOTIFICATION,
            "notification_type": TaskNotification.NOTIFICATION_TYPE_PROPOSAL,
            "title": title,
            "text": text,
            "recipient_id": recipient,
            "task_id": task_id,
            "description": description
        }
        message = MessageBuilder.build(raw_message)
        self.assertIsInstance(message, TaskProposalNotification)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)
        self.assertEqual(recipient, message.recipient_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(description, message.description)
        self.assertEqual(Message.TYPE_TASK_NOTIFICATION, message.type)
        self.assertEqual(TaskNotification.NOTIFICATION_TYPE_PROPOSAL, message.notification_type)

    def test_notification_volunteer_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        task_id = str(uuid4())
        description = str(uuid4())
        raw_message = {
            "type": Message.TYPE_TASK_NOTIFICATION,
            "notification_type": TaskNotification.NOTIFICATION_TYPE_VOLUNTEER,
            "title": title,
            "text": text,
            "recipient_id": recipient,
            "task_id": task_id,
            "description": description
        }
        message = MessageBuilder.build(raw_message)
        self.assertIsInstance(message, TaskVolunteerNotification)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)
        self.assertEqual(recipient, message.recipient_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(description, message.description)
        self.assertEqual(Message.TYPE_TASK_NOTIFICATION, message.type)
        self.assertEqual(TaskNotification.NOTIFICATION_TYPE_VOLUNTEER, message.notification_type)

    def test_message_from_user_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        task_id = str(uuid4())
        description = str(uuid4())
        sender = str(uuid4())
        raw_message = {
            "type": Message.TYPE_TASK_NOTIFICATION,
            "notification_type": TaskNotification.NOTIFICATION_TYPE_MESSAGE_FROM_USER,
            "title": title,
            "text": text,
            "recipient_id": recipient,
            "task_id": task_id,
            "description": description,
            "sender_id": sender
        }
        message = MessageBuilder.build(raw_message)
        self.assertIsInstance(message, MessageFromUserNotification)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)
        self.assertEqual(recipient, message.recipient_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(description, message.description)
        self.assertEqual(Message.TYPE_TASK_NOTIFICATION, message.type)
        self.assertEqual(TaskNotification.NOTIFICATION_TYPE_MESSAGE_FROM_USER, message.notification_type)
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
        raw_message = {
            "type": Message.TYPE_TASK_NOTIFICATION,
            "notification_type": TaskNotification.NOTIFICATION_TYPE_CONCLUDED,
            "title": title,
            "text": text,
            "recipient_id": recipient,
            "task_id": task_id,
            "description": description,
            "outcome": outcome
        }
        message = MessageBuilder.build(raw_message)
        self.assertIsInstance(message, TaskConcludedNotification)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)
        self.assertEqual(recipient, message.recipient_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(description, message.description)
        self.assertEqual(Message.TYPE_TASK_NOTIFICATION, message.type)
        self.assertEqual(TaskNotification.NOTIFICATION_TYPE_CONCLUDED, message.notification_type)
        self.assertEqual(outcome, message.outcome)

    def test_wrong_message_type_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        recipient = str(uuid4())
        raw_message = {
            "type": "puppa",
            "recipient_id": recipient,
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
            "type": Message.TYPE_TASK_NOTIFICATION,
            "notification_type": "puppa",
            "title": title,
            "text": text,
            "recipient_id": recipient,
            "task_id": task_id,
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
        self.assertEqual(BaseMessage.TYPE_EVENT, message.type)
        self.assertEqual(Event.TYPE_NEW_USER, message.event_type)
