from __future__ import absolute_import, annotations

import abc
from typing import List, Optional


class BaseContent(abc.ABC):
    """
    Base class of the contents of logging messages, containing the actual messages exchanged between users,
    applications and the Wenet platform
    """

    def __init__(self) -> None:
        self.type = self.get_type()

    @staticmethod
    @abc.abstractmethod
    def get_type() -> str:
        """
        Get a string describing the type of the content class
        """
        pass

    def to_repr(self) -> dict:
        return {
            "type": self.type
        }

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BaseContent):
            return False
        return self.type == o.type

    @staticmethod
    def from_repr(raw: dict) -> BaseContent:
        content_type = raw["type"]
        if content_type == TextualContent.get_type():
            return TextualContent.from_repr(raw)
        elif content_type == ActionContent.get_type():
            return ActionContent.from_repr(raw)
        elif content_type == AttachmentContent.get_type():
            return AttachmentContent.from_repr(raw)
        elif content_type == LocationContent.get_type():
            return LocationContent.from_repr(raw)
        elif content_type == CarouselContent.get_type():
            return CarouselContent.from_repr(raw)
        raise TypeError(f"Unexpected type [{content_type}] of content")


class ContentWithButtons(BaseContent, abc.ABC):
    """
    Abstract class with an array of buttons
    """

    def __init__(self, buttons: Optional[List[ActionContent]] = None) -> None:
        super().__init__()
        self.buttons = buttons
        if not self.buttons:
            self.buttons = []

    def with_action_response(self, button: ActionContent) -> ContentWithButtons:
        self.buttons.append(button)
        return self

    def with_button(self, text: str, intent: str) -> ContentWithButtons:
        self.buttons.append(ActionContent(text, intent))
        return self

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr.update({
            "buttons": [b.to_repr() for b in self.buttons]
        })
        return base_repr

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ContentWithButtons):
            return False
        return self.type == o.type and self.buttons == o.buttons


class ActionContent(BaseContent):
    """
    A button with a text and a payload
    """
    TYPE = "action"

    def __init__(self, button_text: str, button_payload: str) -> None:
        super().__init__()
        self.button_text = button_text
        self.button_payload = button_payload

    @staticmethod
    def get_type() -> str:
        return ActionContent.TYPE

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ActionContent):
            return False
        return self.type == o.type and self.button_text == o.button_text and self.button_payload == o.button_payload

    def to_repr(self) -> dict:
        return {
            "type": self.type,
            "buttonText": self.button_text,
            "buttonId": self.button_payload,
        }

    @staticmethod
    def from_repr(raw: dict) -> ActionContent:
        return ActionContent(
            raw["buttonText"],
            raw["buttonId"]
        )


class TextualContent(ContentWithButtons):
    """
    A content made of text, and optionally containing some buttons
    """
    TYPE = "text"

    @staticmethod
    def get_type() -> str:
        return TextualContent.TYPE

    def __init__(self, value: str, buttons: Optional[List[ActionContent]] = None) -> None:
        super().__init__(buttons)
        self.value = value

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr.update({
            "value": self.value,
        })
        return base_repr

    @staticmethod
    def from_repr(raw: dict) -> BaseContent:
        return TextualContent(
            raw["value"],
            [ActionContent.from_repr(b) for b in raw.get("buttons", [])]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TextualContent):
            return False
        return super().__eq__(o) and self.value == o.value and self.buttons == o.buttons


class AttachmentContent(ContentWithButtons):
    """
    A content containing an URI attachment
    """
    TYPE = "attachment"

    @staticmethod
    def get_type() -> str:
        return AttachmentContent.TYPE

    def __init__(self, uri: str, alternative_text: Optional[str] = None,
                 buttons: Optional[List[ActionContent]] = None) -> None:
        super().__init__(buttons)
        self.uri = uri
        self.alternative_text = alternative_text

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr.update({
            "uri": self.uri,
            "alternativeText": self.alternative_text,
        })
        return base_repr

    @staticmethod
    def from_repr(raw: dict) -> AttachmentContent:
        return AttachmentContent(
            raw["uri"],
            raw["alternativeText"],
            [ActionContent.from_repr(b) for b in raw["buttons"]]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, AttachmentContent):
            return False
        return super().__eq__(o) and self.uri == o.uri and self.alternative_text == o.alternative_text


class LocationContent(ContentWithButtons):
    """
    Content with lat & lon location
    """
    TYPE = "location"

    @staticmethod
    def get_type() -> str:
        return LocationContent.TYPE

    def __init__(self, lat: float, lon: float, buttons: Optional[List[ActionContent]] = None) -> None:
        super().__init__(buttons)
        self.lat = lat
        self.lon = lon

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, LocationContent):
            return False
        return super().__eq__(o) and self.lat == o.lat and self.lon == o.lon

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr.update({
            "lat": self.lat,
            "lon": self.lon,
        })
        return base_repr

    @staticmethod
    def from_repr(raw: dict) -> LocationContent:
        return LocationContent(
            raw["lat"],
            raw["lon"],
            [ActionContent.from_repr(b) for b in raw["buttons"]]
        )


class Card(ContentWithButtons):
    """
    A card of a carousel
    """
    TYPE = "card"

    @staticmethod
    def get_type() -> str:
        return Card.TYPE

    def __init__(self, title: str, image_url: Optional[str] = None, subtitle: Optional[str] = None,
                 default_action: Optional[dict] = None, buttons: Optional[List[ActionContent]] = None) -> None:
        super().__init__(buttons)
        self.title = title
        self.image_url = image_url
        self.subtitle = subtitle
        self.default_action = default_action
        if not self.default_action:
            self.default_action = {}

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Card):
            return False
        return super().__eq__(o) and self.title == o.title and self.subtitle == o.subtitle and \
            self.image_url == o.image_url and self.default_action == o.default_action

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr.update({
            "title": self.title,
            "subtitle": self.subtitle,
            "imageUrl": self.image_url,
            "defaultAction": self.default_action,
        })
        return base_repr

    @staticmethod
    def from_repr(raw: dict) -> Card:
        return Card(
            raw["title"],
            raw["imageUrl"],
            raw["subtitle"],
            raw["defaultAction"],
            [ActionContent.from_repr(b) for b in raw["buttons"]]
        )


class CarouselContent(BaseContent):
    """
    A carousel content with a list of cards
    """
    TYPE = "carousel"

    @staticmethod
    def get_type() -> str:
        return CarouselContent.TYPE

    def __init__(self, cards: List[Card]) -> None:
        super().__init__()
        self.cards = cards

    def with_card(self, card: Card) -> CarouselContent:
        self.cards.append(card)
        return self

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, CarouselContent):
            return False
        return super().__eq__(o) and self.cards == o.cards

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr.update({
            "cards": [c.to_repr() for c in self.cards]
        })
        return base_repr

    @staticmethod
    def from_repr(raw: dict) -> CarouselContent:
        return CarouselContent(
            [Card.from_repr(c) for c in raw["cards"]]
        )
