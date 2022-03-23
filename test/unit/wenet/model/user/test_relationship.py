from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.user.relationship import Relationship, RelationType


class TestCompetence(TestCase):

    def test_repr(self):
        relationship = Relationship(
            app_id="app_id",
            source_id="source_id",
            target_id="target_id",
            relation_type=RelationType.COLLEAGUE,
            weight=0.8
        )

        to_repr = relationship.to_repr()
        from_repr = Relationship.from_repr(to_repr)

        self.assertIsInstance(from_repr, Relationship)
        self.assertEqual(relationship, from_repr)

    def test_wrong_level(self):
        with self.assertRaises(ValueError):
             Relationship(
                app_id="app_id",
                source_id="source_id",
                target_id="user_id",
                relation_type=RelationType.COLLEAGUE,
                weight=2.8
            )
