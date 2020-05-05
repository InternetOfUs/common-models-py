from __future__ import absolute_import, annotations

from wenet.common.model.message.exception import NotificationTypeError, EventTypeError, MessageTypeError
from wenet.common.model.message.message import BaseMessage, TextualMessage, TaskNotification, TaskConcludedNotification, \
    TaskVolunteerNotification, TaskProposalNotification, MessageFromUserNotification, Event, NewUserForPlatform, \
    TaskSelectionNotification


class MessageBuilder:

    @staticmethod
    def build(raw_message: dict) -> BaseMessage:
        """
        It may raise ValueError or KeyError, to be caught where this method is used

        :param raw_message: the raw message representation
        :return BaseMessage: the message model
        :raises ValueError ValueError NotificationTypeError EventTypeError MessageTypeError:
        """
        message_type = raw_message["type"]
        if message_type == TextualMessage.TYPE:
            message = TextualMessage.from_repr(raw_message)
        elif message_type == TaskNotification.TYPE:
            notification_type = raw_message["notificationType"]
            if notification_type == TaskConcludedNotification.TYPE:
                message = TaskConcludedNotification.from_repr(raw_message)
            elif notification_type == TaskVolunteerNotification.TYPE:
                message = TaskVolunteerNotification.from_repr(raw_message)
            elif notification_type == TaskProposalNotification.TYPE:
                message = TaskProposalNotification.from_repr(raw_message)
            elif notification_type == MessageFromUserNotification.TYPE:
                message = MessageFromUserNotification.from_repr(raw_message)
            elif notification_type == TaskSelectionNotification.TYPE:
                message = TaskSelectionNotification.from_repr(raw_message)
            else:
                raise NotificationTypeError(notification_type)
        elif message_type == Event.TYPE:
            event_type = raw_message["eventType"]
            if event_type == NewUserForPlatform.TYPE:
                message = NewUserForPlatform.from_repr(raw_message)
            else:
                raise EventTypeError(event_type)
        else:
            raise MessageTypeError(message_type)
        return message
