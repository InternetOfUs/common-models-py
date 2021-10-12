from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.protocol_norm import ProtocolNorm


class TestProtocolNorm(TestCase):

    def test_repr(self):
        norm = ProtocolNorm(
            description="description",
            whenever="whenever",
            thenceforth="thenceforth",
            ontology="ontology"
        )

        to_repr = norm.to_repr()
        from_repr = ProtocolNorm.from_repr(to_repr)

        self.assertIsInstance(from_repr, ProtocolNorm)
        self.assertEqual(norm, from_repr)
