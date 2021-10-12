from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.user.relevant_location import RelevantLocation


class TestRelevantLocation(TestCase):

    def test_repr(self):
        relevant_location = RelevantLocation(
            location_id="location_id",
            label="label",
            latitude=67,
            longitude=134
        )

        to_repr = relevant_location.to_repr()
        from_repr = RelevantLocation.from_repr(to_repr)

        self.assertIsInstance(from_repr, RelevantLocation)
        self.assertEqual(relevant_location, from_repr)

    def test_wrong_latitude(self):
        with self.assertRaises(ValueError):
            relevant_location = RelevantLocation(
                location_id="location_id",
                label="label",
                latitude=97,
                longitude=134
            )

    def test_wrong_longitude(self):
        with self.assertRaises(ValueError):
            relevant_location = RelevantLocation(
                location_id="location_id",
                label="label",
                latitude=67,
                longitude=192
            )
