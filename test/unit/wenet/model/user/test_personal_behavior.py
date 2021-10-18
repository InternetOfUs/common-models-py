from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.user.personal_behaviors import Label, ScoredLabel, PersonalBehavior


class TestLabel(TestCase):

    def test_repr(self):
        label = Label(
            name="name",
            semantic_class=1,
            latitude=67,
            longitude=134
        )

        to_repr = label.to_repr()
        from_repr = Label.from_repr(to_repr)

        self.assertIsInstance(from_repr, Label)
        self.assertEqual(label, from_repr)

    def test_wrong_latitude(self):
        with self.assertRaises(ValueError):
            label = Label(
                name="name",
                semantic_class=1,
                latitude=97,
                longitude=134
            )

    def test_wrong_longitude(self):
        with self.assertRaises(ValueError):
            label = Label(
                name="name",
                semantic_class=1,
                latitude=67,
                longitude=192
            )


class TestScoredLabel(TestCase):

    def test_repr(self):
        scored_label = ScoredLabel(
            label=Label(
                name="name",
                semantic_class=1,
                latitude=67,
                longitude=134
            ),
            score=0.7
        )

        to_repr = scored_label.to_repr()
        from_repr = ScoredLabel.from_repr(to_repr)

        self.assertIsInstance(from_repr, ScoredLabel)
        self.assertEqual(scored_label, from_repr)


class TestPersonalBehavior(TestCase):

    def test_repr(self):
        personal_behaviors = PersonalBehavior(
            user_id="user_id",
            weekday="monday",
            label_distribution={
                "slot": [ScoredLabel(
                    label=Label(
                        name="name",
                        semantic_class=1,
                        latitude=67,
                        longitude=134
                    ),
                    score=0.7
                )]
            },
            confidence=0.8
        )

        to_repr = personal_behaviors.to_repr()
        from_repr = PersonalBehavior.from_repr(to_repr)

        self.assertIsInstance(from_repr, PersonalBehavior)
        self.assertEqual(personal_behaviors, from_repr)
