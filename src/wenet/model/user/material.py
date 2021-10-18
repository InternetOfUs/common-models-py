from __future__ import absolute_import, annotations

from typing import Optional

from wenet.model.extended_property import ExtendedProperty


class Material(ExtendedProperty):

    def __init__(self, name: Optional[str], description: Optional[str], quantity: Optional[int], classification: Optional[str]) -> None:
        """
        It describes an object that is available to a user

        Args:
            name: The name of the object
            description: A description of the object
            quantity: The amount of units available, minimum: 1
            classification: The classification used for representing the object
        """
        self.name = name
        self.description = description
        self.quantity = quantity
        self.classification = classification

        if self.quantity is not None and not (1 <= self.quantity):
            raise ValueError("quantity value is under the minimum value of 1")

    def to_repr(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "quantity": self.quantity,
            "classification": self.classification
        }

    @staticmethod
    def from_repr(raw_data: dict) -> Material:
        return Material(
            name=raw_data.get("name", None),
            description=raw_data.get("description", None),
            quantity=raw_data.get("quantity", None),
            classification=raw_data.get("classification", None)
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, Material):
            return False
        return self.name == o.name and self.description == o.description and self.quantity == o.quantity and self.classification == o.classification
