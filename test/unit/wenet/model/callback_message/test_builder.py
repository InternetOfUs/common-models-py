from __future__ import absolute_import, annotations

import random
from unittest import TestCase
from uuid import uuid4

from wenet.model.callback_message.builder import EventBuilder
from wenet.model.callback_message.event import Event, WeNetAuthenticationEvent


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
