from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.service_api.norm import Norm, NormOperator


class TestNorm(TestCase):

    def test_repr(self):
        norm = Norm(
            norm_id="norm-id",
            attribute="attribute",
            operator=NormOperator.EQUALS,
            comparison=True,
            negation=False
        )

        to_repr = norm.to_repr()
        from_repr = Norm.from_repr(to_repr)

        self.assertIsInstance(from_repr, Norm)
        self.assertEqual(norm, from_repr)

    def test_repr2(self):

        raw_norm = {
            "id": "norm-d",
            "attribute": "attribute",
            "operator": "EQUALS",
            "comparison": True,
            "negation": False
        }

        from_repr = Norm.from_repr(raw_norm)

        self.assertIsInstance(from_repr, Norm)
        self.assertEqual(raw_norm, from_repr.to_repr())

    def test_repr3(self):

        raw_norm = {
            "id": "norm-d",
            "attribute": "attribute",
            "operator": "EQUALS1",
            "comparison": True,
            "negation": False
        }

        self.assertRaises(
            ValueError,
            Norm.from_repr,
            raw_norm
        )
