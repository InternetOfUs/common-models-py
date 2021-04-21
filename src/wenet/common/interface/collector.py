from __future__ import absolute_import, annotations

import os
from typing import Optional

from wenet.common.interface.component import ComponentInterface
from wenet.common.interface.client import ApikeyClient
from wenet.common.interface.hub import HubInterface
from wenet.common.interface.incentive_server import IncentiveServerInterface
from wenet.common.interface.logger import LoggerInterface
from wenet.common.interface.profile_manager import ProfileManagerInterface
from wenet.common.interface.service_api import ServiceApiInterface
from wenet.common.interface.task_manager import TaskManagerInterface


class ServiceCollector:

    def __init__(self,
                 service_api: ServiceApiInterface,
                 profile_manager: ProfileManagerInterface,
                 incentive_server: IncentiveServerInterface,
                 task_manager: TaskManagerInterface,
                 logger: LoggerInterface,
                 hub: HubInterface
                 ):
        self.service_api = service_api
        self.profile_manager = profile_manager
        self.incentive_server = incentive_server
        self.task_manager = task_manager
        self.logger = logger
        self.hub = hub

    @staticmethod
    def build(base_headers: Optional[dict] = None) -> ServiceCollector:

        instance = os.getenv("INSTANCE", ComponentInterface.PRODUCTION_INSTANCE)
        client = ApikeyClient(os.getenv("APIKEY"))

        return ServiceCollector(
            service_api=ServiceApiInterface(client, instance=instance, base_headers=base_headers),
            profile_manager=ProfileManagerInterface(client, instance=instance, base_headers=base_headers),
            incentive_server=IncentiveServerInterface(client, instance=instance, base_headers=base_headers),
            task_manager=TaskManagerInterface(client, instance=instance, base_headers=base_headers),
            logger=LoggerInterface(client, instance=instance, base_headers=base_headers),
            hub=HubInterface(client, instance=instance, base_headers=base_headers)
        )
