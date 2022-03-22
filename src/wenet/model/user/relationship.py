from __future__ import absolute_import, annotations

from enum import Enum
from typing import Optional, List

from wenet.model.extended_property import ExtendedProperty


class RelationType(Enum):

    FRIEND = "friend"
    COLLEAGUE = "colleague"
    FOLLOWER = "follower"
    FAMILY = "family"
    ACQUAINTANCE = "acquaintance"


class Relationship(ExtendedProperty):

    def __init__(self,
                 app_id: Optional[str],
                 source_id: Optional[str],
                 target_id: Optional[str],
                 relation_type: Optional[RelationType],
                 weight: Optional[float]
                 ) -> None:
        """
        A relationship between wenet users

        Args:
            app_id: The identifier of the application where the relation happens
            target_id: The identifier of the wenet user the relationship is related to
            relation_type: The relationship type
            weight: A number from 0 to 1 that indicates the strength of the relation. 0 indicates a deleted/non-exisiting relation
        """
        self.app_id = app_id
        self.source_id = source_id
        self.target_id = target_id
        self.relation_type = relation_type
        self.weight = weight

        if self.weight is not None and not (0 <= self.weight <= 1):
            raise ValueError("weight value is not between 0 and 1")

    def to_repr(self) -> dict:
        return {
            "appId": self.app_id,
            "sourceId": self.source_id,
            "targetId": self.target_id,
            "type": self.relation_type.value,
            "weight": self.weight
        }

    @staticmethod
    def from_repr(raw_data: dict) -> Relationship:
        return Relationship(
            app_id=raw_data.get("appId", None),
            source_id=raw_data.get("sourceId", None),
            target_id=raw_data.get("targetId", None),
            relation_type=RelationType(raw_data["type"]) if raw_data.get("type", None) is not None else None,
            weight=raw_data.get("weight", None)
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, Relationship):
            return False
        return self.app_id == o.app_id and self.source_id == o.source_id and self.target_id == o.target_id and self.relation_type == o.relation_type and self.weight == o.weight


class RelationshipPage:

    def __init__(self, offset: int, total: int, relationships: List[Relationship]):
        self.offset = offset
        self.total = total
        self.relationships = relationships

    def to_repr(self) -> dict:
        return {
            "offset": self.offset,
            "total": self.total,
            "relationships": [x.to_repr() for x in self.relationships]
        }

    @staticmethod
    def from_repr(raw_data: dict) -> RelationshipPage:
        return RelationshipPage(
            offset=raw_data["offset"],
            total=raw_data["total"],
            relationships=[Relationship.from_repr(x) for x in raw_data["relationships"]] if raw_data.get("relationships") else []
        )

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

    def __eq__(self, o) -> bool:
        if not isinstance(o, RelationshipPage):
            return False

        return self.offset == o.offset and self.total == o.total and self.relationships == o.relationships
