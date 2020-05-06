from __future__ import absolute_import, annotations


class BaseMessage:
    """
    Generic class representing a message coming from WeNet
    """

    def __init__(self, message_type: str) -> None:
        """
        Create a BaseMessage instance
        :param message_type: the type of message, one of Task notification, Event or Textual message
        :raises ValueError: in case the specified type is not one of the aforementioned
        """
        allowed_types = [TaskNotification.TYPE, TextualMessage.TYPE, Event.TYPE]
        if message_type not in allowed_types:
            raise ValueError(f"type {message_type} not valid. It must be one of {allowed_types}")
        self.type = message_type

    def to_repr(self) -> dict:
        return {"type": self.type}

    @staticmethod
    def from_repr(raw: dict) -> BaseMessage:
        return BaseMessage(raw["type"])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BaseMessage):
            return False
        return self.type == o.type


class Message(BaseMessage):
    """
    Common class for a message, that can be either a textual message or a notification
    """

    def __init__(self, message_type: str, recipient_id: str, title: str, text: str) -> None:
        """
        Create a Message instance
        :param message_type: type of the message, either a notification or a textual message
        :param recipient_id: WeNet ID of the recipient
        :param title: title of the message
        :param text: text of the message
        :raises ValueError: in case the message type is wrong
        """
        types = [TaskNotification.TYPE, TextualMessage.TYPE]
        if message_type not in types:
            raise ValueError("Message type must be either %s given [%s]" % (str(types), message_type))
        super().__init__(message_type)
        self.recipient_id = recipient_id
        self.title = title
        self.text = text

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Message):
            return False
        return self.type == o.type and self.recipient_id == o.recipient_id and self.title == o.title and self.text == o.text

    def to_repr(self) -> dict:
        return {
            "type": self.type,
            "recipientId": self.recipient_id,
            "title": self.title,
            "text": self.text
        }

    @staticmethod
    def from_repr(raw: dict) -> Message:
        return Message(raw["type"], raw["recipientId"], raw["title"], raw["text"])


class TextualMessage(Message):
    """
    Class representing a textual message between two users
    """

    TYPE = "textualMessage"

    def __init__(self, recipient_id: str, title: str, text: str) -> None:
        """
        Construct a TextualMessage
        :param recipient_id: the WeNet ID of the recipient
        :param title: the title of the message
        :param text: the text of the message
        """
        super().__init__(self.TYPE, recipient_id, title, text)

    @staticmethod
    def from_repr(raw: dict) -> TextualMessage:
        message = Message.from_repr(raw)
        return TextualMessage(message.recipient_id, message.title, message.text)


class TaskNotification(Message):
    """
    General notification class
    """

    TYPE = "taskNotification"

    def __init__(self, recipient_id: str, title: str, text: str, description: str, task_id: str,
                 notification_type: str) -> None:
        """
        Create a general notification object
        :param recipient_id: WeNet ID of the recipient
        :param title: title of the notification
        :param text: text of the notification
        :param description: description of the notification
        :param task_id: task related to the notification
        :param notification_type: type of the notification. It must be on of: taskProposal, taskVolunteer, taskConcluded
        or messageFromUser
        :raises ValueError: in case the notification type is wrong
        """
        super().__init__(TaskNotification.TYPE, recipient_id, title, text)
        types = [TaskProposalNotification.TYPE, TaskVolunteerNotification.TYPE, TaskConcludedNotification.TYPE,
                 MessageFromUserNotification.TYPE, TaskSelectionNotification.TYPE]
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
        base_repr["taskId"] = self.task_id
        base_repr["notificationType"] = self.notification_type
        return base_repr

    @staticmethod
    def from_repr(raw: dict) -> TaskNotification:
        return TaskNotification(
            raw["recipientId"],
            raw["title"],
            raw["text"],
            raw["description"],
            raw["taskId"],
            raw["notificationType"]
        )


class TaskProposalNotification(TaskNotification):
    """
    Notification used to propose a task to a user
    """

    TYPE = "taskProposal"

    def __init__(self, recipient_id: str, title: str, text: str, description: str, task_id: str) -> None:
        """
        Create a TaskProposalNotification
        :param recipient_id: WeNet ID of the recipient
        :param title: title of the notification
        :param text: text of the notification
        :param description: description of the notification
        :param task_id: task related to the notification
        """
        super().__init__(recipient_id, title, text, description, task_id, self.TYPE)

    @staticmethod
    def from_repr(raw: dict) -> TaskProposalNotification:
        message = TaskNotification.from_repr(raw)
        return TaskProposalNotification(message.recipient_id, message.title, message.text, message.description,
                                        message.task_id)


class TaskVolunteerNotification(TaskNotification):
    """
    Notification used to notify a task owner that a candidate volunteer has sent its application to participate
    """
    TYPE = "taskVolunteer"

    def __init__(self, recipient_id: str, title: str, text: str, description: str, task_id: str, volunteer_id: str) -> None:
        """
        Create a TaskVolunteerNotification
        :param recipient_id: WeNet Id of the recipient
        :param title: title of the notification
        :param text: text of the notification
        :param description: description of the notification
        :param task_id: task related to the notification
        :param volunteer_id: id of the volunteer that applied to the task
        """
        super().__init__(recipient_id, title, text, description, task_id, self.TYPE)
        self.volunteer_id = volunteer_id

    @staticmethod
    def from_repr(raw: dict) -> TaskVolunteerNotification:
        message = TaskNotification.from_repr(raw)
        return TaskVolunteerNotification(message.recipient_id, message.title, message.text, message.description,
                                         message.task_id, raw["volunteerId"])

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr["volunteerId"] = self.volunteer_id
        return base_repr

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TaskVolunteerNotification):
            return False
        return super().__eq__(o) and self.volunteer_id == o.volunteer_id


class MessageFromUserNotification(TaskNotification):
    """
    Notification to notify of a new message from a WeNet user
    """

    TYPE = "messageFromUser"

    def __init__(self, recipient_id: str, title: str, text: str, description: str, task_id: str,
                 sender_id: str) -> None:
        """
        Create a new notification for a new message from an user
        :param recipient_id: WeNet Id of the recipient
        :param title: title of the notification
        :param text: text of the notification
        :param description: description of the notification
        :param task_id: task related to the notification
        :param sender_id: WeNet Id of the sender
        """
        super().__init__(recipient_id, title, text, description, task_id, self.TYPE)
        self.sender_id = sender_id

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, MessageFromUserNotification):
            return False
        return super().__eq__(o) and self.sender_id == o.sender_id

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr["senderId"] = self.sender_id
        return base_repr

    @staticmethod
    def from_repr(raw: dict) -> MessageFromUserNotification:
        return MessageFromUserNotification(
            raw["recipientId"],
            raw["title"],
            raw["text"],
            raw["description"],
            raw["taskId"],
            raw["senderId"]
        )


class TaskConcludedNotification(TaskNotification):
    """
    Notification used to conclude a task
    """

    TYPE = "taskConcluded"

    OUTCOME_CANCELLED = 'cancelled'
    OUTCOME_SUCCESSFUL = 'completed'
    OUTCOME_FAILED = 'failed'

    def __init__(self, recipient_id: str, title: str, text: str, description: str, task_id: str, outcome: str) -> None:
        """
        Create a notification to close a task
        :param recipient_id: WeNet Id of the recipient
        :param title: title of the notification
        :param text: text of the notification
        :param description: description of the notification
        :param task_id: task related to the notification
        :param outcome: outcome of the task. Either cancelled, completed or failed
        :raises ValueError: in case the given outcome is not valid
        """
        super().__init__(recipient_id, title, text, description, task_id, self.TYPE)
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
            raw["recipientId"],
            raw["title"],
            raw["text"],
            raw["description"],
            raw["taskId"],
            raw["outcome"]
        )


class TaskSelectionNotification(TaskNotification):
    """
    This notification is used in order to notify the user who volunteer about the decision of the task creator
    """
    TYPE = "selectionVolunteer"
    OUTCOME_ACCEPTED = 'accepted'
    OUTCOME_REFUSED = 'refused'

    def __init__(self, recipient_id: str, title: str, text: str, description: str, task_id: str, outcome: str) -> None:
        """
        Create a notification for the positive or negative selection of a volunteer
        :param recipient_id: WeNet Id of the recipient
        :param title: title of the notification
        :param text: text of the notification
        :param description: description of the notification
        :param task_id: task related to the notification
        :param outcome: outcome of the task. Either cancelled, completed or failed
        :raises ValueError: in case the given outcome is not valid
        """
        allowed_outcomes = [TaskSelectionNotification.OUTCOME_ACCEPTED, TaskSelectionNotification.OUTCOME_REFUSED]
        if outcome not in allowed_outcomes:
            raise ValueError("Outcome must be either %s. Got [%s]" % (str(allowed_outcomes), outcome))
        super().__init__(recipient_id, title, text, description, task_id, TaskSelectionNotification.TYPE)
        self.outcome = outcome

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TaskSelectionNotification):
            return False
        return super().__eq__(o) and self.outcome == o.outcome

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr["outcome"] = self.outcome
        return base_repr

    @staticmethod
    def from_repr(raw: dict) -> TaskSelectionNotification:
        return TaskSelectionNotification(
            raw["recipientId"],
            raw["title"],
            raw["text"],
            raw["description"],
            raw["taskId"],
            raw["outcome"]
        )


class Event(BaseMessage):
    """
    Base class for an event
    """

    TYPE = "event"

    def __init__(self, event_type: str) -> None:
        """
        Create a new event
        :param event_type: type of the event, it must be newUserForPlatform
        :raises ValueError: in case the specified event type is wrong
        """
        allowed_types = [NewUserForPlatform.TYPE]
        if event_type not in allowed_types:
            raise ValueError(f"Event type {event_type} not valid. It must be one of {allowed_types}")
        super().__init__(Event.TYPE)
        self.event_type = event_type

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Event):
            return False
        return super().__eq__(o) and self.event_type == o.event_type

    def to_repr(self) -> dict:
        base = super().to_repr()
        base["eventType"] = self.event_type
        return base

    @staticmethod
    def from_repr(raw: dict) -> Event:
        return Event(raw["eventType"])


class NewUserForPlatform(Event):
    """
    Event used to notify the bot that a new user has just logged into the WeNet Hub
    """

    TYPE = "newUserForPlatform"

    def __init__(self, app_id: str, user_id: str, platform: str) -> None:
        """
        Create a new NewUserForPlatform
        :param app_id: WeNet app related to the event
        :param user_id: WeNet user ID that has just logged in
        :param platform: platform on which the login happened - e.g. Telegram
        """
        super().__init__(NewUserForPlatform.TYPE)
        self.app_id = app_id
        self.user_id = user_id
        self.platform = platform

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, NewUserForPlatform):
            return False
        return super().__eq__(o) and self.app_id == o.app_id and self.user_id == o.user_id and \
            self.platform == o.platform

    def to_repr(self) -> dict:
        base = super().to_repr()
        base.update({
            "app": self.app_id,
            "userId": self.user_id,
            "platform": self.platform
        })
        return base

    @staticmethod
    def from_repr(raw: dict) -> NewUserForPlatform:
        return NewUserForPlatform(
            raw["app"],
            raw["userId"],
            raw["platform"]
        )
