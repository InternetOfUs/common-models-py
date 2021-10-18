from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.user.material import Material


class TestMaterial(TestCase):

    def test_repr(self):
        material = Material(
            name="name",
            description="description",
            quantity=1,
            classification="classification"
        )

        to_repr = material.to_repr()
        from_repr = Material.from_repr(to_repr)

        self.assertIsInstance(from_repr, Material)
        self.assertEqual(material, from_repr)

    def test_wrong_quantity(self):
        with self.assertRaises(ValueError):
            material = Material(
                name="name",
                description="description",
                quantity=0,
                classification="classification"
            )
