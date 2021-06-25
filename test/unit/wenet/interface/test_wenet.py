from __future__ import absolute_import, annotations

from unittest import TestCase

from test.unit.wenet.interface.mock.client import MockApikeyClient
from test.unit.wenet.interface.mock.collector import MockWeNet
from wenet.interface.wenet import WeNet
from wenet.interface.hub import HubInterface
from wenet.interface.incentive_server import IncentiveServerInterface
from wenet.interface.logger import LoggerInterface
from wenet.interface.profile_manager import ProfileManagerInterface
from wenet.interface.service_api import ServiceApiInterface
from wenet.interface.task_manager import TaskManagerInterface


class TestServiceCollector(TestCase):

    def test_build(self):
        wenet = MockWeNet.build(MockApikeyClient())
        self.assertIsInstance(wenet, WeNet)
        self.assertIsInstance(wenet.service_api, ServiceApiInterface)
        self.assertIsInstance(wenet.profile_manager, ProfileManagerInterface)
        self.assertIsInstance(wenet.incentive_server, IncentiveServerInterface)
        self.assertIsInstance(wenet.task_manager, TaskManagerInterface)
        self.assertIsInstance(wenet.logger, LoggerInterface)
        self.assertIsInstance(wenet.hub, HubInterface)
