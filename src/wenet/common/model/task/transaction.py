from __future__ import absolute_import, annotations

from typing import Optional


class TaskTransaction:
    LABEL_VOLUNTEER_FOR_TASK = 'volunteerForTask'
    LABEL_REFUSE_TASK = 'refuseTask'
    LABEL_ACCEPT_VOLUNTEER = 'acceptVolunteer'
    LABEL_REFUSE_VOLUNTEER = 'refuseVolunteer'
    LABEL_TASK_COMPLETED = 'taskCompleted'

    def __init__(self, task_id: str, label: str, attributes: Optional[dict]):
        self.task_id = task_id
        self.label = label
        self.attributes = attributes

        if not isinstance(task_id, str):
            raise TypeError("Task id should be a string")
        if not isinstance(label, str):
            raise TypeError("Type id should be a string")

        if self.attributes:
            if not isinstance(self.attributes, dict):
                raise TypeError("Attributes should be a list of TaskAttribute")
        else:
            self.attributes = {}

        allowed_task_labels = [TaskTransaction.LABEL_ACCEPT_VOLUNTEER, TaskTransaction.LABEL_REFUSE_TASK,
                               TaskTransaction.LABEL_TASK_COMPLETED, TaskTransaction.LABEL_REFUSE_VOLUNTEER,
                               TaskTransaction.LABEL_VOLUNTEER_FOR_TASK]
        if self.label not in allowed_task_labels:
            raise ValueError(f"Label {label} not valid, it must be one of {allowed_task_labels}")

    def to_repr(self) -> dict:
        return {
            "taskId": self.task_id,
            "label": self.label,
            "attributes": self.attributes
        }

    @staticmethod
    def from_repr(raw_data: dict) -> TaskTransaction:
        return TaskTransaction(
            task_id=raw_data["taskId"],
            label=raw_data["label"],
            attributes=raw_data.get("attributes", None)
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
