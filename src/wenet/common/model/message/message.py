from __future__ import absolute_import
from __future__ import annotations


class Message:
    """
    Base message from WeNet to the user.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - community_id: ID of the community related to the message
        - task_id: The identifier of the target task
        - receiver_id: The Wenet user ID of the recipient of the message
        - label: The type of the message
        - attributes: dictionary with additional attributes of the message
    """

    def __init__(self, app_id: str, community_id: str, task_id: str, receiver_id: str, label: str,
                 attributes: dict) -> None:
        self.app_id = app_id
        self.community_id = community_id
        self.task_id = task_id
        self.receiver_id = receiver_id
        self.label = label
        self.attributes = attributes

    def to_repr(self) -> dict:
        return {
            "appId": self.app_id,
            "communityId": self.community_id,
            "taskId": self.task_id,
            "receiverId": self.receiver_id,
            "label": self.label,
            "attributes": self.attributes
        }

    @staticmethod
    def from_repr(raw: dict) -> Message:
        return Message(
            raw["appId"],
            raw["communityId"],
            raw["taskId"],
            raw["receiverId"],
            raw["label"],
            raw["attributes"]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Message):
            return False
        return self.app_id == o.app_id and self.community_id == o.community_id and self.task_id == o.task_id and \
            self.receiver_id == o.receiver_id and self.label == o.label and self.attributes == o.attributes


class TextualMessage(Message):
    """
    A simple textual message from WeNet to the user.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - community_id: ID of the community related to the message
        - task_id: The identifier of the target task
        - receiver_id: The Wenet user ID of the recipient of the message
        - title: The title of the message
        - text: the content of the message
    """
    LABEL = "TextualMessage"

    def __init__(self, app_id: str, community_id: str, task_id: str, receiver_id: str, title: str, text: str) -> None:
        attributes = {
            "title": title,
            "text": text,
        }
        super().__init__(app_id, community_id, task_id, receiver_id, self.LABEL, attributes)

    @property
    def text(self) -> str:
        return self.attributes["text"]

    @property
    def title(self) -> str:
        return self.attributes["title"]

    @staticmethod
    def from_repr(raw: dict) -> TextualMessage:
        return TextualMessage(
            raw["appId"],
            raw["communityId"],
            raw["taskId"],
            raw["receiverId"],
            raw["attributes"]["title"],
            raw["attributes"]["text"]
        )


class TaskProposalNotification(Message):
    """
    This notification is used in order to propose a user to volunteer to a newly created task

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - community_id: ID of the community related to the message
        - task_id: The identifier of the target task
        - receiver_id: The Wenet user ID of the recipient of the message
    """
    LABEL = "TaskProposalNotification"

    def __init__(self, app_id: str, community_id: str, task_id: str, receiver_id: str) -> None:
        super().__init__(app_id, community_id, task_id, receiver_id, self.LABEL, {})

    @staticmethod
    def from_repr(raw: dict) -> TaskProposalNotification:
        return TaskProposalNotification(
            raw["appId"],
            raw["communityId"],
            raw["taskId"],
            raw["receiverId"]
        )


class TaskVolunteerNotification(Message):
    """
    This notification is used in order to notify the task creator that a new volunteer is proposing to participate
    to the task.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - community_id: ID of the community related to the message
        - task_id: The identifier of the target task
        - receiver_id: The Wenet user ID of the recipient of the message
        - volunteer_id: The Wenet user ID of the volunteer
    """
    LABEL = "TaskVolunteerNotification"

    def __init__(self, app_id: str, community_id: str, task_id: str, receiver_id: str, volunteer_id: str) -> None:
        attributes = {"volunteerId": volunteer_id}
        super().__init__(app_id, community_id, task_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> TaskVolunteerNotification:
        return TaskVolunteerNotification(
            raw["appId"],
            raw["communityId"],
            raw["taskId"],
            raw["receiverId"],
            raw["attributes"]["volunteerId"]
        )

    @property
    def volunteer_id(self) -> str:
        return self.attributes["volunteerId"]


class TaskSelectionNotification(Message):
    """
    This notification is used in order to notify the user who volunteered about the decision of the task creator.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - community_id: ID of the community related to the message
        - task_id: The identifier of the target task
        - receiver_id: The Wenet user ID of the recipient of the message
        - outcome: The outcome of the selection, either 'accepted' or 'refused'
    """
    LABEL = "TaskSelectionNotification"
    OUTCOME_ACCEPTED = 'accepted'
    OUTCOME_REFUSED = 'refused'

    def __init__(self, app_id: str, community_id: str, task_id: str, receiver_id: str, outcome: str) -> None:
        accepted_outcomes = [self.OUTCOME_ACCEPTED, self.OUTCOME_REFUSED]
        if outcome not in accepted_outcomes:
            raise ValueError(f"Outcome must be one of {accepted_outcomes}, got [{outcome}]")
        attributes = {"outcome": outcome}
        super().__init__(app_id, community_id, task_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> TaskSelectionNotification:
        return TaskSelectionNotification(
            raw["appId"],
            raw["communityId"],
            raw["taskId"],
            raw["receiverId"],
            raw["attributes"]["outcome"]
        )

    @property
    def outcome(self) -> str:
        return self.attributes["outcome"]


class TaskConcludedNotification(Message):
    """
    This notification is used in order to notify task participants that a task has been completed, the outcome could be:
        - completed (if completed correctly)
        - failed (if something went wrong)
        - cancelled (the creator cancelled the task)

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - community_id: ID of the community related to the message
        - task_id: The identifier of the target task
        - receiver_id: The Wenet user ID of the recipient of the message
        - outcome: The outcome of the task
    """
    LABEL = "TaskConcludedNotification"
    OUTCOME_COMPLETED = "completed"
    OUTCOME_CANCELLED = "cancelled"
    OUTCOME_FAILED = "failed"

    def __init__(self, app_id: str, community_id: str, task_id: str, receiver_id: str, outcome: str) -> None:
        accepted_outcomes = [self.OUTCOME_COMPLETED, self.OUTCOME_CANCELLED, self.OUTCOME_FAILED]
        if outcome not in accepted_outcomes:
            raise ValueError(f"Outcome must be one of {accepted_outcomes}, got [{outcome}]")
        attributes = {"outcome": outcome}
        super().__init__(app_id, community_id, task_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> TaskConcludedNotification:
        return TaskConcludedNotification(
            raw["appId"],
            raw["communityId"],
            raw["taskId"],
            raw["receiverId"],
            raw["attributes"]["outcome"]
        )

    @property
    def outcome(self) -> str:
        return self.attributes["outcome"]
