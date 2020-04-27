from __future__ import absolute_import, annotations

from enum import Enum


class NormOperator(Enum):

    EQUALS = "EQUALS"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_EQ_THAN = "LESS_EQ_THAN"
    GREATER_EQ_THAN = "GREATER_EQ_THAN"


class Norm:

    def __init__(self, norm_id: str, attribute: str, operator: NormOperator, comparison: bool, negation: bool):
        self.norm_id = norm_id
        self.attribute = attribute
        self.operator = operator
        self.comparison = comparison
        self.negation = negation

    def to_repr(self) -> dict:
        return {
            "id": self.norm_id,
            "attribute": self.attribute,
            "operator": self.operator.value,
            "comparison": self.comparison,
            "negation": self.negation
        }

    @staticmethod
    def from_repr(raw_data: dict) -> Norm:
        return Norm(
            norm_id=raw_data["id"],
            attribute=raw_data["attribute"],
            operator=NormOperator(raw_data["operator"]),
            comparison=raw_data["comparison"],
            negation=raw_data["negation"]
        )

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

    def __eq__(self, o):
        if not isinstance(o, Norm):
            return False
        return self.norm_id == o.norm_id and self.attribute == o.attribute and self.operator == o.operator and self.comparison == o.comparison and self.negation == o.negation
