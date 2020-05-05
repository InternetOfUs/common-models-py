from __future__ import absolute_import, annotations

from wenet.common.model.message.exception import NotificationTypeError, EventTypeError, MessageTypeError
from wenet.common.model.message.message import BaseMessage, TextualMessage, TaskNotification, TaskConcludedNotification, \
    TaskVolunteerNotification, TaskProposalNotification, MessageFromUserNotification, Event, NewUserForPlatform


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
        if message_type == BaseMessage.TYPE_TEXTUAL_MESSAGE:
            message = TextualMessage.from_repr(raw_message)
        elif message_type == BaseMessage.TYPE_TASK_NOTIFICATION:
            notification_type = raw_message["notificationType"]
            if notification_type == TaskNotification.NOTIFICATION_TYPE_CONCLUDED:
                message = TaskConcludedNotification.from_repr(raw_message)
            elif notification_type == TaskNotification.NOTIFICATION_TYPE_VOLUNTEER:
                message = TaskVolunteerNotification.from_repr(raw_message)
            elif notification_type == TaskNotification.NOTIFICATION_TYPE_PROPOSAL:
                message = TaskProposalNotification.from_repr(raw_message)
            elif notification_type == TaskNotification.NOTIFICATION_TYPE_MESSAGE_FROM_USER:
                message = MessageFromUserNotification.from_repr(raw_message)
            else:
                raise NotificationTypeError(notification_type)
        elif message_type == BaseMessage.TYPE_EVENT:
            event_type = raw_message["eventType"]
            if event_type == Event.TYPE_NEW_USER:
                message = NewUserForPlatform.from_repr(raw_message)
            else:
                raise EventTypeError(event_type)
        else:
            raise MessageTypeError(message_type)
        return message
