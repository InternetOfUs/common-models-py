from __future__ import absolute_import, annotations

from datetime import datetime
from enum import Enum
from typing import Optional, List

import dateparser
import pytz

from wenet.model.extended_property import ExtendedProperty


class ActivityStatus(Enum):

    CONFIRMED = "confirmed"
    TENTATIVE = "tentative"
    CANCELLED = "cancelled"


class PlannedActivity(ExtendedProperty):

    def __init__(self, activity_id: str, start_time: Optional[datetime], end_time: Optional[datetime],
                 description: Optional[str], attendees: Optional[List[str]], status: Optional[ActivityStatus]) -> None:
        """
        A planned activity

        Args:
            activity_id: The identifier of the activity
            start_time: The starting time of the activity (must have a timezone)
            end_time: The ending time of the activity (must have a timezone)
            description: The description of the activity
            attendees: The identifiers of other wenet users taking part to the activity
            status: The current status of the activity
        """
        self.activity_id = activity_id
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.attendees = attendees
        self.status = status

        if self.start_time is not None and self.start_time.tzinfo is None:
            raise ValueError("start_time has no time zone")

        if self.end_time is not None and self.end_time.tzinfo is None:
            raise ValueError("start_time has no time zone")

    def to_repr(self) -> dict:
        return {
            "id": self.activity_id,
            "startTime": self.start_time.astimezone(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.start_time is not None else None,
            "endTime": self.end_time.astimezone(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.end_time is not None else None,
            "description": self.description,
            "attendees": self.attendees,
            "status": self.status.value
        }

    @staticmethod
    def from_repr(raw_data: dict) -> PlannedActivity:
        return PlannedActivity(
            activity_id=raw_data["id"],
            start_time=dateparser.parse(raw_data["startTime"]) if raw_data.get("startTime", None) is not None else None,
            end_time=dateparser.parse(raw_data["endTime"]) if raw_data.get("endTime", None) is not None else None,
            description=raw_data.get("description", None),
            attendees=raw_data.get("attendees", None),
            status=ActivityStatus(raw_data["status"]) if raw_data.get("status", None) is not None else None,
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, PlannedActivity):
            return False
        return self.activity_id == o.activity_id and self.start_time == o.start_time and self.end_time == o.end_time \
            and self.description == o.description and self.attendees == o.attendees and self.status == o.status
