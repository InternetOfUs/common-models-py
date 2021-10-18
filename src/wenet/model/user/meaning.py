from __future__ import absolute_import, annotations

from typing import Optional

from wenet.model.extended_property import ExtendedProperty


class Meaning(ExtendedProperty):

    def __init__(self, name: Optional[str], category: Optional[str], level: Optional[float]) -> None:
        """
        For defining more general purpose concepts

        Args:
            name: The name of the concept represented by the meaning
            category: The category associated to the meaning
            level: The level associated to the concept
        """
        self.name = name
        self.category = category
        self.level = level

    def to_repr(self) -> dict:
        return {
            "name": self.name,
            "category": self.category,
            "level": self.level
        }

    @staticmethod
    def from_repr(raw_data: dict) -> Meaning:
        return Meaning(
            name=raw_data.get("name", None),
            category=raw_data.get("category", None),
            level=raw_data.get("level", None)
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, Meaning):
            return False
        return self.name == o.name and self.category == o.category and self.level == o.level
