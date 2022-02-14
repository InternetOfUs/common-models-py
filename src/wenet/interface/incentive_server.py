from __future__ import absolute_import, annotations

import logging
from typing import Optional, List

from wenet.interface.component import ComponentInterface
from wenet.interface.client import RestClient

logger = logging.getLogger("wenet.interface.incentive_server")


class IncentiveServerInterface(ComponentInterface):

    def __init__(self, client: RestClient, platform_url: str, component_path: str = "/incentive_server", extra_headers: Optional[dict] = None) -> None:
        base_url = platform_url + component_path
        super().__init__(client, base_url, extra_headers)

    def get_cohorts(self, headers: Optional[dict] = None) -> List[dict]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}/api/UsersCohorts/", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)
