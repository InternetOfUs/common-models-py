from __future__ import absolute_import, annotations

from typing import Optional

from wenet.model.extended_property import ExtendedProperty


class Competence(ExtendedProperty):

    def __init__(self, name: Optional[str], ontology: Optional[str], level: Optional[float]) -> None:
        """
        It describe a competence of a user

        Args:
            name: The name of the competence
            ontology: The identifier of the competence
            level: The identifier of the competence (value in between 0 and 1, both included)
        """
        self.name = name
        self.ontology = ontology
        self.level = level

        if self.level is not None and not (0 <= self.level <= 1):
            raise ValueError("level value is not between 0 and 1")

    def to_repr(self) -> dict:
        return {
            "name": self.name,
            "ontology": self.ontology,
            "level": self.level
        }

    @staticmethod
    def from_repr(raw_data: dict) -> Competence:
        return Competence(
            name=raw_data.get("name", None),
            ontology=raw_data.get("ontology", None),
            level=raw_data.get("level", None)
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, Competence):
            return False
        return self.name == o.name and self.ontology == o.ontology and self.level == o.level
