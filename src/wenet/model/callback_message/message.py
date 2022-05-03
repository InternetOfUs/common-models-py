from __future__ import absolute_import, annotations

from typing import Optional


class Message:
    """
    Base message from WeNet to the user.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - receiver_id: The Wenet user ID of the recipient of the message
        - label: The type of the message
        - attributes: dictionary with additional attributes of the message. It may contain
            - community_id: ID of the community related to the message
            - task_id: The identifier of the target task
    """

    def __init__(self, app_id: str, receiver_id: str, label: str, attributes: dict) -> None:
        self.app_id = app_id
        self.receiver_id = receiver_id
        self.label = label
        self.attributes = attributes

    def to_repr(self) -> dict:
        return {
            "appId": self.app_id,
            "receiverId": self.receiver_id,
            "label": self.label,
            "attributes": self.attributes
        }

    @staticmethod
    def from_repr(raw: dict) -> Message:
        return Message(
            app_id=raw["appId"],
            receiver_id=raw["receiverId"],
            label=raw["label"],
            attributes=raw["attributes"]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Message):
            return False
        return self.app_id == o.app_id and self.receiver_id == o.receiver_id and self.label == o.label and \
            self.attributes == o.attributes

    @property
    def community_id(self) -> Optional[str]:
        return self.attributes["communityId"] if "communityId" in self.attributes else None

    @property
    def task_id(self) -> Optional[str]:
        return self.attributes["taskId"] if "taskId" in self.attributes else None
