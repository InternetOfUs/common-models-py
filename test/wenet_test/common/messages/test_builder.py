import random
from unittest import TestCase
from uuid import uuid4

from wenet.common.model.message.builder import MessageBuilder, EventBuilder
from wenet.common.model.message.event import Event, WeNetAuthenticationEvent
from wenet.common.model.message.message import TextualMessage, TaskProposalNotification, TaskVolunteerNotification, \
    TaskConcludedNotification, TaskSelectionNotification


class TestMessageBuilder(TestCase):
    def test_incoming_textual_message_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        receiver_id = str(uuid4())
        app_id = str(uuid4())
        community_id = str(uuid4())
        task_id = str(uuid4())
        raw_message = TextualMessage(app_id, community_id, task_id, receiver_id, title, text)
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TextualMessage)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)

    def test_notification_proposal_parsing(self):
        receiver_id = str(uuid4())
        app_id = str(uuid4())
        community_id = str(uuid4())
        task_id = str(uuid4())
        raw_message = TaskProposalNotification(app_id, community_id, task_id, receiver_id)
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TaskProposalNotification)
        self.assertEqual(receiver_id, message.receiver_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(TaskProposalNotification.LABEL, message.label)

    def test_notification_volunteer_parsing(self):
        receiver_id = str(uuid4())
        app_id = str(uuid4())
        community_id = str(uuid4())
        task_id = str(uuid4())
        volunteer_id = str(uuid4())
        raw_message = TaskVolunteerNotification(app_id, community_id, task_id, receiver_id, volunteer_id)
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TaskVolunteerNotification)
        self.assertEqual(receiver_id, message.receiver_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(volunteer_id, message.volunteer_id)
        self.assertEqual(TaskVolunteerNotification.LABEL, message.label)

    def test_message_task_concluded_parsing(self):
        receiver_id = str(uuid4())
        app_id = str(uuid4())
        community_id = str(uuid4())
        task_id = str(uuid4())
        outcome = random.choice([TaskConcludedNotification.OUTCOME_CANCELLED,
                                 TaskConcludedNotification.OUTCOME_COMPLETED,
                                 TaskConcludedNotification.OUTCOME_FAILED])
        raw_message = TaskConcludedNotification(app_id, community_id, task_id, receiver_id, outcome)
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TaskConcludedNotification)
        self.assertEqual(receiver_id, message.receiver_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(TaskConcludedNotification.LABEL, message.label)
        self.assertEqual(outcome, message.outcome)

    def testTaskSelectionNotification(self):
        receiver_id = str(uuid4())
        app_id = str(uuid4())
        community_id = str(uuid4())
        task_id = str(uuid4())
        outcome = random.choice([TaskSelectionNotification.OUTCOME_ACCEPTED,
                                 TaskSelectionNotification.OUTCOME_REFUSED])
        start_message = TaskSelectionNotification(app_id, community_id, task_id, receiver_id, outcome)
        message = MessageBuilder.build(start_message.to_repr())
        self.assertIsInstance(message, TaskSelectionNotification)
        self.assertEqual(receiver_id, message.receiver_id)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(TaskSelectionNotification.LABEL, message.label)
        self.assertEqual(outcome, message.outcome)


class TestEventBuilder(TestCase):
    def test_event(self):
        event_type = str(uuid4())
        event = Event(event_type)
        parsed_event = EventBuilder.build(event.to_repr())
        self.assertIsInstance(parsed_event, Event)
        self.assertEqual(parsed_event.event_type, event.event_type)

    def test_authentication_event(self):
        code = str(uuid4())
        external_id = str(uuid4())
        event = WeNetAuthenticationEvent(external_id, code)
        parsed_event = EventBuilder.build(event.to_repr())
        self.assertIsInstance(parsed_event, WeNetAuthenticationEvent)
        self.assertEqual(parsed_event.event_type, event.event_type)
        self.assertEqual(parsed_event.external_id, event.external_id)
        self.assertEqual(parsed_event.code, event.code)
