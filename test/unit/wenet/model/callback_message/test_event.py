from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.callback_message.event import Event


class TestEvent(TestCase):
    def test_repr(self):
        event = Event("type")
        self.assertEqual(event, Event.from_repr(event.to_repr()))
