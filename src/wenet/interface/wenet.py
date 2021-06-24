from __future__ import absolute_import, annotations

from typing import Optional

from wenet.interface.client import RestClient
from wenet.interface.hub import HubInterface
from wenet.interface.incentive_server import IncentiveServerInterface
from wenet.interface.logger import LoggerInterface
from wenet.interface.profile_manager import ProfileManagerInterface
from wenet.interface.service_api import ServiceApiInterface
from wenet.interface.task_manager import TaskManagerInterface


class WeNet:

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
    def build(client: RestClient, platform_url: str = "https://internetofus.u-hopper.com/prod", extra_headers: Optional[dict] = None) -> WeNet:
        return WeNet(
            service_api=ServiceApiInterface(client, platform_url=platform_url, extra_headers=extra_headers),
            profile_manager=ProfileManagerInterface(client, platform_url=platform_url, extra_headers=extra_headers),
            incentive_server=IncentiveServerInterface(client, platform_url=platform_url, extra_headers=extra_headers),
            task_manager=TaskManagerInterface(client, platform_url=platform_url, extra_headers=extra_headers),
            logger=LoggerInterface(client, platform_url=platform_url, extra_headers=extra_headers),
            hub=HubInterface(client, platform_url=platform_url, extra_headers=extra_headers)
        )
