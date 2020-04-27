from __future__ import absolute_import, annotations

from typing import Optional, List

from wenet.service_api.task import TaskAttribute


class TaskTransaction:

    def __init__(self, task_id: str, type_id: str, attributes: Optional[List[TaskAttribute]]):
        self.task_id = task_id
        self.type_id = type_id
        self.attributes = attributes

        if not isinstance(task_id, str):
            raise TypeError("Task id should be a string")
        if not isinstance(type_id, str):
            raise TypeError("Type id should be a string")

        if self.attributes:
            if not isinstance(self.attributes, list):
                raise TypeError("Attributes should be a list of TaskAttribute")
            else:
                for attribute in attributes:
                    if not isinstance(attribute, TaskAttribute):
                        raise TypeError("Attributes should be a list of TaskAttribute")
        else:
            self.attributes: List[TaskAttribute] = []

    def to_repr(self) -> dict:
        return {
            "taskId": self.task_id,
            "typeId": self.type_id,
            "attributes": list(x.to_repr() for x in self.attributes)
        }

    @staticmethod
    def from_repr(raw_data: dict) -> TaskTransaction:
        return TaskTransaction(
            task_id=raw_data["taskId"],
            type_id=raw_data["typeId"],
            attributes=list(TaskAttribute.from_repr(x) for x in raw_data["attributes"]) if raw_data.get("attributes", None) else None
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, TaskTransaction):
            return False
        return self.task_id == o.task_id and self.type_id == o.type_id and self.attributes == o.attributes

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()
