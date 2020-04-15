from __future__ import absolute_import, annotations


class Message:
    TYPE_TEXTUAL_MESSAGE = "textualMessage"
    TYPE_TASK_NOTIFICATION = 'taskNotification'

    def __init__(self, type: str, recipient_id: str, title: str, text: str) -> None:
        types = [self.TYPE_TASK_NOTIFICATION, self.TYPE_TEXTUAL_MESSAGE]
        if type not in types:
            raise ValueError("Message type must be either %s given [%s]" % (str(types), type))
        self.type = type
        self.recipient_id = recipient_id
        self.title = title
        self.text = text

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Message):
            return False
        return self.type == o.type and self.recipient_id == o.recipient_id and self.title == o.title and \
               self.text == o.text

    def to_repr(self) -> dict:
        return {
            "type": self.type,
            "recipient_id": self.recipient_id,
            "title": self.title,
            "text": self.text
        }

    @staticmethod
    def from_repr(raw: dict) -> Message:
        return Message(raw["type"], raw["recipient_id"], raw["title"], raw["text"])


class TextualMessage(Message):
    TYPE = Message.TYPE_TEXTUAL_MESSAGE

    def __init__(self, recipient_id: str, title: str, text: str) -> None:
        super().__init__(self.TYPE, recipient_id, title, text)


class TaskNotification(Message):
    TYPE = Message.TYPE_TASK_NOTIFICATION
    NOTIFICATION_TYPE_PROPOSAL = "taskProposal"
    NOTIFICATION_TYPE_VOLUNTEER = "taskVolunteer"
    NOTIFICATION_TYPE_CONCLUDED = "taskConcluded"
    NOTIFICATION_TYPE_MESSAGE_FROM_USER = "messageFromUser"

    def __init__(self, recipient_id: str, title: str, text: str, description: str, task_id: str,
                 notification_type: str) -> None:
        super().__init__(self.TYPE, recipient_id, title, text)
        types = [self.NOTIFICATION_TYPE_PROPOSAL, self.NOTIFICATION_TYPE_VOLUNTEER, self.NOTIFICATION_TYPE_CONCLUDED,
                 self.NOTIFICATION_TYPE_MESSAGE_FROM_USER]
        if notification_type not in types:
            raise ValueError("Notification type must be either %s. Given [%s]" % (str(types), notification_type))
        self.description = description
        self.task_id = task_id
        self.notification_type = notification_type

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TaskNotification):
            return False
        return super().__eq__(o) and self.description == o.description and self.task_id == o.task_id and \
               self.notification_type == o.notification_type

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr["description"] = self.description
        base_repr["task_id"] = self.task_id
        base_repr["notification_type"] = self.notification_type
        return base_repr

    @staticmethod
    def from_repr(raw: dict) -> TaskNotification:
        return TaskNotification(
            raw["recipient_id"],
            raw["title"],
            raw["text"],
            raw["description"],
            raw["task_id"],
            raw["notification_type"]
        )


class TaskProposalNotification(TaskNotification):
    NOTIFICATION_TYPE = TaskNotification.NOTIFICATION_TYPE_PROPOSAL

    def __init__(self, recipient_id: str, title: str, text: str, description: str, task_id: str) -> None:
        super().__init__(recipient_id, title, text, description, task_id, self.NOTIFICATION_TYPE)


class TaskVolunteerNotification(TaskNotification):
    NOTIFICATION_TYPE = TaskNotification.NOTIFICATION_TYPE_VOLUNTEER

    def __init__(self, recipient_id: str, title: str, text: str, description: str, task_id: str) -> None:
        super().__init__(recipient_id, title, text, description, task_id, self.NOTIFICATION_TYPE)


class MessageFromUserNotification(TaskNotification):
    NOTIFICATION_TYPE = TaskNotification.NOTIFICATION_TYPE_MESSAGE_FROM_USER

    def __init__(self, recipient_id: str, title: str, text: str, description: str, task_id: str,
                 sender_id: str) -> None:
        super().__init__(recipient_id, title, text, description, task_id, self.NOTIFICATION_TYPE)
        self.sender_id = sender_id

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, MessageFromUserNotification):
            return False
        return super().__eq__(o) and self.sender_id == o.sender_id

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr["sender_id"] = self.sender_id
        return base_repr

    @staticmethod
    def from_repr(raw: dict) -> MessageFromUserNotification:
        return MessageFromUserNotification(
            raw["recipient_id"],
            raw["title"],
            raw["text"],
            raw["description"],
            raw["task_id"],
            raw["sender_id"]
        )


class TaskConcludedNotification(TaskNotification):
    NOTIFICATION_TYPE = TaskNotification.NOTIFICATION_TYPE_CONCLUDED

    OUTCOME_CANCELLED = 'cancelled'
    OUTCOME_SUCCESSFUL = 'successful'
    OUTCOME_FAILED = 'failed'

    def __init__(self, recipient_id: str, title: str, text: str, description: str, task_id: str, outcome: str) -> None:
        super().__init__(recipient_id, title, text, description, task_id, self.NOTIFICATION_TYPE)
        valid_outcomes = [self.OUTCOME_CANCELLED, self.OUTCOME_SUCCESSFUL, self.OUTCOME_FAILED]
        if outcome not in valid_outcomes:
            raise ValueError("Outcome must be either %s. Got [%s]" % (str(valid_outcomes), outcome))
        self.outcome = outcome

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TaskConcludedNotification):
            return False
        return super().__eq__(o) and self.outcome == o.outcome

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr["outcome"] = self.outcome
        return base_repr

    @staticmethod
    def from_repr(raw: dict) -> TaskConcludedNotification:
        return TaskConcludedNotification(
            raw["recipient_id"],
            raw["title"],
            raw["text"],
            raw["description"],
            raw["task_id"],
            raw["outcome"]
        )
