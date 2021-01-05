import random
from unittest import TestCase
from uuid import uuid4

from wenet.common.model.message.message import Message, TextualMessage, TaskProposalNotification, \
    TaskVolunteerNotification, TaskSelectionNotification, TaskConcludedNotification, IncentiveMessage, IncentiveBadge, \
    QuestionToAnswerMessage, AnsweredQuestionMessage


class TestMessage(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        community_id = str(uuid4())
        receiver_id = str(uuid4())
        task_id = str(uuid4())
        label = str(uuid4())
        attributes = {
            "key": "value",
            "communityId": community_id,
            "taskId": task_id
        }
        message = Message(app_id, receiver_id, label, attributes)
        message_repr = message.to_repr()
        self.assertEqual(Message.from_repr(message_repr), message)
        self.assertEqual(message.task_id, task_id)
        self.assertEqual(message.community_id, community_id)

    def test_with_empty_attributes(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        label = str(uuid4())
        attributes = {
            "key": "value",
        }
        message = Message(app_id, receiver_id, label, attributes)
        message_repr = message.to_repr()
        self.assertEqual(Message.from_repr(message_repr), message)
        self.assertIsNone(message.community_id)
        self.assertIsNone(message.task_id)


class TestTextualMessage(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        title = str(uuid4())
        text = str(uuid4())
        message = TextualMessage(app_id, receiver_id, title, text, {})
        message_repr = message.to_repr()
        self.assertEqual(Message.from_repr(message_repr), message)
        self.assertEqual(TextualMessage.LABEL, message.label)


class TestTaskProposalNotification(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        notification = TaskProposalNotification(app_id, receiver_id, {})
        notification_repr = notification.to_repr()
        self.assertEqual(TaskProposalNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskProposalNotification.LABEL, notification.label)


class TestTaskConcludedNotification(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        possible_outcomes = [TaskConcludedNotification.OUTCOME_FAILED, TaskConcludedNotification.OUTCOME_COMPLETED,
                             TaskConcludedNotification.OUTCOME_CANCELLED]
        outcome = random.choice(possible_outcomes)
        notification = TaskConcludedNotification(app_id, receiver_id, outcome, {})
        notification_repr = notification.to_repr()
        self.assertEqual(TaskConcludedNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskConcludedNotification.LABEL, notification.label)


class TestTaskSelectionNotification(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        possible_outcomes = [TaskSelectionNotification.OUTCOME_REFUSED, TaskSelectionNotification.OUTCOME_ACCEPTED]
        outcome = random.choice(possible_outcomes)
        notification = TaskSelectionNotification(app_id, receiver_id, outcome, {})
        notification_repr = notification.to_repr()
        self.assertEqual(TaskSelectionNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskSelectionNotification.LABEL, notification.label)


class TestTaskVolunteerNotification(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        volunteer_id = str(uuid4())
        notification = TaskVolunteerNotification(app_id, receiver_id, volunteer_id, {})
        notification_repr = notification.to_repr()
        self.assertEqual(TaskVolunteerNotification.from_repr(notification_repr), notification)
        self.assertEqual(TaskVolunteerNotification.LABEL, notification.label)


class TestIncentiveMessage(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        issuer = str(uuid4())
        content = str(uuid4())
        message = IncentiveMessage(app_id, receiver_id, issuer, content, {})
        message_repr = message.to_repr()
        self.assertEqual(IncentiveMessage.from_repr(message_repr), message)
        self.assertEqual(IncentiveMessage.LABEL, message.label)


class TestIncentiveBadge(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        issuer = str(uuid4())
        image_url = str(uuid4())
        badge_class = str(uuid4())
        message = str(uuid4())
        criteria = str(uuid4())
        badge = IncentiveBadge(app_id, receiver_id, issuer, badge_class, image_url, criteria, message, {})
        self.assertEqual(IncentiveBadge.from_repr(badge.to_repr()), badge)
        self.assertEqual(IncentiveBadge.LABEL, badge.label)


class TestQuestionToAnswerMessage(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        question = str(uuid4())
        user_id = str(uuid4())
        message = QuestionToAnswerMessage(app_id, receiver_id, {}, question, user_id)
        self.assertEqual(QuestionToAnswerMessage.from_repr(message.to_repr()), message)
        self.assertEqual(question, message.question)
        self.assertEqual(user_id, message.user_id)


class TestAnsweredQuestionMessage(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        answer = str(uuid4())
        user_id = str(uuid4())
        transaction_id = str(uuid4())
        message = AnsweredQuestionMessage(app_id, receiver_id, answer, transaction_id, user_id, {})
        self.assertEqual(AnsweredQuestionMessage.from_repr(message.to_repr()), message)
        self.assertEqual(answer, message.answer)
        self.assertEqual(user_id, message.user_id)
        self.assertEqual(transaction_id, message.transaction_id)
