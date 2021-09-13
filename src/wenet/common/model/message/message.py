from __future__ import absolute_import
from __future__ import annotations

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
        message_type = raw["label"]
        if message_type == TextualMessage.LABEL:
            return TextualMessage.from_repr(raw)
        elif message_type == TaskProposalNotification.LABEL:
            return TaskProposalNotification.from_repr(raw)
        elif message_type == TaskConcludedNotification.LABEL:
            return TaskConcludedNotification.from_repr(raw)
        elif message_type == TaskSelectionNotification.LABEL:
            return TaskSelectionNotification.from_repr(raw)
        elif message_type == TaskVolunteerNotification.LABEL:
            return TaskVolunteerNotification.from_repr(raw)
        elif message_type == IncentiveMessage.LABEL:
            return IncentiveMessage.from_repr(raw)
        elif message_type == IncentiveBadge.LABEL:
            return IncentiveBadge.from_repr(raw)
        elif message_type == QuestionToAnswerMessage.LABEL:
            return QuestionToAnswerMessage.from_repr(raw)
        elif message_type == AnsweredQuestionMessage.LABEL:
            return AnsweredQuestionMessage.from_repr(raw)
        elif message_type == AnsweredPickedMessage.LABEL:
            return AnsweredPickedMessage.from_repr(raw)
        else:
            return Message(
                raw["appId"],
                raw["receiverId"],
                raw["label"],
                raw["attributes"]
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


class TextualMessage(Message):
    """
    A simple textual message from WeNet to the user.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - receiver_id: The Wenet user ID of the recipient of the message
        - title: The title of the message
        - text: the content of the message
        - attributes: dictionary with additional attributes of the message. It may contain
            - community_id: ID of the community related to the message
            - task_id: The identifier of the target task
    """
    LABEL = "TextualMessage"

    def __init__(self, app_id: str, receiver_id: str, title: str, text: str, attributes: dict) -> None:
        attributes.update({
            "title": title,
            "text": text,
        })
        super().__init__(app_id, receiver_id, self.LABEL, attributes)

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
            raw["receiverId"],
            raw["attributes"]["title"],
            raw["attributes"]["text"],
            raw["attributes"]
        )


class TaskProposalNotification(Message):
    """
    This notification is used in order to propose a user to volunteer to a newly created task

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - receiver_id: The Wenet user ID of the recipient of the message
        - attributes: dictionary with additional attributes of the message. It may contain
            - community_id: ID of the community related to the message
            - task_id: The identifier of the target task
    """
    LABEL = "TaskProposalNotification"

    def __init__(self, app_id: str, receiver_id: str, attributes: dict) -> None:
        super().__init__(app_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> TaskProposalNotification:
        return TaskProposalNotification(
            raw["appId"],
            raw["receiverId"],
            raw["attributes"]
        )


class TaskVolunteerNotification(Message):
    """
    This notification is used in order to notify the task creator that a new volunteer is proposing to participate
    to the task.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - receiver_id: The Wenet user ID of the recipient of the message
        - volunteer_id: The Wenet user ID of the volunteer
        - attributes: dictionary with additional attributes of the message. It may contain
            - community_id: ID of the community related to the message
            - task_id: The identifier of the target task
    """
    LABEL = "TaskVolunteerNotification"

    def __init__(self, app_id: str, receiver_id: str, volunteer_id: str, attributes: dict) -> None:
        attributes.update({"volunteerId": volunteer_id})
        super().__init__(app_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> TaskVolunteerNotification:
        return TaskVolunteerNotification(
            raw["appId"],
            raw["receiverId"],
            raw["attributes"]["volunteerId"],
            raw["attributes"]
        )

    @property
    def volunteer_id(self) -> str:
        return self.attributes["volunteerId"]


class TaskSelectionNotification(Message):
    """
    This notification is used in order to notify the user who volunteered about the decision of the task creator.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - receiver_id: The Wenet user ID of the recipient of the message
        - outcome: The outcome of the selection, either 'accepted' or 'refused'
        - attributes: dictionary with additional attributes of the message. It may contain
            - community_id: ID of the community related to the message
            - task_id: The identifier of the target task
    """
    LABEL = "TaskSelectionNotification"
    OUTCOME_ACCEPTED = 'accepted'
    OUTCOME_REFUSED = 'refused'

    def __init__(self, app_id: str, receiver_id: str, outcome: str, attributes: dict) -> None:
        accepted_outcomes = [self.OUTCOME_ACCEPTED, self.OUTCOME_REFUSED]
        if outcome not in accepted_outcomes:
            raise ValueError(f"Outcome must be one of {accepted_outcomes}, got [{outcome}]")
        attributes.update({"outcome": outcome})
        super().__init__(app_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> TaskSelectionNotification:
        return TaskSelectionNotification(
            raw["appId"],
            raw["receiverId"],
            raw["attributes"]["outcome"],
            raw["attributes"]
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
        - receiver_id: The Wenet user ID of the recipient of the message
        - outcome: The outcome of the task
        - attributes: dictionary with additional attributes of the message. It may contain
            - community_id: ID of the community related to the message
            - task_id: The identifier of the target task
    """
    LABEL = "TaskConcludedNotification"
    OUTCOME_COMPLETED = "completed"
    OUTCOME_CANCELLED = "cancelled"
    OUTCOME_FAILED = "failed"

    def __init__(self, app_id: str, receiver_id: str, outcome: str, attributes: dict) -> None:
        accepted_outcomes = [self.OUTCOME_COMPLETED, self.OUTCOME_CANCELLED, self.OUTCOME_FAILED]
        if outcome not in accepted_outcomes:
            raise ValueError(f"Outcome must be one of {accepted_outcomes}, got [{outcome}]")
        attributes.update({"outcome": outcome})
        super().__init__(app_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> TaskConcludedNotification:
        return TaskConcludedNotification(
            raw["appId"],
            raw["receiverId"],
            raw["attributes"]["outcome"],
            raw["attributes"]
        )

    @property
    def outcome(self) -> str:
        return self.attributes["outcome"]


class IncentiveMessage(Message):
    """
    This message is used to send an incentive to an user.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - receiver_id: The Wenet user ID of the recipient of the message
        - issuer: the issuer of the incentive
        - content: the content of the incentive
        - attributes: dictionary with additional attributes of the message. It may contain
            - community_id: ID of the community related to the message
            - task_id: The identifier of the target task
    """
    LABEL = "IncentiveMessage"

    def __init__(self, app_id: str, receiver_id: str, issuer: str, content: str, attributes: dict) -> None:
        attributes.update({
            "issuer": issuer,
            "content": content,
        })
        super().__init__(app_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> IncentiveMessage:
        return IncentiveMessage(
            raw["appId"],
            raw["receiverId"],
            raw["attributes"]["issuer"],
            raw["attributes"]["content"],
            raw["attributes"]
        )

    @property
    def issuer(self) -> str:
        return self.attributes["issuer"]

    @property
    def content(self) -> str:
        return self.attributes["content"]


class IncentiveBadge(Message):
    """
    This message is used to send a badge to an user.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - receiver_id: The Wenet user ID of the recipient of the message
        - issuer: the issuer of the incentive
        - badge_class: the class of the badge
        - image_url: the URL of the image of the badge
        - criteria: the criteria with which the badge was given
        - message: the content of the incentive
        - attributes: dictionary with additional attributes of the message. It may contain
            - community_id: ID of the community related to the message
            - task_id: The identifier of the target task
    """
    LABEL = "IncentiveBadge"

    def __init__(self, app_id: str, receiver_id: str, issuer: str, badge_class: str, image_url: str, criteria: str,
                 message: str, attributes: dict) -> None:
        attributes.update({
            "issuer": issuer,
            "badgeClass": badge_class,
            "imageUrl": image_url,
            "criteria": criteria,
            "message": message,
        })
        super().__init__(app_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> IncentiveBadge:
        return IncentiveBadge(
            raw["appId"],
            raw["receiverId"],
            raw["attributes"]["issuer"] if "issuer" in raw["attributes"] else raw["attributes"]["Issuer"],
            raw["attributes"]["badgeClass"] if "badgeClass" in raw["attributes"] else raw["attributes"]["Badge"]["BadgeClass"],
            raw["attributes"]["imageUrl"] if "imageUrl" in raw["attributes"] else raw["attributes"]["Badge"]["ImgUrl"],
            raw["attributes"]["criteria"] if "criteria" in raw["attributes"] else raw["attributes"]["Badge"]["Criteria"],
            raw["attributes"]["message"] if "message" in raw["attributes"] else raw["attributes"]["Badge"]["Message"],
            raw["attributes"]
        )

    @property
    def issuer(self) -> str:
        return self.attributes["issuer"]

    @property
    def badge_class(self) -> str:
        return self.attributes["badgeClass"]

    @property
    def image_url(self) -> str:
        return self.attributes["imageUrl"]

    @property
    def criteria(self) -> str:
        return self.attributes["criteria"]

    @property
    def message(self) -> str:
        return self.attributes["message"]


class QuestionToAnswerMessage(Message):
    """
    Message containing a new question to be answered.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - receiver_id: The Wenet user ID of the recipient of the message
        - label: The type of the message
        - attributes: dictionary with additional attributes of the message. It may contain
            - community_id: ID of the community related to the message
            - task_id: The identifier of the target task
            - question: The question to be answered
            - user_id: The author of the question
    """
    LABEL = "QuestionToAnswerMessage"

    def __init__(self, app_id: str, receiver_id: str, attributes: dict, question: str, user_id: str) -> None:
        attributes.update({
            "question": question,
            "userId": user_id,
        })
        super().__init__(app_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> QuestionToAnswerMessage:
        return QuestionToAnswerMessage(
            raw["appId"],
            raw["receiverId"],
            raw["attributes"],
            raw["attributes"]["question"],
            raw["attributes"]["userId"]
        )

    @property
    def question(self) -> str:
        return self.attributes["question"]

    @property
    def user_id(self) -> str:
        return self.attributes["userId"]


class AnsweredQuestionMessage(Message):
    """
    Message containing a new answer to a question.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - receiver_id: The Wenet user ID of the recipient of the message
        - label: The type of the message
        - attributes: dictionary with additional attributes of the message. It may contain
            - community_id: ID of the community related to the message
            - task_id: The identifier of the target task
            - answer: The answer to the question
            - userId: The author of the question
            - transaction_id: The id of the transaction associated with the answer
    """
    LABEL = "AnsweredQuestionMessage"

    def __init__(self, app_id: str, receiver_id: str, answer: str, transaction_id: str, user_id: str,
                 attributes: dict) -> None:
        attributes.update({
            "answer": answer,
            "transactionId": transaction_id,
            "userId": user_id,
        })
        super().__init__(app_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> AnsweredQuestionMessage:
        return AnsweredQuestionMessage(
            raw["appId"],
            raw["receiverId"],
            raw["attributes"]["answer"],
            raw["attributes"]["transactionId"],
            raw["attributes"]["userId"],
            raw["attributes"]
        )

    @property
    def answer(self) -> str:
        return self.attributes["answer"]

    @property
    def transaction_id(self) -> str:
        return self.attributes["transactionId"]

    @property
    def user_id(self) -> str:
        return self.attributes["userId"]


class AnsweredPickedMessage(Message):
    """
    Message received when an answer is picked as the best one.

    Attributes:
        - app_id: ID of the Wenet application related to the message
        - receiver_id: The Wenet user ID of the recipient of the message
        - label: The type of the message
        - attributes: dictionary with additional attributes of the message. It may contain
            - community_id: ID of the community related to the message
            - task_id: The identifier of the target task
            - transaction_id: The id of the transaction associated with the answer
    """
    LABEL = "AnsweredPickedMessage"

    def __init__(self, app_id: str, receiver_id: str, task_id: str, transaction_id: str, attributes: dict) -> None:
        attributes.update({
            "transactionId": transaction_id,
            "taskId": task_id,
        })
        super().__init__(app_id, receiver_id, self.LABEL, attributes)

    @staticmethod
    def from_repr(raw: dict) -> AnsweredPickedMessage:
        return AnsweredPickedMessage(
            raw["appId"],
            raw["receiverId"],
            raw["attributes"]["taskId"],
            raw["attributes"]["transactionId"],
            raw["attributes"]
        )

    @property
    def transaction_id(self) -> str:
        return self.attributes["transactionId"]

    @property
    def task_id(self) -> str:
        return self.attributes["taskId"]
