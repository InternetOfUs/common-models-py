from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.user.competence import Competence


class TestCompetence(TestCase):

    def test_repr(self):
        competence = Competence(
            name="name",
            ontology="ontology",
            level=0.8
        )

        to_repr = competence.to_repr()
        from_repr = Competence.from_repr(to_repr)

        self.assertIsInstance(from_repr, Competence)
        self.assertEqual(competence, from_repr)

    def test_wrong_level(self):
        with self.assertRaises(ValueError):
            competence = Competence(
                name="name",
                ontology="ontology",
                level=2.8
            )
