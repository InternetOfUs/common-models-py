from wenet.common.messages.exceptions import NotificationTypeError, MessageTypeError
from wenet.common.messages.models import Message, TextualMessage, TaskNotification, TaskConcludedNotification, \
    TaskVolunteerNotification, TaskProposalNotification, MessageFromUserNotification


class MessageBuilder:

    @staticmethod
    def build(raw_message: dict) -> Message:
        """
        It may raise ValueError or KeyError, to be caught where this method is used
        """
        message_type = raw_message["type"]
        if message_type == Message.TYPE_TEXTUAL_MESSAGE:
            message = TextualMessage.from_repr(raw_message)
        elif message_type == Message.TYPE_TASK_NOTIFICATION:
            notification_type = raw_message["notification_type"]
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
        else:
            raise MessageTypeError(message_type)
        return message
