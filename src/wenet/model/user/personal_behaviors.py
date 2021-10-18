from __future__ import absolute_import, annotations

from typing import Optional, Dict, List

from wenet.model.extended_property import ExtendedProperty


class Label:

    def __init__(self, name: Optional[str], semantic_class: Optional[float], latitude: Optional[float], longitude: Optional[float]) -> None:
        """
        A label

        Args:
            name: name of the label
            semantic_class: number that represent the category of the label
            latitude: latitude of the label for the user (minimum: -90, maximum: 90)
            longitude: longitude of the label for the user (minimum: -180, maximum: 180)
        """
        self.name = name
        self.semantic_class = semantic_class
        self.latitude = latitude
        self.longitude = longitude

        if self.latitude is not None and not (-90 <= self.latitude <= 90):
            raise ValueError("latitude value is not between -90 and 90")

        if self.longitude is not None and not (-180 <= self.longitude <= 180):
            raise ValueError("longitude value is not between -180 and 180")

    def to_repr(self) -> dict:
        return {
            "name": self.name,
            "semantic_class": self.semantic_class,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    @staticmethod
    def from_repr(raw_data: dict) -> Label:
        return Label(
            name=raw_data.get("name", None),
            semantic_class=raw_data.get("semantic_class", None),
            latitude=raw_data.get("latitude", None),
            longitude=raw_data.get("longitude", None)
        )

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, o) -> bool:
        if not isinstance(o, Label):
            return False
        return self.name == o.name and self.semantic_class == o.semantic_class and self.latitude == o.latitude and self.longitude == o.longitude


class ScoredLabel:

    def __init__(self, label: Optional[Label], score: Optional[float]) -> None:
        """
        Label with score

        Args:
            label: the label
            score: score of the label
        """
        self.label = label
        self.score = score

    def to_repr(self) -> dict:
        return {
            "label": self.label.to_repr(),
            "score": self.score
        }

    @staticmethod
    def from_repr(raw_data: dict) -> ScoredLabel:
        return ScoredLabel(
            label=Label.from_repr(raw_data["label"]) if raw_data.get("label", None) is not None else None,
            score=raw_data.get("score", None)
        )

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, o) -> bool:
        if not isinstance(o, ScoredLabel):
            return False
        return self.label == o.label and self.score == o.score


class PersonalBehavior(ExtendedProperty):

    def __init__(self, user_id: Optional[str], weekday: Optional[str], label_distribution: Optional[Dict[str, Optional[List[ScoredLabel]]]],
                 confidence: Optional[float]) -> None:
        """
        Labels distribution for a given user, time and weekday

        Args:
            user_id: id of the user
            weekday: day of the week
            label_distribution: time slots with distribution of the labels
            confidence: confidence of the result
        """
        self.user_id = user_id
        self.weekday = weekday
        self.label_distribution = label_distribution
        self.confidence = confidence

    def to_repr(self) -> dict:
        if self.label_distribution is not None:
            label_distribution = {}
            for key in self.label_distribution:
                if self.label_distribution[key] is not None:
                    label_distribution[key] = [item.to_repr() for item in self.label_distribution[key]]
                else:
                    label_distribution[key] = None
        else:
            label_distribution = None

        return {
            "user_id": self.user_id,
            "weekday": self.weekday,
            "label_distribution": label_distribution,
            "confidence": self.confidence
        }

    @staticmethod
    def from_repr(raw_data: dict) -> PersonalBehavior:
        if raw_data.get("label_distribution", None) is not None:
            label_distribution = {}
            for key in raw_data["label_distribution"]:
                if raw_data["label_distribution"][key] is not None:
                    label_distribution[key] = [ScoredLabel.from_repr(item) for item in raw_data["label_distribution"][key]]
                else:
                    label_distribution[key] = None
        else:
            label_distribution = None

        return PersonalBehavior(
            user_id=raw_data.get("user_id", None),
            weekday=raw_data.get("weekday", None),
            label_distribution=label_distribution,
            confidence=raw_data.get("confidence", None)
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, PersonalBehavior):
            return False
        return self.user_id == o.user_id and self.weekday == o.weekday and self.label_distribution == o.label_distribution and self.confidence == o.confidence
