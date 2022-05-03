from __future__ import absolute_import, annotations


class Event:
    """
    Generic event sent by Wenet to applications.

    Attributes:
        - event_type: a string defining the type of the event
    """

    def __init__(self, event_type: str) -> None:
        self.event_type = event_type

    def to_repr(self) -> dict:
        return {"type": self.event_type}

    @staticmethod
    def from_repr(raw: dict) -> Event:
        return Event(raw["type"])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Event):
            return False
        return self.event_type == o.event_type
