from __future__ import absolute_import, annotations

from wenet.model.callback_message.event import Event, WeNetAuthenticationEvent
from wenet.model.callback_message.message import TextualMessage, Message, TaskConcludedNotification, \
    TaskVolunteerNotification, TaskProposalNotification, TaskSelectionNotification, IncentiveMessage, IncentiveBadge, \
    QuestionToAnswerMessage, AnsweredQuestionMessage


class MessageBuilder:

    @staticmethod
    def build(raw_message: dict) -> Message:
        """
        It may raise ValueError or KeyError, to be caught where this method is used

        :param raw_message: the raw message representation
        :return Message: the message model
        :raises ValueError KeyError:
        """
        message_label = raw_message["label"]
        if message_label == TextualMessage.LABEL:
            message = TextualMessage.from_repr(raw_message)
        elif message_label == TaskConcludedNotification.LABEL:
            message = TaskConcludedNotification.from_repr(raw_message)
        elif message_label == TaskVolunteerNotification.LABEL:
            message = TaskVolunteerNotification.from_repr(raw_message)
        elif message_label == TaskProposalNotification.LABEL:
            message = TaskProposalNotification.from_repr(raw_message)
        elif message_label == TaskSelectionNotification.LABEL:
            message = TaskSelectionNotification.from_repr(raw_message)
        elif message_label == IncentiveMessage.LABEL:
            message = IncentiveMessage.from_repr(raw_message)
        elif message_label == IncentiveBadge.LABEL:
            message = IncentiveBadge.from_repr(raw_message)
        elif message_label == QuestionToAnswerMessage.LABEL:
            message = QuestionToAnswerMessage.from_repr(raw_message)
        elif message_label == AnsweredQuestionMessage.LABEL:
            message = AnsweredQuestionMessage.from_repr(raw_message)
        else:
            message = Message.from_repr(raw_message)
        return message


class EventBuilder:

    @staticmethod
    def build(raw_event: dict) -> Event:
        """
        Build an event from a raw representation
        :param raw_event: the raw event representation
        :return Event: the event model
        :raises KeyError:
        """
        event_type = raw_event["type"]
        if event_type == WeNetAuthenticationEvent.TYPE:
            event = WeNetAuthenticationEvent.from_repr(raw_event)
        else:
            event = Event.from_repr(raw_event)
        return event
