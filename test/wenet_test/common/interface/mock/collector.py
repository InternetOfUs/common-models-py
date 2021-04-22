from __future__ import absolute_import, annotations

from typing import Optional

from test.wenet_test.common.interface.mock.client import MockApikeyClient
from wenet.common.interface.collector import ServiceCollector
from wenet.common.interface.hub import HubInterface
from wenet.common.interface.incentive_server import IncentiveServerInterface
from wenet.common.interface.logger import LoggerInterface
from wenet.common.interface.profile_manager import ProfileManagerInterface
from wenet.common.interface.service_api import ServiceApiInterface
from wenet.common.interface.task_manager import TaskManagerInterface


class MockServiceCollector(ServiceCollector):

    @staticmethod
    def build(base_headers: Optional[dict] = None) -> ServiceCollector:
        instance = ""
        client = MockApikeyClient()

        return ServiceCollector(
            service_api=ServiceApiInterface(client, instance=instance, base_headers=base_headers),
            profile_manager=ProfileManagerInterface(client, instance=instance, base_headers=base_headers),
            incentive_server=IncentiveServerInterface(client, instance=instance, base_headers=base_headers),
            task_manager=TaskManagerInterface(client, instance=instance, base_headers=base_headers),
            logger=LoggerInterface(client, instance=instance, base_headers=base_headers),
            hub=HubInterface(client, instance=instance, base_headers=base_headers)
        )
