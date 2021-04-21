from __future__ import absolute_import, annotations

import logging
import os
from typing import Optional

from wenet.common.interface.component import ComponentInterface
from wenet.common.interface.client import RestClient, ApikeyClient


logger = logging.getLogger("wenet.common.interface.incentive_server")


class IncentiveServerInterface(ComponentInterface):

    COMPONENT_PATH = os.getenv("INCENTIVE_SERVER_PATH", "/incentive_server")

    def __init__(self, client: RestClient, instance: str = ComponentInterface.PRODUCTION_INSTANCE, base_headers: Optional[dict] = None):
        if isinstance(client, ApikeyClient):
            base_url = instance + self.COMPONENT_PATH
        else:
            raise ValueError("Not a valid client for the incentive server interface")

        super().__init__(client, base_url, base_headers)

    def get_cohorts(self, headers: Optional[dict] = None) -> dict:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}/api/UsersCohorts/", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")
