from __future__ import absolute_import, annotations

from datetime import datetime
from unittest import TestCase

import pytz

from wenet.model.user.planned_activity import PlannedActivity, ActivityStatus


class TestPlannedActivity(TestCase):

    def test_repr(self):
        activity = PlannedActivity(
            activity_id="activity_id",
            start_time=datetime.now(tz=pytz.UTC),
            end_time=datetime.now(tz=pytz.UTC),
            description="description",
            attendees=["user_id"],
            status=ActivityStatus.CONFIRMED
        )

        to_repr = activity.to_repr()
        from_repr = PlannedActivity.from_repr(to_repr)

        self.assertIsInstance(from_repr, PlannedActivity)
        self.assertEqual(activity, from_repr)

    def test_wrong_start_time(self):
        with self.assertRaises(ValueError):
            activity = PlannedActivity(
                activity_id="activity_id",
                start_time=datetime.now(),
                end_time=datetime.now(tz=pytz.UTC),
                description="description",
                attendees=["user_id"],
                status=ActivityStatus.CONFIRMED
            )

    def test_wrong_end_time(self):
        with self.assertRaises(ValueError):
            activity = PlannedActivity(
                activity_id="activity_id",
                start_time=datetime.now(tz=pytz.UTC),
                end_time=datetime.now(),
                description="description",
                attendees=["user_id"],
                status=ActivityStatus.CONFIRMED
            )
