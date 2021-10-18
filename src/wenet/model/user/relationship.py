from __future__ import absolute_import, annotations

from enum import Enum
from typing import Optional

from wenet.model.extended_property import ExtendedProperty


class RelationType(Enum):

    FRIEND = "friend"
    COLLEAGUE = "colleague"
    FOLLOWER = "follower"
    FAMILY = "family"
    ACQUAINTANCE = "acquaintance"


class Relationship(ExtendedProperty):

    def __init__(self, app_id: Optional[str], user_id: Optional[str], relation_type: Optional[RelationType], weight: Optional[float]) -> None:
        """
        A relationship between wenet users

        Args:
            app_id: The identifier of the application where the relation happens
            user_id: The identifier of the wenet user the relationship is related to
            relation_type: The relationship type
            weight: A number from 0 to 1 that indicates the strength of the relation. 0 indicates a deleted/non-exisiting relation
        """
        self.app_id = app_id
        self.user_id = user_id
        self.relation_type = relation_type
        self.weight = weight

        if self.weight is not None and not (0 <= self.weight <= 1):
            raise ValueError("weight value is not between 0 and 1")

    def to_repr(self) -> dict:
        return {
            "appId": self.app_id,
            "userId": self.user_id,
            "type": self.relation_type.value,
            "weight": self.weight
        }

    @staticmethod
    def from_repr(raw_data: dict) -> Relationship:
        return Relationship(
            app_id=raw_data.get("appId", None),
            user_id=raw_data.get("userId", None),
            relation_type=RelationType(raw_data["type"]) if raw_data.get("type", None) is not None else None,
            weight=raw_data.get("weight", None)
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, Relationship):
            return False
        return self.app_id == o.app_id and self.user_id == o.user_id and self.relation_type == o.relation_type and self.weight == o.weight
