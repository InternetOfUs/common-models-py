from __future__ import absolute_import, annotations

from typing import Optional

from wenet.model.extended_property import ExtendedProperty


class ProtocolNorm(ExtendedProperty):

    def __init__(self, description: Optional[str], whenever: Optional[str], thenceforth: Optional[str], ontology: Optional[str]) -> None:
        """
        The description of a rule that has to follow by the wenet users

        Args:
            description: A human readable description of the norm
            whenever: The conditions that fires this norm
            thenceforth: The action to do if the conditions are satisfied
            ontology: The ontology used on the norms
        """
        self.description = description
        self.whenever = whenever
        self.thenceforth = thenceforth
        self.ontology = ontology

    def to_repr(self) -> dict:
        return {
            "description": self.description,
            "whenever": self.whenever,
            "thenceforth": self.thenceforth,
            "ontology": self.ontology
        }

    @staticmethod
    def from_repr(raw_data: dict) -> ProtocolNorm:
        return ProtocolNorm(
            description=raw_data.get("description", None),
            whenever=raw_data.get("whenever", None),
            thenceforth=raw_data.get("thenceforth", None),
            ontology=raw_data.get("ontology", None)
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, ProtocolNorm):
            return False
        return self.description == o.description and self.whenever == o.whenever and self.thenceforth == o.thenceforth and self.ontology == o.ontology
