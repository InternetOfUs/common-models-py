from __future__ import absolute_import, annotations

from enum import Enum
from numbers import Number
from typing import Optional, List, Union

from wenet.model.protocol_norm import ProtocolNorm
from wenet.model.task.transaction import TaskTransaction


class TaskState(Enum):

    OPEN = "Open"
    PENDING_ASSIGNMENT = "PendingAssignment"
    ASSIGNED = "Assigned"
    COMPLETED = "Completed"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"


class TaskGoal:

    def __init__(self, name: str, description: str, keywords: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.keywords = keywords if keywords else []

    def to_repr(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "keywords": self.keywords,
        }

    @staticmethod
    def from_repr(raw_data: dict) -> TaskGoal:
        return TaskGoal(
            name=raw_data["name"],
            description=raw_data.get("description", ""),
            keywords=raw_data.get("keywords", None)
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TaskGoal):
            return False

        return self.name == o.name and self.description == o.description and self.keywords == o.keywords

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self):
        return self.to_repr()


class Task:

    def __init__(self,
                 task_id: Optional[str],
                 creation_ts: Optional[Number],
                 last_update_ts: Optional[Number],
                 task_type_id: str,
                 requester_id: str,
                 app_id: str,
                 community_id: Optional[str],
                 goal: TaskGoal,
                 norms: Optional[Union[List[dict], List[ProtocolNorm]]] = None,
                 attributes: Optional[dict] = None,
                 close_ts: Optional[Number] = None,
                 transactions: Optional[List[TaskTransaction]] = None
                 ):

        self.task_id = task_id
        self.creation_ts = creation_ts

        self.last_update_ts = last_update_ts
        self.task_type_id = task_type_id
        self.requester_id = requester_id
        self.app_id = app_id
        self.goal = goal
        self.community_id = community_id

        self.norms = norms
        self.attributes = attributes
        self.close_ts = close_ts
        self.transactions = transactions

        if task_id is not None:
            if not isinstance(task_id, str):
                raise TypeError("TaskId should be a string")

        if creation_ts is not None:
            if not isinstance(creation_ts, Number):
                raise TypeError("CreationTs should be a string")

        if last_update_ts is not None:
            if not isinstance(last_update_ts, Number):
                raise TypeError("LastUpdateTs should be a number")

        if not isinstance(task_type_id, str):
            raise TypeError("TaskType Id should be a string")

        if not isinstance(requester_id, str):
            raise TypeError("RequesterId Id should be a string")

        if not isinstance(app_id, str):
            raise TypeError("AppId should be a string")

        if not isinstance(goal, TaskGoal):
            raise TypeError("Goal should be an instance of TaskGoal")

        if norms:
            if not isinstance(norms, list):
                raise ValueError("Norms should be a list of Norm")
        else:
            self.norms = []

        if self.attributes:
            if not isinstance(self.attributes, dict):
                raise TypeError("Attributes should be a list of attributes")
        else:
            self.attributes = {}

        if self.close_ts is not None:
            if not isinstance(self.close_ts, Number):
                raise TypeError("CloseTS should be an integer")

        if not self.transactions:
            self.transactions = []

    def to_repr(self) -> dict:
        raw_norms = [norm.to_repr() if isinstance(norm, ProtocolNorm) else norm for norm in self.norms]
        return {
            "id": self.task_id,
            "_creationTs": self.creation_ts,
            "_lastUpdateTs": self.last_update_ts,
            "taskTypeId": self.task_type_id,
            "requesterId": self.requester_id,
            "appId": self.app_id,
            "goal": self.goal.to_repr(),
            "norms": raw_norms,
            "attributes": self.attributes,
            "closeTs": self.close_ts,
            "communityId": self.community_id,
            "transactions": [t.to_repr() for t in self.transactions],
        }

    @staticmethod
    def from_repr(raw_data: dict, task_id: Optional[str] = None) -> Task:

        if task_id is None:
            task_id = raw_data.get("id", None)

        return Task(
            task_id,
            raw_data.get("_creationTs", None),
            raw_data.get("_lastUpdateTs", None),
            raw_data["taskTypeId"],
            raw_data["requesterId"],
            raw_data["appId"],
            raw_data.get("communityId", None),
            TaskGoal.from_repr(raw_data["goal"]),
            raw_data["norms"] if raw_data.get("norms", None) else None,
            raw_data.get("attributes", None),
            raw_data.get("closeTs", None),
            [TaskTransaction.from_repr(t) for t in raw_data.get("transactions", None)] if raw_data.get("transactions", None) else None
        )

    @property
    def norms_as_objects(self) -> Optional[List[ProtocolNorm]]:
        """
        Returns the norms attribute as a list of ProtocolNorm objects
        """
        return [ProtocolNorm.from_repr(norm) if isinstance(norm, dict) else norm for norm in self.norms] if self.norms is not None else None

    def prepare_task(self) -> dict:
        task_repr = self.to_repr()
        task_repr.pop("_creationTs", None)
        task_repr.pop("_lastUpdateTs", None)
        return task_repr

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

    def __eq__(self, o):
        if not isinstance(o, Task):
            return False
        return self.task_id == o.task_id and self.creation_ts == o.creation_ts and \
            self.last_update_ts == o.last_update_ts and self.task_type_id == o.task_type_id and \
            self.requester_id == o.requester_id and self.app_id == o.app_id and self.goal == o.goal and \
            self.norms == o.norms and self.attributes == o.attributes and self.close_ts == o.close_ts and \
            self.community_id == o.community_id and self.transactions == o.transactions


class TaskPage:

    def __init__(self, offset: int, total: int, tasks: Optional[List[Task]]):
        """
        Contains a set of tasks, used for the pagination in task list requests
        @param offset:
        @param total:
        @param tasks:
        """
        self.offset = offset
        self.total = total
        self.tasks = tasks

        if not isinstance(self.offset, int):
            raise TypeError("Offset should be an integer")
        if not isinstance(self.total, int):
            raise TypeError("Total should be an integer")
        if self.tasks:
            if isinstance(self.tasks, list):
                for task in self.tasks:
                    if not isinstance(task, Task):
                        raise TypeError("Tasks should be a list of Tasks")
            else:
                raise TypeError("Tasks should be a list of Task")
        else:
            self.tasks = []

    def to_repr(self) -> dict:
        return {
            "offset": self.offset,
            "total": self.total,
            "tasks": list(x.to_repr() for x in self.tasks)
        }

    @staticmethod
    def from_repr(raw_data: dict) -> TaskPage:
        tasks = raw_data.get("tasks")
        if tasks:
            tasks = list(Task.from_repr(x) for x in tasks)
        return TaskPage(
            offset=raw_data["offset"],
            total=raw_data["total"],
            tasks=tasks
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, TaskPage):
            return False
        return self.offset == o.offset and self.total == o.total and self.tasks == o.tasks

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()
