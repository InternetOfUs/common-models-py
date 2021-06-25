from __future__ import absolute_import, annotations

import random
from unittest import TestCase
from uuid import uuid4

from wenet.model.callback_message.builder import MessageBuilder, EventBuilder
from wenet.model.callback_message.event import Event, WeNetAuthenticationEvent
from wenet.model.callback_message.message import TextualMessage, TaskProposalNotification, TaskVolunteerNotification, \
    TaskConcludedNotification, TaskSelectionNotification, IncentiveMessage, IncentiveBadge, QuestionToAnswerMessage, \
    AnsweredQuestionMessage


class TestMessageBuilder(TestCase):
    def test_incoming_textual_message_parsing(self):
        title = str(uuid4())
        text = str(uuid4())
        receiver_id = str(uuid4())
        app_id = str(uuid4())
        community_id = str(uuid4())
        task_id = str(uuid4())
        attributes = {
            "taskId": task_id,
            "communityId": community_id
        }
        raw_message = TextualMessage(app_id, receiver_id, title, text, attributes)
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TextualMessage)
        self.assertEqual(title, message.title)
        self.assertEqual(text, message.text)
        self.assertEqual(task_id, message.task_id)
        self.assertEqual(community_id, message.community_id)

    def test_notification_proposal_parsing(self):
        receiver_id = str(uuid4())
        app_id = str(uuid4())
        raw_message = TaskProposalNotification(app_id, receiver_id, {})
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TaskProposalNotification)
        self.assertEqual(receiver_id, message.receiver_id)
        self.assertIsNone(message.task_id)
        self.assertIsNone(message.community_id)
        self.assertEqual(TaskProposalNotification.LABEL, message.label)

    def test_notification_volunteer_parsing(self):
        receiver_id = str(uuid4())
        app_id = str(uuid4())
        volunteer_id = str(uuid4())
        raw_message = TaskVolunteerNotification(app_id, receiver_id, volunteer_id, {})
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TaskVolunteerNotification)
        self.assertEqual(receiver_id, message.receiver_id)
        self.assertEqual(volunteer_id, message.volunteer_id)
        self.assertEqual(TaskVolunteerNotification.LABEL, message.label)

    def test_message_task_concluded_parsing(self):
        receiver_id = str(uuid4())
        app_id = str(uuid4())
        outcome = random.choice([TaskConcludedNotification.OUTCOME_CANCELLED,
                                 TaskConcludedNotification.OUTCOME_COMPLETED,
                                 TaskConcludedNotification.OUTCOME_FAILED])
        raw_message = TaskConcludedNotification(app_id, receiver_id, outcome, {})
        message = MessageBuilder.build(raw_message.to_repr())
        self.assertIsInstance(message, TaskConcludedNotification)
        self.assertEqual(receiver_id, message.receiver_id)
        self.assertEqual(TaskConcludedNotification.LABEL, message.label)
        self.assertEqual(outcome, message.outcome)

    def testTaskSelectionNotification(self):
        receiver_id = str(uuid4())
        app_id = str(uuid4())
        outcome = random.choice([TaskSelectionNotification.OUTCOME_ACCEPTED,
                                 TaskSelectionNotification.OUTCOME_REFUSED])
        start_message = TaskSelectionNotification(app_id, receiver_id, outcome, {})
        message = MessageBuilder.build(start_message.to_repr())
        self.assertIsInstance(message, TaskSelectionNotification)
        self.assertEqual(receiver_id, message.receiver_id)
        self.assertEqual(TaskSelectionNotification.LABEL, message.label)
        self.assertEqual(outcome, message.outcome)

    def test_incentive_message(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        issuer = str(uuid4())
        content = str(uuid4())
        start_message = IncentiveMessage(app_id, receiver_id, issuer, content, {})
        message = MessageBuilder.build(start_message.to_repr())
        self.assertIsInstance(message, IncentiveMessage)
        self.assertEqual(receiver_id, message.receiver_id)
        self.assertEqual(IncentiveMessage.LABEL, message.label)
        self.assertEqual(issuer, message.issuer)
        self.assertEqual(content, message.content)

    def test_incentive_badge(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        issuer = str(uuid4())
        image_url = str(uuid4())
        badge_class = str(uuid4())
        badge_message = str(uuid4())
        criteria = str(uuid4())
        start_message = IncentiveBadge(app_id, receiver_id, issuer, badge_class, image_url, criteria, badge_message, {})
        message = MessageBuilder.build(start_message.to_repr())
        self.assertIsInstance(message, IncentiveBadge)
        self.assertEqual(receiver_id, message.receiver_id)
        self.assertEqual(IncentiveBadge.LABEL, message.label)
        self.assertEqual(issuer, message.issuer)
        self.assertEqual(image_url, message.image_url)
        self.assertEqual(badge_class, message.badge_class)
        self.assertEqual(badge_message, message.message)
        self.assertEqual(criteria, message.criteria)

    def test_question_to_answer_message(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        question = str(uuid4())
        user_id = str(uuid4())
        start_message = QuestionToAnswerMessage(app_id, receiver_id, {}, question, user_id)
        message = MessageBuilder.build(start_message.to_repr())
        self.assertIsInstance(message, QuestionToAnswerMessage)
        self.assertEqual(question, message.question)
        self.assertEqual(user_id, message.user_id)

    def test_answer_to_question_message(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        answer = str(uuid4())
        user_id = str(uuid4())
        transaction_id = str(uuid4())
        start_message = AnsweredQuestionMessage(app_id, receiver_id, answer, transaction_id, user_id, {})
        message = MessageBuilder.build(start_message.to_repr())
        self.assertIsInstance(message, AnsweredQuestionMessage)
        self.assertEqual(answer, message.answer)
        self.assertEqual(user_id, message.user_id)
        self.assertEqual(transaction_id, message.transaction_id)


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
