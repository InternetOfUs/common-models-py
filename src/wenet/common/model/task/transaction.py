from __future__ import absolute_import, annotations

from typing import Optional, List

from wenet.common.model.task.task import TaskAttribute


class TaskTransaction:
    LABEL_VOLUNTEER_FOR_TASK = 'volunteerForTask'
    LABEL_REFUSE_TASK = 'refuseTask'
    LABEL_ACCEPT_VOLUNTEER = 'acceptVolunteer'
    LABEL_REFUSE_VOLUNTEER = 'refuseVolunteer'
    LABEL_TASK_COMPLETED = 'taskCompleted'

    def __init__(self, task_id: str, label: str, attributes: Optional[List[TaskAttribute]]):
        self.task_id = task_id
        self.label = label
        self.attributes = attributes

        if not isinstance(task_id, str):
            raise TypeError("Task id should be a string")
        if not isinstance(label, str):
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

        allowed_task_labels = [TaskTransaction.LABEL_ACCEPT_VOLUNTEER, TaskTransaction.LABEL_REFUSE_TASK,
                               TaskTransaction.LABEL_TASK_COMPLETED, TaskTransaction.LABEL_REFUSE_VOLUNTEER,
                               TaskTransaction.LABEL_VOLUNTEER_FOR_TASK]
        if self.label not in allowed_task_labels:
            raise ValueError(f"Label {label} not valid, it must be one of {allowed_task_labels}")

    def to_repr(self) -> dict:
        return {
            "taskId": self.task_id,
            "label": self.label,
            "attributes": {x.name: x.value for x in self.attributes}
        }

    @staticmethod
    def from_repr(raw_data: dict) -> TaskTransaction:
        return TaskTransaction(
            task_id=raw_data["taskId"],
            label=raw_data["label"],
            attributes=[TaskAttribute(x, raw_data["attributes"][x]) for x in raw_data["attributes"]]
            if raw_data.get("attributes", None) else None
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, TaskTransaction):
            return False
        return self.task_id == o.task_id and self.label == o.label and self.attributes == o.attributes

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()

    def with_attribute(self, attribute: TaskAttribute) -> TaskTransaction:
        self.attributes.append(attribute)
        return self
