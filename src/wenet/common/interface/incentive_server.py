from __future__ import absolute_import, annotations

import logging

from wenet.common.interface.base import BaseInterface
from wenet.common.interface.client import RestClient


logger = logging.getLogger("wenet.common.interface.incentive_server")


class IncentiveServerInterface(BaseInterface):

    def __init__(self, client: RestClient, instance: str = BaseInterface.PRODUCTION_INSTANCE):
        base_url = instance + "/incentive_server"
        super().__init__(client, base_url)

    def get_cohorts(self) -> dict:
        response = self._client.get(self._base_url + "/api/UsersCohorts/")

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request has return a code {response.status_code} with content {response.text}")
