from __future__ import absolute_import, annotations

from unittest import TestCase

from test.wenet_test.common.interface.mock.collector import MockServiceCollector
from wenet.common.interface.collector import ServiceCollector
from wenet.common.interface.hub import HubInterface
from wenet.common.interface.incentive_server import IncentiveServerInterface
from wenet.common.interface.logger import LoggerInterface
from wenet.common.interface.profile_manager import ProfileManagerInterface
from wenet.common.interface.service_api import ServiceApiInterface
from wenet.common.interface.task_manager import TaskManagerInterface


class TestServiceCollector(TestCase):

    def test_build(self):
        collector = MockServiceCollector.build()
        self.assertIsInstance(collector, ServiceCollector)
        self.assertIsInstance(collector.service_api, ServiceApiInterface)
        self.assertIsInstance(collector.profile_manager, ProfileManagerInterface)
        self.assertIsInstance(collector.incentive_server, IncentiveServerInterface)
        self.assertIsInstance(collector.task_manager, TaskManagerInterface)
        self.assertIsInstance(collector.logger, LoggerInterface)
        self.assertIsInstance(collector.hub, HubInterface)
