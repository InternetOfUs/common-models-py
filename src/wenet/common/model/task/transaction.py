from __future__ import absolute_import, annotations

from typing import Optional, List

from wenet.common.model.message.message import Message


class TaskTransaction:

    def __init__(self, id: str, task_id: str, label: str, creation_ts: int, last_update_ts: int, actioneer_id: str,
                 attributes: Optional[dict], messages: Optional[List[Message]] = None):
        self.task_id = task_id
        self.label = label
        self.attributes = attributes
        self.id = id
        self.creation_ts = creation_ts
        self.last_update_ts = last_update_ts
        self.actioneer_id = actioneer_id
        self.messages = messages

        if not isinstance(task_id, str):
            raise TypeError("Task id should be a string")
        if not isinstance(label, str):
            raise TypeError("Type id should be a string")

        if self.attributes:
            if not isinstance(self.attributes, dict):
                raise TypeError("Attributes should be a list of TaskAttribute")
        else:
            self.attributes = {}

        if not self.messages:
            self.messages = []

    def to_repr(self) -> dict:
        return {
            "id": self.id,
            "taskId": self.task_id,
            "label": self.label,
            "attributes": self.attributes,
            "_creationTs": self.creation_ts,
            "_lastUpdateTs": self.last_update_ts,
            "actioneerId": self.actioneer_id,
            "messages": self.messages,
        }

    @staticmethod
    def from_repr(raw_data: dict) -> TaskTransaction:
        return TaskTransaction(
            raw_data["id"],
            raw_data["taskId"],
            raw_data["label"],
            raw_data["_creationTs"],
            raw_data["_lastUpdateTs"],
            raw_data["actioneerId"],
            raw_data.get("attributes", None) if raw_data.get("attributes", None) else None,
            raw_data.get("messages", None) if raw_data.get("messages", None) else None
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, TaskTransaction):
            return False
        return self.task_id == o.task_id and self.label == o.label and self.attributes == o.attributes and \
            self.id == o.id and self.actioneer_id == o.actioneer_id

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()
