from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.logging_message.content import TextualContent
from wenet.model.logging_message.message import RequestMessage, ResponseMessage, BaseMessage, \
    NotificationMessage


class TestRequestMessage(TestCase):
    def test_repr(self):
        content = TextualContent("text")
        content.with_button("button", "value")
        message = RequestMessage("message_id", "channel", "user_id", "project", content)
        self.assertEqual(message, BaseMessage.from_repr(message.to_repr()))


class TestResponseMessage(TestCase):
    def test_repr(self):
        content = TextualContent("text")
        content.with_button("button", "value")
        message = ResponseMessage("message_id", "channel", "user_id", "project", content, "responseTo")
        self.assertEqual(message, BaseMessage.from_repr(message.to_repr()))


class TestNotificationMessage(TestCase):
    def test_repr(self):
        content = TextualContent("text")
        content.with_button("button", "value")
        message = NotificationMessage("message_id", "channel", "user_id", "project", content)
        self.assertEqual(message, BaseMessage.from_repr(message.to_repr()))
