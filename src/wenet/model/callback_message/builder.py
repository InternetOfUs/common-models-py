from __future__ import absolute_import, annotations

from wenet.model.callback_message.event import Event, WeNetAuthenticationEvent


class EventBuilder:

    @staticmethod
    def build(raw_event: dict) -> Event:
        """
        Build an event from a raw representation
        :param raw_event: the raw event representation
        :return Event: the event model
        :raises KeyError:
        """
        event_type = raw_event["type"]
        if event_type == WeNetAuthenticationEvent.TYPE:
            event = WeNetAuthenticationEvent.from_repr(raw_event)
        else:
            event = Event.from_repr(raw_event)
        return event
