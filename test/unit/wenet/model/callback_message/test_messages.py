from __future__ import absolute_import, annotations

import random
from unittest import TestCase
from uuid import uuid4

from wenet.model.callback_message.message import Message


class TestMessage(TestCase):
    def test_repr(self):
        app_id = str(uuid4())
        community_id = str(uuid4())
        receiver_id = str(uuid4())
        task_id = str(uuid4())
        label = str(uuid4())
        attributes = {
            "key": "value",
            "communityId": community_id,
            "taskId": task_id
        }
        message = Message(app_id, receiver_id, label, attributes)
        message_repr = message.to_repr()
        self.assertEqual(Message.from_repr(message_repr), message)
        self.assertEqual(message.task_id, task_id)
        self.assertEqual(message.community_id, community_id)

    def test_with_empty_attributes(self):
        app_id = str(uuid4())
        receiver_id = str(uuid4())
        label = str(uuid4())
        attributes = {
            "key": "value",
        }
        message = Message(app_id, receiver_id, label, attributes)
        message_repr = message.to_repr()
        self.assertEqual(Message.from_repr(message_repr), message)
        self.assertIsNone(message.community_id)
        self.assertIsNone(message.task_id)
