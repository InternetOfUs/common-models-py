from unittest import TestCase

from wenet.model.message.event import WeNetAuthenticationEvent, Event


class TestWeNetAuthenticationEvent(TestCase):
    def test_repr(self):
        auth_event = WeNetAuthenticationEvent("external id", "code")
        self.assertEqual(auth_event, WeNetAuthenticationEvent.from_repr(auth_event.to_repr()))


class TestEvent(TestCase):
    def test_repr(self):
        event = Event("type")
        self.assertEqual(event, Event.from_repr(event.to_repr()))
