from __future__ import absolute_import, annotations

import abc
from datetime import datetime
from typing import Optional

from wenet.model.logging_messages.contents import BaseContent


class BaseMessage(abc.ABC):
    """
    Base class containing all the common fields of a message.
    Attributes:
        - message_id: an unique string identifying the message
        - channel: the channel in which the message is passed (e.g. Facebook, Telegram)
        - user_id: the user ID to which the message is meant to
        - project: the project in which the message is exchanged
        - content: the content of the message
        - timestamp: the timestamp of the message. If None is given, the current timestamp is used
        - metadata: an optional dictionary containing key-value pairs
    """
    @staticmethod
    @abc.abstractmethod
    def get_type() -> str:
        """
        Get the string value of the type of the message
        """
        pass

    def __init__(self, message_id: str, channel: str, user_id: str, project: str, content: BaseContent,
                 timestamp: Optional[datetime] = None, metadata: Optional[dict] = None) -> None:
        self.type = self.get_type()
        self.message_id = message_id
        self.channel = channel
        self.user_id = user_id
        self.project = project
        self.content = content
        self.timestamp = timestamp
        self.metadata = metadata
        if not self.timestamp:
            self.timestamp = datetime.now()
        if not self.metadata:
            self.metadata = {}

    def to_repr(self) -> dict:
        return {
            "type": self.type,
            "messageId": self.message_id,
            "channel": self.channel,
            "userId": self.user_id,
            "project": self.project,
            "content": self.content.to_repr(),
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    @staticmethod
    def from_repr(raw: dict) -> BaseMessage:
        message_type = raw["type"]
        if message_type == RequestMessage.get_type():
            return RequestMessage.from_repr(raw)
        elif message_type == ResponseMessage.get_type():
            return ResponseMessage.from_repr(raw)
        elif message_type == NotificationMessage.get_type():
            return NotificationMessage.from_repr(raw)
        raise TypeError(f"Unexpected type [{message_type}] of message")

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BaseMessage):
            return False
        return self.type == o.type and self.message_id == o.message_id and self.channel == o.channel and \
            self.user_id == o.user_id and self.project == o.project and self.content == o.content and \
            self.timestamp == o.timestamp and self.metadata == o.metadata


class RequestMessage(BaseMessage):
    """
    Request message, with the same attributes of the base message
    """
    TYPE = "REQUEST"

    @staticmethod
    def get_type() -> str:
        return RequestMessage.TYPE

    @staticmethod
    def from_repr(raw: dict) -> RequestMessage:
        return RequestMessage(
            raw["messageId"],
            raw["channel"],
            raw["userId"],
            raw["project"],
            BaseContent.from_repr(raw["content"]),
            datetime.fromisoformat(raw["timestamp"]),
            raw.get("metadata", None)
        )


class ResponseMessage(BaseMessage):
    """
    Request message, with the same attributes of the base message
    """
    TYPE = "RESPONSE"

    def __init__(self, message_id: str, channel: str, user_id: str, project: str, content: BaseContent,
                 response_to: str, timestamp: Optional[datetime] = None, metadata: Optional[dict] = None) -> None:
        super().__init__(message_id, channel, user_id, project, content, timestamp, metadata)
        self.response_to = response_to

    @staticmethod
    def get_type() -> str:
        return ResponseMessage.TYPE

    @staticmethod
    def from_repr(raw: dict) -> ResponseMessage:
        return ResponseMessage(
            raw["messageId"],
            raw["channel"],
            raw["userId"],
            raw["project"],
            BaseContent.from_repr(raw["content"]),
            raw["responseTo"],
            datetime.fromisoformat(raw["timestamp"]),
            raw.get("metadata", None)
        )

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr.update({"responseTo": self.response_to})
        return base_repr


class NotificationMessage(BaseMessage):
    """
    Request message, with the same attributes of the base message
    """
    TYPE = "NOTIFICATION"

    @staticmethod
    def get_type() -> str:
        return NotificationMessage.TYPE

    @staticmethod
    def from_repr(raw: dict) -> NotificationMessage:
        return NotificationMessage(
            raw["messageId"],
            raw["channel"],
            raw["userId"],
            raw["project"],
            BaseContent.from_repr(raw["content"]),
            datetime.fromisoformat(raw["timestamp"]),
            raw.get("metadata", None)
        )
