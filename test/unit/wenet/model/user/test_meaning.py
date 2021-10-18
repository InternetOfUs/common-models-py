from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.user.meaning import Meaning


class TestMeaning(TestCase):

    def test_repr(self):
        meaning = Meaning(
            name="name",
            category="category",
            level=0.8
        )

        to_repr = meaning.to_repr()
        from_repr = Meaning.from_repr(to_repr)

        self.assertIsInstance(from_repr, Meaning)
        self.assertEqual(meaning, from_repr)
