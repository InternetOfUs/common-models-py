from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.logging_message.content import TextualContent, BaseContent, ActionContent, AttachmentContent, \
    LocationContent, Card, CarouselContent, ActionRequest


class TestActionContent(TestCase):
    def test_repr(self):
        button = ActionContent("text", "payload")
        self.assertEqual(button, BaseContent.from_repr(button.to_repr()))


class TestTextualContent(TestCase):
    def test_repr(self):
        content = TextualContent("text")
        content.with_button("button", "payload")
        self.assertEqual(content, BaseContent.from_repr(content.to_repr()))

    def test_repr2(self):

        payload = {
            "value": "val"
        }

        from_repr = TextualContent.from_repr(payload)
        self.assertIsInstance(from_repr, TextualContent)
        self.assertEqual(payload["value"], from_repr.value)


class TestAttachmentContent(TestCase):
    def test_repr(self):
        content = AttachmentContent("uri", "alt")
        content.with_button("button", "payload")
        self.assertEqual(content, BaseContent.from_repr(content.to_repr()))


class TestLocationContent(TestCase):
    def test_repr(self):
        content = LocationContent(12.4235, 33.0045)
        content.with_button("button", "payload")
        self.assertEqual(content, BaseContent.from_repr(content.to_repr()))


class TestCard(TestCase):
    def test_repr(self):
        card = Card("title", "image url", "subtitle", {"action": "value"})
        card.with_button("button", "payload")
        self.assertEqual(card, Card.from_repr(card.to_repr()))


class TestCarouselContent(TestCase):
    def test_repr(self):
        cards = [
            Card("title", "image url", "subtitle", {"action": "value"})
                .with_button("button", "payload")
                .with_button("button", "payload"),
            Card("title", "image url", "subtitle", {"action": "value"})
                .with_button("button", "payload")
                .with_button("button", "payload"),
        ]
        content = CarouselContent(cards)
        self.assertEqual(content, BaseContent.from_repr(content.to_repr()))


class TestActionRequest(TestCase):
    def test_repr(self):
        content = ActionRequest("value")
        self.assertEqual(content, ActionRequest.from_repr(content.to_repr()))
